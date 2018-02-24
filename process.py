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
        positions_stack = [(0, 0)]
        i = 0
        while not len(positions_stack) == 0:
            i += 1
            top_left = positions_stack.pop(-1)
            print('{}/{}'.format(i, iterations))
            # Initialise a slice
            print('Starting from: {}'.format(top_left))
            slice = Slice(self.data, top_left)
            # grow a slice
            was_valid = self.grow_valid_slice(slice)
            # self.print()
            if was_valid:
                # add new possible starting positions
                max_new_bottom = slice.top_left[0] + slice.rows
                max_new_right = slice.top_left[1] + slice.columns
                if max_new_bottom <= self.pizza_rows and max_new_right <= self.pizza_cols:
                    positions_stack.append((max_new_bottom, max_new_right))
                if max_new_bottom <= self.pizza_rows:
                    positions_stack.append((max_new_bottom, slice.top_left[1]))
                if max_new_right <= self.pizza_cols:
                    positions_stack.append((slice.top_left[0], max_new_right))
                print('Stack Size: {}'.format(len(positions_stack)))


    def grow_valid_slice(self, slice):
        print('Attempting to grow valid slice')
        while self.slice_can_grow(slice):
            r_slice = deepcopy(slice)
            # C_SLICE
            beyond_column_limits = slice.top_left[1] + slice.columns >= self.pizza_cols
            if not beyond_column_limits:
                print('Growing by Column')
                slice.growCol(self.data)
                if self.slice_is_valid(slice):
                    self.add_slice(slice)
                    return True
            beyond_row_limits = r_slice.top_left[0] + r_slice.rows >= self.pizza_rows
            if not beyond_row_limits:
                print('Growing by row')
                r_slice.growRow(self.data)
                if self.slice_is_valid(r_slice):
                    self.add_slice(r_slice)
                    return True
            if not beyond_column_limits and not beyond_row_limits:
                print('Growing by both')
                slice.growRow(self.data)
                if self.slice_is_valid(slice):
                    self.add_slice(slice)
                    return True
        return False

    def slice_can_grow(self, slice):
        return self.is_below_minimum_ingredients(slice) and not self.is_too_big(slice) and not self.overlap_exists(
            slice)

    def add_slice(self, slice):
        self.slices.append(slice)

    def slice_is_valid(self, slice):
        return self.has_minimum_ingredients(slice) and not self.is_too_big(slice) and not self.overlap_exists(slice)

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
        return slice.mushroom < self.min_ing or slice.tomato < self.min_ing

    def has_minimum_ingredients(self, slice):
        return slice.mushroom >= self.min_ing and slice.tomato >= self.min_ing

    def is_too_big(self, slice):
        return slice.size() > self.max_cells

    def print(self):
        print('{} valid slices present'.format(len(self.slices)))
        pizza = []
        for row in range(0, self.pizza_rows):
            row_list = []
            for col in range(0, self.pizza_cols):
                row_list.append(self.data[row][col])
            pizza.append(row_list)
        for i in range(0, len(self.slices)):
            slice = self.slices[i]
            for row in range(slice.top_left[0], slice.top_left[0] + slice.rows):
                for col in range(slice.top_left[1], slice.top_left[1] + slice.columns):
                    pizza[row][col] = str(i)
        for row in range(0, self.pizza_rows):
            for col in range(0, self.pizza_cols):
                print('{}{}, '.format(pizza[row][col], pizza[row][col]), end='')
            print()


if __name__ == '__main__':
    example_input = ExampleInput()
    medium_input = MediumInput()
    # example_input.read_file()
    medium_input.read_file()
    # p = Process(example_input)
    p = Process(medium_input)
    p.run()

