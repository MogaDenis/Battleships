import texttable


class OverlappingShipsException(Exception):
    pass


class Board:
    def __init__(self):
        self._size = 6 
        self._board = self._create_board()
        self._ships_count = 0
        self._ships_coordinates = []

    @property
    def size(self):
        return self._size

    @property
    def board(self):
        return self._board

    @property
    def ships_count(self):
        return self._ships_count

    @ships_count.setter
    def ships_count(self, new_value):
        self._ships_count = new_value

    def check_if_game_over(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.get_symbol(row, col) == '+':
                    return False

        return True

    def attack(self, row, col):
        if self.get_symbol(row, col) != '+':
            self.board[row][col] = 'o'
            return False 
        
        else:
            self.board[row][col] = 'X'
            return True

    def get_symbol(self, row, col):
        return self.board[row][col]

    def place_ship(self, list_of_indices):
        """
            This method places a ship on the game board. If there are already two ships and the user adds a third one, the oldest one gets replaced.

        :param list_of_indices: List containing pairs of (column, row) indices.
        :raises OverlappingShipsException: Exception raised if the current ship overlaps with a ship that already exists. 
        """

        # A pair is given as (col, row)
        for pair in list_of_indices:
            col, row = pair
            if self.get_symbol(row, col) != '.':
                raise OverlappingShipsException

        for pair in list_of_indices:
            col, row = pair
            self.board[row][col] = '+'

        self._ships_coordinates.append(list_of_indices)
        self.ships_count += 1
        if self.ships_count == 3:
            self._remove_ship(self._ships_coordinates.pop(0)) 
            self.ships_count -= 1

    def _remove_ship(self, list_of_indices):
        """
            This method removes a ship from the board given by its indices, in case the number of ships exceeds 2. 

        :param list_of_indices: List containing pairs of (column, row) indices.
        """

        for pair in list_of_indices:
            col, row = pair
            self.board[row][col] = '.'

    def is_in_board(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        return True

    def _create_board(self):
        board = []

        for _ in range(self.size):
            row = []
            for _ in range(self.size):
                row.append('.')

            board.append(row)

        return board

    def draw_board(self, hide=False):
        board = texttable.Texttable()
        header = ['/', 'A', 'B', 'C', 'D', 'E', 'F']

        board.header(header)

        for i in range(self.size):
            row = [i]
            for j in range(self.size):
                if self.get_symbol(i, j) == 'X':
                    row.append('X')
                elif hide and self.get_symbol(i, j) == 'o':
                    row.append('o')
                elif hide:
                    row.append('.')
                else:
                    row.append(self.get_symbol(i, j))

            board.add_row(row)

        return board.draw()
