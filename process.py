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
        print('Maximum Slice Size: ', self.max_cells)
        print('Minimum Ingredient Count: ', self.min_ing)
        print('Pizza Size: {} by {}'.format(self.pizza_rows, self.pizza_cols))
        positions_stack = [(0, 0)]
        i = 0
        while not len(positions_stack) == 0:
            i += 1
            top_left = positions_stack.pop()
            print('{}/{}'.format(i, iterations))
            # Initialise a slice
            print('Starting from: {}'.format(top_left))
            slice = Slice(self.data, top_left)
            # grow a slice
            was_valid = self.grow_valid_slice(slice)
            self.print()
            if was_valid:
                print('Added slice from: {},{} with {} rows and {} columns'.format(slice.top_left[0], slice.top_left[1], slice.rows, slice.columns))
                # Search for a new starting position
                # Try just to the left
                new_top_left = (slice.top_left[0] + slice.rows - 1, slice.top_left[1] + slice.columns - 1 + 1)
                # if it is invalid, keep searching
                if self.is_out_of_bounds(new_top_left[0], new_top_left[1]):
                    self.search_for_new_starting_position(new_top_left)
                positions_stack.append(new_top_left)
            else:
                print('Slice: {},{} with {} rows and {} columns was not valid'.format(slice.top_left[0], slice.top_left[1], slice.rows, slice.columns))
                new_top_left = (slice.top_left[0] + slice.rows - 1, slice.top_left[1] + slice.columns - 1 + 1)
                # if it is invalid, keep searching
                if self.is_out_of_bounds(new_top_left[0], new_top_left[1]):
                    self.search_for_new_starting_position(new_top_left)
                positions_stack.append(new_top_left)

    def search_for_new_starting_position(self, top_left):
        new_top_left = (top_left[0], top_left[1])
        # if it is invalid, keep searching
        while self.is_out_of_bounds(new_top_left[0], new_top_left[1]):
            print('Searching for new valid start position')
            # if we fall off the right side...
            if new_top_left[1] >= self.pizza_cols:
                # go down to the start of the next row
                new_top_left = (new_top_left[0] + 1, 0)
        return new_top_left

    def is_out_of_bounds(self, r, c):
        return c >= self.pizza_cols or r >= self.pizza_rows

    def grow_valid_slice(self, slice):
        print('Attempting to grow valid slice')
        while self.slice_can_grow(slice):
            r_slice = deepcopy(slice)
            # C_SLICE
            beyond_column_limits = slice.top_left[1] + slice.columns >= self.pizza_cols
            if not beyond_column_limits:
                print('COL.', end='')
                slice.growCol(self.data)
                if self.slice_is_valid(slice):
                    self.add_slice(slice)
                    return True
            beyond_row_limits = r_slice.top_left[0] + r_slice.rows >= self.pizza_rows
            if not beyond_row_limits:
                print('ROW.', end='')
                r_slice.growRow(self.data)
                if self.slice_is_valid(r_slice):
                    self.add_slice(r_slice)
                    return True
            if not beyond_column_limits and not beyond_row_limits:
                print('BOTH.', end='')
                slice.growRow(self.data)
                if self.slice_is_valid(slice):
                    self.add_slice(slice)
                    return True
        print()
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
    # example_input = ExampleInput()
    # example_input.read_file()
    # p = Process(example_input)
    # small_input = SmallInput()
    # small_input.read_file()
    # p = Process(small_input)
    medium_input = MediumInput()
    medium_input.read_file()
    p = Process(medium_input)
    p.run()

