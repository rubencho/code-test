import unittest

from bowling import BowlingGame, More10FramesInThisGame

class TestBowling(unittest.TestCase):

    def setUp(self):
        self.g = BowlingGame()
    
    def roll_many(self, n, pins):
        for _ in range(n):
            self.g.roll(pins)

    def roll_spare(self):
        self.g.roll(5)
        self.g.roll(5)

    def roll_strike(self):
        self.g.roll(10)

    def test_error_pins_greater_than_10(self):
        with self.assertRaises(Exception):
            self.g.roll(11)


    def test_error_pins_lower_than_0(self):
        with self.assertRaises(Exception):
            self.g.roll(-1)

    def test_gutter_game(self):
        self.roll_many(20, 0)
        self.assertEqual(self.g.score(), 0)

    def test_all_ones(self):
        self.roll_many(20, 1)
        self.assertEqual(self.g.score(), 20)

    def test_one_spare(self):
        self.roll_spare()
        self.g.roll(3)
        self.roll_many(17, 0)
        self.assertEqual(self.g.score(), 16)

    def test_one_strike(self):
        self.roll_strike()
        self.g.roll(3)
        self.g.roll(4)
        self.roll_many(16, 0)
        self.assertEqual(self.g.score(), 24)

    def test_perfect_game(self):
        self.roll_many(12, 10)
        self.assertEqual(self.g.score(), 300)

    def test_more_than_21_rolls_raises_error(self):
        self.roll_many(18, 0)
        self.roll_spare()
        self.g.roll(0)
        with self.assertRaises(More10FramesInThisGame):
            self.g.roll(3)

if __name__ == '__main__':
    unittest.main()