from input import Input, ExampleInput, MediumInput, SmallInput, BigInput
from models.ride import calculate_distance
from models.Route import Route

from copy import deepcopy


class Process:
    def __init__(self, input_data):
        self.input_data = input_data
        self.current_time = 0
        self.get_routes()

    def run(self):
        for i in range(0 , self.input_data.sim_steps):
            self.current_time = i

    def get_unassigned_rides(self):
        return [ride for ride in self.input_data.rides if ride.assigned_car == -1]

    def set_next_routes(self, route, routes):
        for t_route in routes:
            if not t_route is route:
                wait = t_route.ordered_rides[0].earliest_start -route.ordered_rides[-1].latest_finish
                if wait >= 0:
                    route.next_routes.append({'route':t_route, 'wait_time': wait}) 
            

    def get_routes(self):
        routes = []
        rides_closests = []

        for ride in self.input_data.rides:
            rides = self.get_next_closest_rides(ride, ride.earliest_start)
            rides_closests.append({'ride': ride, 'rides': rides})

        rides_closests = sorted(rides_closests, key=lambda k: len(k['rides']), reverse=True)
        print(rides_closests)
        for ride_closest in rides_closests:
            last_ride = None
            while last_ride is None and len(ride_closest['rides']) > 0:
                temp_ride = ride_closest['rides'].pop()
                if(temp_ride.assigned_car is None):
                    last_ride = temp_ride
            if not last_ride is None:
                last_ride.assigned_car = 1
                ride_closest['ride'].assigned_car = 1
                routes = self.add_to_route(ride_closest['ride'], last_ride, routes)
        
        print(len(routes))
        for route in routes:
            print(len(route.ordered_rides), end=":")
            for ordered_ride in route.ordered_rides:
                print(ordered_ride.ride_id, end=",")
            print()
        print(routes[0].ordered_rides)

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

    def get_next_closest_rides(self, ride, actual_start_time):
        unassigned_rides = self.input_data.rides
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
    example_input = Input(filename='c_no_hurry.in')
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
