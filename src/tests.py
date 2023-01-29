import unittest
from domain.board import Board, OverlappingShipsException
from service.service import Service


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_place_ship(self):
        # The board is empty, we can place a ship anywhere. 
        self.board.place_ship([(1,2), (1,3)])

        # Check if the positions are occupied. 
        self.assertEqual('+', self.board.get_symbol(2, 1))
        self.assertEqual('+', self.board.get_symbol(3, 1))

        # Now let's try adding a ship over the same one. An Exception should be raised.  
        self.assertRaises(OverlappingShipsException, self.board.place_ship, [(1,1), (1,2)])

        # Now let's add a second ship. 
        self.board.place_ship([(3,4), (4,4)])

        # When we add the third ship, the first one should be replaced.
        self.board.place_ship([(5,5), (5,4)])

        # Check if the positions are freed. 
        self.assertEqual('.', self.board.get_symbol(2, 1))
        self.assertEqual('.', self.board.get_symbol(3, 1))

        # Check if the second ship still exists. 
        self.assertEqual('+', self.board.get_symbol(4, 3))
        self.assertEqual('+', self.board.get_symbol(4, 4))


class TestService(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.service = Service(self.board)

    def test_place_ship(self):
        # The board is empty, we can place a ship anywhere. 
        self.service.place_ship([(1,2), (1,3)])

        # Check if the positions are occupied. 
        self.assertEqual('+', self.service.get_symbol(2, 1))
        self.assertEqual('+', self.service.get_symbol(3, 1))

        # Now let's try adding a ship over the same one. An Exception should be raised.  
        self.assertRaises(OverlappingShipsException, self.service.place_ship, [(1,1), (1,2)])

        # Now let's add a second ship. 
        self.service.place_ship([(3,4), (4,4)])

        # When we add the third ship, the first one should be replaced.
        self.service.place_ship([(5,5), (5,4)])

        # Check if the positions are freed. 
        self.assertEqual('.', self.service.get_symbol(2, 1))
        self.assertEqual('.', self.service.get_symbol(3, 1))

        # Check if the second ship still exists. 
        self.assertEqual('+', self.service.get_symbol(4, 3))
        self.assertEqual('+', self.service.get_symbol(4, 4))


if __name__ == "__main__":
    unittest.main()