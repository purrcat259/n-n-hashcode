from GHC2018.input import ExampleInput, MediumInput, SmallInput, BigInput
from GHC2018.models.Car import Car
from GHC2018.models.Route import Route
from GHC2018.models.ride import calculate_distance

from copy import deepcopy


class Process:
    def __init__(self, input_data, debug=True):
        self.input_data = input_data
        self.debug = debug
        self.current_time = 0
        self.initialise_cars()
        self.cars = []
        self.rides = input_data.rides

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
        for i in range(0, self.input_data.sim_steps):
            print('--- STEP {} ---'.format(i))
            self.current_time = i
            # if cars are at their destination, end the ride
            self.end_rides()
            # schedule any cars that are not assigned a ride
            self.schedule_rides()
            # move any cars
            self.move_cars()

    def end_rides(self):
        self.debug_print('Checking if cars have arrived')
        completed_cars = [
            car for car in self.get_assigned_cars() if car.is_at_destination()
        ]
        self.debug_print('{} cars completed their ride this turn'.format(len(completed_cars)))
        for car in completed_cars:
            car.complete()
            car.assigned_ride.complete()
            self.debug_print('{}/{} rides completed'.format(
                len(self.get_completed_rides()),
                len(self.rides)
            ))

    def get_completed_rides(self):
        return [ride for ride in self.input_data.rides if ride.completed]

    def schedule_rides(self):
        unassigned_cars = self.get_unassigned_cars()
        unassigned_rides = self.get_unassigned_rides()
        for car in unassigned_cars:
            next_ride = unassigned_rides.pop(0)
            rides_for_route = [next_ride]
            if not len(unassigned_rides) == 0:
                closest_next_ride = self.get_next_closest_rides(next_ride, self.current_time)[0]
                self.debug_print('Closest ride to {} is {}'.format(next_ride.ride_id, closest_next_ride.ride_id))
                unassigned_rides.pop(unassigned_rides.index(closest_next_ride))
                rides_for_route.append(closest_next_ride)
            route = Route(rides_for_route)
            self.debug_print('Assigned route with ride IDs {} to car: {}'.format(
                route.get_route_ride_ids(),
                car.car_id
            ))
            car.assign_route(route)

    def move_cars(self):
        for car in self.get_assigned_cars():
            self.debug_print('Moving car with ID: {}'.format(car.car_id))
            car.move_towards_destination()

    def get_assigned_cars(self):
        return [car for car in self.cars if car.assigned_route is not None]

    def get_unassigned_cars(self):
        return [car for car in self.cars if car.assigned_route is None]

    def get_unassigned_rides(self):
        return [ride for ride in self.input_data.rides if ride.assigned_car == -1]

    def get_next_closest_rides(self, ride, actual_start_time):
        # unassigned_rides = deepcopy(self.get_unassigned_rides())
        unassigned_rides = self.get_unassigned_rides()
        possible_best_rides = []
        for unassigned_ride in unassigned_rides:
            if ride == unassigned_rides:
                continue
            distance_to_next_ride = calculate_distance(ride.row_end, unassigned_ride.row_start, ride.col_end, unassigned_ride.col_start)
            full_distance = distance_to_next_ride + ride.distance
            time_to_new_start = actual_start_time + full_distance
            if time_to_new_start >= unassigned_ride.earliest_start:
                if time_to_new_start + unassigned_ride.distance <= unassigned_ride.latest_finish:
                    possible_best_rides.append(unassigned_ride)
        return possible_best_rides


if __name__ == '__main__':
    example_input = ExampleInput()
    example_input.read_file()
    p = Process(example_input)
    p.run()
    #
    # small_input = SmallInput()
    # small_input.read_file()
    # p = Process(small_input)
    # p.run()
    #
    # medium_input = MediumInput()
    # medium_input.read_file()
    # p = Process(medium_input)
    # p.run()
    #
    # big_input = BigInput()
    # big_input.read_file()
    # p = Process(big_input)
    # p.run()
    #
