from GHC2018.input import ExampleInput
from GHC2018.process import Process

example_input = ExampleInput()
example_input.read_file()
p = Process(example_input)
first_ride = p.input_data.rides[0]
print(p.get_next_possible_rides(first_ride, 0)[0].ride_id)


