class Move:
    def __init__(self, src_cell, dest_cell, change):
        self.__src_cell = src_cell  # Cell object
        self.__dest_cell = dest_cell  # Cell object
        self.__change = change  # Change object

    def __str__(self):
        src_x = self.__src_cell.x
        src_y = self.__src_cell.y
        dest_x = self.__dest_cell.x
        dest_y = self.__dest_cell.y
        return f"({src_x}, {src_y}) -> ({dest_x}, {dest_y})"

    @property
    def src_cell(self):
        return self.__src_cell

    @property
    def dest_cell(self):
        return self.__dest_cell

    @property
    def change(self):
        return self.__change

    def parse_for_socket(self):
        x1 = self.__src_cell.x
        y1 = self.__src_cell.y
        x2 = self.__dest_cell.x
        y2 = self.__dest_cell.y
        moving_group_size = self.__change.value
        return x1, y1, moving_group_size, x2, y2
