from process import Process
from input import ExampleInput
from models.slice import Slice


"""
TTTTT
TMMMT
TTTTT
"""

example_input = ExampleInput()
example_input.read_file()

data = example_input.data


class TestSliceOverlap:
    s = None
    p = None

    def setup_method(self):
        self.s = Slice(data, (0, 2), 2, 1)
        self.p = Process(example_input)

    def test_only_two_tomatoes(self):
        assert False is self.p.slice_is_valid(self.s)

