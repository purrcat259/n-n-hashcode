from input import ExampleInput

from pizza.models.slice import Slice
from pizza.process import Process

"""
TTTTT
TMMMT
TTTTT
"""

example_input = ExampleInput()
example_input.read_file()

data = example_input.data


class TestSliceOverlap:
    p = None

    def setup_method(self):
        self.p = Process(example_input)

    def test_returns_false_on_adjacent_slices(self):
        self.p.slices.append(Slice(data, (0, 0)))
        assert False is self.p.overlap_exists(Slice(data, (1, 1)))

    def test_returns_true_on_overlapping_slices(self):
        self.p.slices.append(Slice(data, (0, 0), 2, 2))
        assert True is self.p.overlap_exists(Slice(data, (1, 1)))
