from GHC2018.input import ExampleInput, MediumInput, SmallInput, BigInput
from GHC2018.models.ride import calculate_distance

from copy import deepcopy


class Process:
    def __init__(self, input_data):
        self.input_data = input_data
        self.current_time = 0

    def run(self):
        for i in range(0 , self.input_data.sim_steps):
            print('--- STEP {} ---'.format(i))
            self.current_time = i

    def get_unassigned_rides(self):
        return [ride for ride in self.input_data.rides if ride.assigned_car == -1]

    

    def get_next_closest_rides(self, ride, actual_start_time):
        unassigned_rides = deepcopy(self.get_unassigned_rides())
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
