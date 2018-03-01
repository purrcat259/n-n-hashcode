from GHC2018.input import ExampleInput, MediumInput, SmallInput, BigInput


class Process:
    def __init__(self, input_data):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    example_input = ExampleInput()
    example_input.read_file()
    p = Process(example_input)
    p.run()
    #
    # small_input = SmallInput()
    # small_input.read_file()
    # p = Process(small_input)
    # p.run()
    #
    # medium_input = MediumInput()
    # medium_input.read_file()
    # p = Process(medium_input)
    # p.run()
    #
    # big_input = BigInput()
    # big_input.read_file()
    # p = Process(big_input)
    # p.run()
    #
