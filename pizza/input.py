import os


current_directory = os.path.dirname(os.path.realpath(__file__))


class Input:
    def __init__(self, filename):
        self._filename = filename
        self._file_path = os.path.join(current_directory, 'data', self._filename)
        self._data = []
        self._rows = 0
        self._columns = 0
        self._minimum_ingredient = 0
        self._maximum_cells = 0

    def read_file(self):
        with open(self._file_path, 'r') as input_file:
            data = input_file.readlines()
            # first line is the parameters so pop it off
            params = data.pop(0).replace('\n', '').split(' ')
            self._rows, self._columns, self._minimum_ingredient, self._maximum_cells = int(params[0]), int(params[1]), int(params[2]), int(params[3])
            for line in data:
                self._data.append(list(line.replace('\n', '')))

    @property
    def data(self):
        return self._data

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def minimum_ingredient(self):
        return self._minimum_ingredient

    @property
    def maximum_cells(self):
        return self._maximum_cells


class ExampleInput(Input):
    def __init__(self):
        super().__init__(filename='example.in')


class SmallInput(Input):
    def __init__(self):
        super().__init__(filename='small.in')


class MediumInput(Input):
    def __init__(self):
        super().__init__(filename='medium.in')


class BigInput(Input):
    def __init__(self):
        super().__init__(filename='big.in')


# Testing on the example file
if __name__ == '__main__':
    input_parser = Input(filename='example.in')
    input_parser.read_file()
    assert 3 == input_parser.rows
    assert 5 == input_parser.columns
    assert 1 == input_parser.minimum_ingredient
    assert 6 == input_parser.maximum_cells
    print(input_parser.data)
    example_input = ExampleInput()
    example_input.read_file()
    assert 3 == example_input.rows
    assert 5 == example_input.columns
    assert 1 == example_input.minimum_ingredient
    assert 6 == example_input.maximum_cells
    print(example_input.data)
    assert input_parser.data == example_input.data
