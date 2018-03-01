from GHC2018.input import Input
from GHC2018.models.Car import Car
from GHC2018.models.Route import Route
from GHC2018.models.ride import calculate_distance

from tqdm import tqdm


class Process:
    def __init__(self, input_data, debug=True):
        self.input_data = input_data
        self.debug = debug
        self.current_time = 0
        # self.get_routes()

    def initialise_cars(self):
        cars = []
        for i in range(0, self.input_data.vehicle_count):
            car = Car(i, 0, 0)
            cars.append(car)
        self.cars = cars

    def debug_print(self, message):
        if self.debug:
            print(message)

    def run(self):
        self.initialise_cars()
        self.rides = self.input_data.rides
        sim_range = range(0, self.input_data.sim_steps)
        if not self.debug:
            sim_range = tqdm(sim_range)
        for i in sim_range:
            self.debug_print('--- STEP {}/{} ---'.format(i, self.input_data.sim_steps))
            self.current_time = i
            # if cars are at their destination, end the ride
            self.end_rides()
            # schedule any cars that are not assigned a ride
            self.schedule_rides()
            # move any cars
            self.move_cars()
        self.debug_print('SIMULATION ENDED')
        print('{} rides completed. {} rides left unfinished'.format(
            len(self.get_completed_rides()),
            len(self.rides) - len(self.get_completed_rides()))
        )
        self.output_file()

    def output_file(self):
        output_file_path = self.input_data.file_path.replace('.in', '.out')
        car_rides = {}
        for ride in self.get_completed_rides():
            if ride.assigned_car in car_rides.keys():
                car_rides[ride.assigned_car].append(ride.ride_id)
            else:
                car_rides[ride.assigned_car] = [ride.ride_id]
        with open(output_file_path, 'w') as output_file:
            for car, rides in car_rides.items():
                output_string = str(len(rides))
                for ride_id in rides:
                    output_string += ' {}'.format(ride_id)
                output_file.write(output_string + '\n')

    def end_rides(self):
        self.debug_print('Checking if cars have arrived')
        completed_cars = [
            car for car in self.get_assigned_cars() if car.is_at_destination()
        ]
        self.debug_print('{} cars completed their ride this turn'.format(len(completed_cars)))
        for car in completed_cars:
            self.debug_print('Car {} has completed their ride'.format(car.car_id))
            car.complete_ride()
            if car.assigned_route_completed():
                car.complete_route()
            self.debug_print('{}/{} rides completed'.format(
                len(self.get_completed_rides()),
                len(self.rides)
            ))

    def get_completed_rides(self):
        return [ride for ride in self.input_data.rides if ride.completed]

    def schedule_rides(self):
        unassigned_cars = self.get_unassigned_cars()
        self.debug_print('Scheduling {} cars'.format(len(unassigned_cars)))
        unassigned_rides = self.get_unassigned_rides()
        if len(unassigned_rides) == 0:
            return
        for car in unassigned_cars:
            # next_ride = unassigned_rides.pop(0)
            next_possible_rides = self.get_next_possible_rides(car, self.current_time)
            if len(next_possible_rides) == 0:
                return
            next_ride = next_possible_rides[0]
            rides_for_route = [next_ride]
            # if not len(unassigned_rides) == 0:
            #     closest_next_rides = self.get_next_possible_rides(next_ride, self.current_time)
            #     if len(closest_next_rides) > 0:
            #         closest_next_ride = closest_next_rides[0]
            #         self.debug_print('Closest ride to {} is {}'.format(next_ride.ride_id, closest_next_ride.ride_id))
            #         unassigned_rides.pop(unassigned_rides.index(closest_next_ride))
            #         rides_for_route.append(closest_next_ride)
            route = Route(rides_for_route)
            self.debug_print('Assigned route with ride IDs {} to car: {}'.format(
                route.get_route_ride_ids(),
                car.car_id
            ))
            car.assign_route(route)

    def get_closest_ride_to_car(self, car, rides):
        closest_ride = rides[0]
        closest_distance = calculate_distance(car.row, closest_ride.row_start, car.col, closest_ride.col_start)
        for i in range(1, len(rides)):
            ride = rides[i]
            next_closest_distance = calculate_distance(car.row, ride.row_start, car.col, ride.col_start)
            if next_closest_distance < closest_distance:
                closest_ride = ride
                closest_distance = next_closest_distance
        return rides.pop(rides.index(closest_ride))

    def move_cars(self):
        for car in self.get_assigned_cars():
            self.debug_print('Moving car with ID: {}'.format(car.car_id))
            car.move_towards_destination()

    def get_assigned_cars(self):
        return [car for car in self.cars if car.assigned_route is not None]

    def get_unassigned_cars(self):
        return [car for car in self.cars if car.assigned_route is None]

    def get_unassigned_rides(self):
        return [ride for ride in self.input_data.rides if ride.assigned_car is None]
            
    def set_next_routes(self, route, routes):
        for t_route in routes:
            if not t_route is route:
                wait = t_route.ordered_rides[0].earliest_start -route.ordered_rides[-1].latest_finish
                if wait >= 0:
                    route.next_routes.append({'route':t_route, 'wait_time': wait})

    # def get_routes(self):
    #     routes = []
    #     rides_closests = []
    #
    #     for ride in self.input_data.rides:
    #         rides = self.get_next_possible_rides(ride, ride.earliest_start)
    #         rides_closests.append({'ride': ride, 'rides': rides})
    #
    #     rides_closests = sorted(rides_closests, key=lambda k: len(k['rides']), reverse=True)
    #     print(rides_closests)
    #     for ride_closest in rides_closests:
    #         last_ride = None
    #         while last_ride is None and len(ride_closest['rides']) > 0:
    #             temp_ride = ride_closest['rides'].pop()
    #             if(temp_ride.assigned_car is None):
    #                 last_ride = temp_ride
    #         if not last_ride is None:
    #             last_ride.assigned_car = 1
    #             ride_closest['ride'].assigned_car = 1
    #             routes = self.add_to_route(ride_closest['ride'], last_ride, routes)
    #
    #     print(len(routes))
    #     for route in routes:
    #         print(len(route.ordered_rides), end=":")
    #         for ordered_ride in route.ordered_rides:
    #             print(ordered_ride.ride_id, end=",")
    #         print()
    #     print(routes[0].ordered_rides)

    def add_to_route(self, ride, next_ride, routes):
        for route in routes:
            start_ride = route.ordered_rides[0]
            end_ride = route.ordered_rides[-1]

            if start_ride is next_ride:
                route.ordered_rides.insert(0, ride)
                return routes
            elif end_ride is ride:
                route.ordered_rides.insert(-1, next_ride)
                return routes

        routes.append(Route([ride, next_ride]))
        return routes

    def get_next_ride(self, car, rides, actual_start_time):
        # unassigned_rides = deepcopy(self.get_unassigned_rides())
        best_ride = None
        waiting = 0 
        for unassigned_ride in rides:
            distance_to_next_ride = calculate_distance(car.row, unassigned_ride.row_start, car.col, unassigned_ride.col_start)
            time_to_new_start = actual_start_time + distance_to_next_ride
            if time_to_new_start + unassigned_ride.distance <= unassigned_ride.latest_finish:
                temp_waiting = max(unassigned_ride.earliest_start - (time_to_new_start + unassigned_ride.distance), 0)
                if(best_ride is None or waiting > temp_waiting):
                    waiting = temp_waiting
                    best_ride = unassigned_ride
        return best_ride


if __name__ == '__main__':
    file_names = [
        'a_example.in',
        'b_should_be_easy.in',
        'c_no_hurry.in',
        'd_metropolis.in',
        'e_high_bonus.in'
    ]
    for file_name in file_names:
        print('Running: {}\n'.format(file_name))
        input_parser = Input(file_name)
        input_parser.read_file()
        p = Process(input_data=input_parser, debug=False)
        p.run()
