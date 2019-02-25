class Move:
    def __init__(self, src_cell, dest_cell, change):
        self.__src_cell = src_cell # Cell object
        self.__dest_cell = dest_cell # Cell object
        self.__change = change # Change object

    @property
    def src_cell(self):
        return self.__src_cell

    @property
    def dest_cell(self):
        return self.__dest_cell

    @property
    def change(self):
        return self.__change
