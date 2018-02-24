from input import ExampleInput, SmallInput, MediumInput, BigInput

from output import Output


class Process:
    def main(self, rows, columns, minIng, maxCells, data):
        self.max_cells = maxCells
        self.pizza_rows = rows
        self.pizza_cols = columns

    def sliceIt(leftPnt):
        m = 0
        t = 0

    def grow(slice, dir):
        if(dir == 0):
            t_row = slice.top_left[0] + slice.rows + 1
            r_col = slice.top_left[1] + slice.cols

            for cell_col in range(top_left[1], r_col)
                addIngredient(slice, data[t_row][cell_col])        
        else if(dir == 1):
            br_row = slice.top_left[0] + slice.rows
            t_col = slice.top_left[1] + slice.cols + 1

            for cell_row in range(top_left[0], br_row)
                addIngredient(slice, data[cell_row][t_col])

        return slice

    def addIngredient(slice,ing):
        if(ing == "M"):
            slice.addMushroom(1)
        else if(ing == "T")
            slice.addTomato(1)    

    def validateSlice(slice, slices):
        


if __name__ == '__main__':
    pass
