from input import ExampleInput, SmallInput, MediumInput, BigInput
from models.slice import Slice
from copy import deepcopy
from pprint import pprint
from output import Output


class Process:
    def __init__(self, input_data):
        self.max_cells = input_data.maximum_cells
        self.min_ing = input_data.minimum_ingredient

        self.pizza_rows = input_data.rows
        self.pizza_cols = input_data.columns

        self.data = input_data.data
        self.slices = []

    def run(self, iterations=1000):
        current_top_left = [0, 0]
        for i in range(iterations):
            print('{}/{}'.format(i, iterations))
            # Initialise a slice
            slice = Slice(self.data, current_top_left)
            # grow a slice
            self.grow_valid_slice(slice)
            self.print()

    def grow_valid_slice(self, slice):
        print('Growing valid slice')
        while self.is_below_minimum_ingredients(slice) and not self.is_too_big(slice) and not self.overlap_exists(slice):
            r_slice = deepcopy(slice)
            # C_SLICE
            slice.growCol(self.data)
            if self.slice_is_valid(slice):
                self.add_slice(slice)
                return
            r_slice.growRow(self.data)
            if self.slice_is_valid(r_slice):
                self.add_slice(slice)
                return
            slice.growRow(self.data)
            if self.slice_is_valid(r_slice):
                self.add_slice(r_slice)
                return

    def add_slice(self, slice):
        self.slices.append(slice)

    def slice_is_valid(self, slice):
        return self.is_below_minimum_ingredients(slice) and not self.is_too_big(slice) and not self.overlap_exists(slice)

    def overlap_exists(self, slice):
        br_sl_row = slice.top_left[0] + slice.rows - 1
        br_sl_col = slice.top_left[1] + slice.columns - 1
        for t_slice in self.slices:
            br_row = t_slice.top_left[0] + t_slice.rows - 1
            br_col = t_slice.top_left[1] + t_slice.columns - 1
            if self.is_point_in_area(slice.top_left, t_slice.top_left, [br_row, br_col]) or \
                    self.is_point_in_area([br_sl_row, br_sl_col], t_slice.top_left, [br_row, br_col]) or \
                    self.is_point_in_area(t_slice.top_left, slice.top_left, [br_sl_row, br_sl_col]) or \
                    self.is_point_in_area([br_row, br_col], slice.top_left, [br_sl_row, br_sl_col]):
                return True
        return False
#

    def is_point_in_area(self, coor, area_tl, area_br):
        return area_tl[0] <= coor[0] <= area_br[0] and area_tl[1] <= coor[1] <= area_br[1]

    def is_below_minimum_ingredients(self, slice):
        return slice.mushroom >= self.min_ing and slice.tomato >= self.min_ing

    def is_too_big(self, slice):
        return slice.size() <= self.max_cells

    def print(self):
        pizza = []
        for row in range(0, self.pizza_rows):
            row_list = []
            for col in range(0, self.pizza_cols):
                row_list.append('X')
            pizza.append(row_list)
        for i in range(0, len(self.slices)):
            slice = self.slices[i]
            for row in range(slice.top_left[0], slice.top_left[0] + slice.rows):
                for col in range(slice.top_left[1], slice.top_left[1] + slice.columns):
                    pizza[row][col] = str(i)
        pprint(pizza)


if __name__ == '__main__':
    example_input = ExampleInput()
    example_input.read_file()
    p = Process(example_input)
    p.run()
