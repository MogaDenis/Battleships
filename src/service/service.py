import random


class Service:
    def __init__(self, board):
        self.board = board

    def is_in_board(self, row, col):
        return self.board.is_in_board(row, col)

    def place_ship(self, list_of_indices):
        """
            This method calls the method inside the board class which places a ship on the board based on its given coordinates. 

        :param list_of_indices: List containing pairs of (column, row) indices.
        """

        self.board.place_ship(list_of_indices)

    def draw_board(self, hide=False):
        return self.board.draw_board(hide)

    def check_if_game_over(self):
        return self.board.check_if_game_over()

    def get_symbol(self, row, col):
        return self.board.get_symbol(row, col)

    def attack(self, row, col):
        return self.board.attack(row, col)

    def _generate_random_ship(self):
        direction = random.randint(0, 1)
        random_row = random.randint(1, self.board.size - 2)
        random_col = random.randint(1, self.board.size - 2)

        list_of_indices = []

        for value in [-1, 0, 1]:
            # Vertical
            if direction == 0:
                list_of_indices.append([random_col, random_row + value])
            # Horizontal
            elif direction == 1:
                list_of_indices.append([random_col + value, random_row])

        return list_of_indices

    def _check_overlapping(self, list_of_indices):
        for pair in list_of_indices:
            col, row = pair
            if self.board.get_symbol(row, col) != '.':
                return False

        return True

    def place_random_ships(self):
        # Let's place ships of length 3. 
        for _ in range(2):
            list_of_indices = self._generate_random_ship()

            while not self._check_overlapping(list_of_indices):
                list_of_indices = self._generate_random_ship()

            self.board.place_ship(list_of_indices)
