from domain.board import Board, OverlappingShipsException
from service.service import Service
import random


class InvalidInputException(Exception):
    pass


class ConsoleUI:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.player_service = Service(self.player_board)
        self.computer_service = Service(self.computer_board)
        self.game_started = False
        self.game_over = False
        self.winner = None
        self.active_cheat = False

    def letter_coordinate_to_indices(self, letter):
        return int(ord(letter) - ord('A'))

    def read_user_command(self):
        command = input("\n>> ").strip()

        tokens = command.split()

        if len(tokens) == 0:
            raise InvalidInputException

        if tokens[0] not in ['cheat', 'start', 'ship', 'attack']:
            raise InvalidInputException

        if tokens[0].lower() in ['cheat', 'start']:
            if len(tokens) != 1:
                raise InvalidInputException

        if tokens[0].lower() == 'ship':
            if len(tokens) != 2:
                raise InvalidInputException

            # tokens[1] == the coordinates of the ship. 
            tokens[1] = tokens[1].upper()

            if len(tokens[1]) % 2 != 0:
                raise InvalidInputException

            for i in range(len(tokens[1])):
                if i % 2 == 0:
                    if tokens[1][i] not in ['A', 'B', 'C', 'D', 'E', 'F']:
                        raise InvalidInputException
                else:
                    if not tokens[1][i].isnumeric() or int(tokens[1][i]) < 0 or int(tokens[1][i]) >= self.player_board.size:
                        raise InvalidInputException

            list_of_indices = []
            for i in range(0, len(tokens[1]) - 1, 2):
                pair = []
                pair.append(self.letter_coordinate_to_indices(tokens[1][i]))
                pair.append(int(tokens[1][i + 1]))
                list_of_indices.append(pair)

            for i in range(0, len(list_of_indices) - 1):
                first_pair = list_of_indices[i]
                second_pair = list_of_indices[i + 1]
                if abs(first_pair[0] - second_pair[0]) > 1 or abs(first_pair[1] - second_pair[1]) > 1:
                    raise InvalidInputException

        if tokens[0].lower() == 'attack':
            if len(tokens) != 2:
                raise InvalidInputException

            tokens[1] = tokens[1].upper()

            if tokens[1][0] not in ['A', 'B', 'C', 'D', 'E', 'F'] or not tokens[1][1].isnumeric() or int(tokens[1][1]) < 0 or int(tokens[1][1]) >= self.player_board.size:
                raise InvalidInputException

        return tokens

    def start(self):
        while True:
            if not self.game_started:
                print("\n\tPlayer board:")
                print(self.player_service.draw_board())
            else:
                print("\n\tPlayer board:")
                print(self.player_service.draw_board())
                print("\n\tComputer board:")
                print(self.computer_service.draw_board(hide=not self.active_cheat))

            if self.game_over:
                break

            while True:
                try:
                    tokens = self.read_user_command()
                    break
                except InvalidInputException:
                    print("\nInvalid input!\n")

            if tokens[0] == 'cheat':
                if self.game_started:
                    self.active_cheat = True
                else:
                    print("\nBruh. The game didn't even start yet!\n")

            elif tokens[0] == 'start':
                if self.player_board.ships_count == 2:
                    self.game_started = True
                    self.computer_service.place_random_ships()
                else:
                    print("\nNot enough ships placed on the board!\n")

            elif tokens[0] == 'ship':
                if not self.game_started:
                    list_of_indices = []
                    for i in range(0, len(tokens[1]) - 1, 2):
                        pair = []
                        pair.append(self.letter_coordinate_to_indices(tokens[1][i]))
                        pair.append(int(tokens[1][i + 1]))
                        list_of_indices.append(pair)

                    try:
                        self.player_service.place_ship(list_of_indices)
                    except OverlappingShipsException:
                        print("\nOverlapping ships!\n")
                else:
                    print("\nYou can't place ships anymore!\n")

            elif tokens[0] == 'attack':
                if not self.game_started:
                    print("\nBruh. The game didn't even start yet!\n")
                else:
                    # The player attacks, then the computer. 
                    col = self.letter_coordinate_to_indices(tokens[1][0])
                    row = int(tokens[1][1])
                    
                    # The user attacks the computer's board.
                    player_hit = self.computer_service.attack(row, col)

                    if player_hit:
                        print("\nPlayer hits!\n")
                    else:
                        print("\nPlayer misses!\n")

                    if not self.computer_service.check_if_game_over():
                        row = random.randint(0, self.player_board.size - 1)
                        col = random.randint(0, self.player_board.size - 1)

                        # The computer attacks the player's board. 
                        computer_hit = self.player_service.attack(row, col)

                        print(f"Computer attacks {chr(ord('A') + col)}{row}.")
                        if computer_hit == True:
                            print("Computer hits!\n")
                        else:
                            print("Computer misses!\n")

                        if self.player_service.check_if_game_over():
                            self.game_over = True
                            self.winner = 'computer'

                    else:
                        self.game_over = True
                        self.winner = 'player'

        if self.winner == 'player':
            print("\n\tCongratulations! You won!\n")
        else:
            print("\n\tReally? The computer won!\n")
