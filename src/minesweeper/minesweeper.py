from numpy.random import choice
from numpy import ravel
from numpy import array

from .spot import Spot


class Minesweeper:
    def __init__(self, n_cols: int, n_rows: int, start_col: int, start_row: int):
        self.field = [[Spot(col, row) for row in range(n_cols)]
                      for col in range(n_rows)]
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.n_spots = n_cols * n_rows
        self.start_pos = (start_col, start_row)

    def __str__(self) -> str:
        _str = "["
        for row in array(self.field).T:
            _str += ("[")
            for spot in row:
                _str += str(spot) + ", "
            _str = _str[:-2] + "], \n"
        _str = _str[:-3] + "]"
        return _str

    def place_mines(self, mines_to_place=None):
        """Makes a consistent minesweeper field that you can't lose in, on the first try. 1 of 6 spots in the field are mines.
        """

        def cut_three_by_three(field, col, row):
            """Cuts a three by three field out of self.field around the center coordinates col and row.

            Args:
                col (int): The index of the col of the center spot of which to cut around
                row (int): The index of the row of the center spot of which to cut around

            Returns:
                List[List]: The list of lists with the 3 by three cutout.
            """
            sliced = []
            sliced += field[:col-1]
            sliced += [field[col-1][:row-1] + field[col-1][row+2:]]
            sliced += [field[col][:row-1] + field[col][row+2:]]
            sliced += [field[col+1][:row-1] + field[col+1][row+2:]]
            sliced += field[col+2:]
            return sliced

        def flatten(field):
            """Converts a 2d array to a 1d array

            Args:
                field (List[List]): The 2d array that will be converted to a 1d array

            Returns:
                List: The 1d array made from the sub-lists of the 2d array
            """
            flat = []
            for col in field:
                flat += col
            return flat

        if mines_to_place in [None, 0, self.n_spots]:
            mines_to_place = round(self.n_spots/6)
        self.n_mines = mines_to_place

        mine_spots = choice(ravel(self.field), mines_to_place, replace=False)

        # cuts out the start spot and all neighboring squares to ensure that there is no mine there, which in turn
        # ensures the start spot to be a 0 to make a start possible.
        field_for_mines = cut_three_by_three(self.field, *self.start_pos)

        mine_spots = choice(flatten(field_for_mines),
                            mines_to_place, replace=False)

        for mine in mine_spots:
            col, row = mine.get_col_row()
            self.field[col][row].mine = True
            neighbors = [
                (col-1, row-1), (col, row-1), (col+1, row-1),
                (col-1, row),                 (col+1, row),
                (col-1, row+1), (col, row+1), (col+1, row+1)
            ]
            for n in neighbors:
                if 0 <= n[0] < self.n_rows and 0 <= n[1] < self.n_cols:
                    if self.field[n[0]][n[1]].mine == True:
                        continue

                    self.field[n[0]][n[1]].n_mines += 1
                    self.field[n[0]][n[1]].orig_n_mines += 1

    def reset_field(self):
        """Resets every Spot's number of mines and whether or not it is a mine
        """
        for row in self.field:
            for spot in row:
                spot.n_mines = 0
                spot.orig_n_mines = 0
                spot.mine = False

    def test_solver(self):
        """Used to test wether or not a board is solvable purely by logic.
        The solver treats Minesweeper as a constraint satisfaction problem with depth first search to open all fields that have no mines as neighbors
        """
        moves = []
        spots_to_probe = []

    def get_spots(self):
        spots = []
        for row in self.field:
            for spot in row:
                spots.append(spot.get_col_row())
        return spots


if __name__ == "__main__":
    ms = Minesweeper(5, 5, 1, 1)
    ms.place_mines()
    print(ms)
    for row in ms.field:
        for spot in row:
            print(spot.mine)
