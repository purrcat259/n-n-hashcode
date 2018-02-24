from input import ExampleInput, SmallInput, MediumInput, BigInput

from output import Output

from slice import Slice

class Process:
    def __init__(self, input_data):
        self.max_cells = input_data.maximum_cells
        self.min_ing = input_data.minimum_ingredient

        self.pizza_rows = input_data.rows
        self.pizza_cols = input_data.columns

        self.data = input_data.data
        self.slices = []

        self.init()

    def init(self):
        self.slices.append(Slice([0,0]))    

    

    def validateSlice(self, slice, slices):
        


if __name__ == '__main__':
    pass
