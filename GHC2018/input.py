import os

from models.ride import Ride

current_directory = os.path.dirname(os.path.realpath(__file__))


class Input:
    def __init__(self, filename):
        self._filename = filename
        self.file_path = os.path.join(current_directory, 'data', self._filename)
        self.rides = []

    def read_file(self):
        with open(self.file_path, 'r') as input_file:
            data = input_file.readlines()
            # first line is the parameters so pop it off
            params = data.pop(0).replace('\n', '').split(' ')
            self.rows, self.columns, self.vehicle_count, self.ride_count, self.on_time_bonus, self.sim_steps = int(params[0]), int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5])
            counter = 0
            for line in data:
                parsed_line = line.replace('\n', '').split(' ')
                ride = Ride(
                    ride_id=counter,
                    row_start=int(parsed_line[0]),
                    col_start=int(parsed_line[1]),
                    row_end=int(parsed_line[2]),
                    col_end=int(parsed_line[3]),
                    earliest_start=int(parsed_line[4]),
                    latest_finish=int(parsed_line[5])
                )
                self.rides.append(ride)
                counter += 1


class ExampleInput(Input):
    def __init__(self):
        super().__init__(filename='a_example.in')


class SmallInput(Input):
    def __init__(self):
        super().__init__(filename='small.in')


class MediumInput(Input):
    def __init__(self):
        super().__init__(filename='medium.in')


class BigInput(Input):
    def __init__(self):
        super().__init__(filename='big.in')


# Testing on the example file
if __name__ == '__main__':
    input_parser = Input(filename='a_example.in')
    input_parser.read_file()
    print(input_parser.rows)
    print(input_parser.columns)
    print(input_parser.vehicle_count)
    print(input_parser.ride_count)
    print(input_parser.on_time_bonus)
    print(input_parser.sim_steps)

