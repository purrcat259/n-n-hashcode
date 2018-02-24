from input import ExampleInput, SmallInput, MediumInput, BigInput

from output import Output


class Process:
    def __init__(self, input_data):
        self.max_cells = input_data.maximum_cells
        self.min_ing = input_data.minimum_ingredient

        self.pizza_rows = input_data.rows
        self.pizza_cols = input_data.columns

        self.data = input_data.data
        self.slices = []

    def grow_slice(self, slice):
        while self._is_below_minimum_ingredients(slice) and not self.is_too_big(slice) and not self.overlap_exists(slice);
            c_slice = slice.growCol(self.data)
            if slice_is_valid(c_slice):
                self.slices.append(slice)
                return
            else:
            r_slice = slice.growRow(self.data)
            if slice_is_valid(r_slice):

            else:
                b_slice = r_slice.growCol(self.data)


        if slice_is_valid(slice):
            self.slices.append(slice)

    def slice_is_valid(self, slice):
<<<<<<< HEAD
        return not self.is_below_minimum_ingredients(slice) and
           not self.is_too_big(slice) and
           not self.overlap_exists(slice)
=======
        return self.is_below_minimum_ingredients(slice) and not self.is_too_big(slice) and not self.overlap_exists(slice)
>>>>>>> 363387ced82ceab1d63eb5f9b329d69bc06139f5

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


if __name__ == '__main__':
    pass
