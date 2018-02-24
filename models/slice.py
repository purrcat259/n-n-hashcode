
class Slice:
    def __init__(self, top_left, rows, columns):
        self.rows = rows
        self.columns = columns
        self.top_left = top_left
        self.tomato = 0
        self.mushroom = 0

    def addMushroom(self):
        self.mushroom++

    def addTomato(self):
        self.tomato++
