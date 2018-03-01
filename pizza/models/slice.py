
class Slice:
    def __init__(self, data, top_left, rows=1, columns=1):
        self.rows = rows
        self.columns = columns
        self.top_left = top_left
        self.tomato = 0
        self.mushroom = 0
        
        self.init(data)

    def init(self, data):
        for row in range(self.top_left[0], self.top_left[0] + self.rows):
            for col in range(self.top_left[1], self.top_left[1] + self.columns):
                self.addIngredient(data, row, col)

    def grow(self, data, dir):
        if dir == 0:
            return self.growRow(data)
        elif dir == 1:
            return self.growCol(data)

    def growRow(self, data):
        t_row = self.top_left[0] + self.rows - 1 + 1
        r_col = self.top_left[1] + self.columns

        for cell_col in range(self.top_left[1], r_col):
            self.addIngredient(data, t_row, cell_col)

        self.rows += 1

    def growCol(self, data):
        br_row = self.top_left[0] + self.rows
        t_col = self.top_left[1] + self.columns - 1 + 1

        for cell_row in range(self.top_left[0], br_row):
            self.addIngredient(data, cell_row, t_col)
            
        self.columns += 1
    
    def growBoth(self, data):
        self.grow(data, 0)
        self.grow(data, 1)

    def addIngredient(self, data, row, col):
        ing = data[row][col]
        if ing == "M":
            self.addMushroom()
        else:
            self.addTomato()

    def addMushroom(self):
        self.mushroom += 1

    def addTomato(self):
        self.tomato += 1

    def size(self):
        return self.rows * self.columns
