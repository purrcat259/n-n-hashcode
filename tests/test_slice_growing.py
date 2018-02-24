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


class TestSliceGrowing:
    s = None

    def setup_method(self):
        self.s = Slice(data, (0, 0))

    def test_grow_row(self):
        assert 1 == self.s.size()
        assert 1 == self.s.tomato
        assert 0 == self.s.mushroom
        self.s.growRow(data)
        assert 2 == self.s.size()
        assert 2 == self.s.tomato
        assert 0 == self.s.mushroom
        self.s.growRow(data)
        assert 3 == self.s.size()
        assert 3 == self.s.tomato
        assert 0 == self.s.mushroom

    def test_grow_column(self):
        assert 1 == self.s.size()
        assert 1 == self.s.tomato
        assert 0 == self.s.mushroom
        self.s.growCol(data)
        assert 2 == self.s.size()
        assert 2 == self.s.tomato
        assert 0 == self.s.mushroom
        self.s.growCol(data)
        assert 3 == self.s.size()
        assert 3 == self.s.tomato
        assert 0 == self.s.mushroom

    def test_grow_both(self):
        assert 1 == self.s.size()
        assert 1 == self.s.tomato
        assert 0 == self.s.mushroom
        self.s.growBoth(data)
        assert 4 == self.s.size()
        assert 3 == self.s.tomato
        assert 1 == self.s.mushroom
        self.s.growBoth(data)
        assert 9 == self.s.size()
        assert 7 == self.s.tomato
        assert 2 == self.s.mushroom
