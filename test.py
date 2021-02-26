import unittest

from bowling import BowlingGame, More10FramesInThisGame, GameOver


class TestBowling(unittest.TestCase):

    def setUp(self):
        self.g = BowlingGame()

    def roll_many(self, n, pins):
        for _ in range(n):
            self.g.roll(pins)

    def roll_spare(self):
        self.g.roll(4)
        self.g.roll(6)

    def roll_strike(self):
        self.g.roll(10)

    def test_error_pins_greater_than_10(self):
        with self.assertRaises(Exception):
            self.g.roll(11)

    def test_error_pins_lower_than_0(self):
        with self.assertRaises(Exception):
            self.g.roll(-1)

    def test_error_pins_float_number(self):
        with self.assertRaises(Exception):
            self.g.roll(2.3)

    def test_error_sum_rolls_greater_than_10_then_correct_score(self):
        self.g.roll(6)
        with self.assertRaises(Exception):
            self.g.roll(5)
        self.g.roll(3)
        self.assertEqual(self.g.score(), 9)

    def test_error_more_than_21_rolls_raises_error(self):
        self.roll_many(20, 0)
        with self.assertRaises(GameOver):
            self.g.roll(3)

    def test_first_two_4_pins_rolls_and_get_score(self):
        self.g.roll(4)
        self.g.roll(4)
        self.assertEqual(self.g.score(), 8)

    def test_all_ceros(self):
        self.roll_many(20, 0)
        self.assertEqual(self.g.score(), 0)

    def test_all_ones(self):
        self.roll_many(20, 1)
        self.assertEqual(self.g.score(), 20)

    def test_one_spare(self):
        self.roll_spare()
        self.g.roll(5)
        self.g.roll(0)
        self.assertEqual(self.g.score(), 20)

    def test_one_strike(self):
        self.roll_strike()
        self.g.roll(5)
        self.g.roll(4)
        self.assertEqual(self.g.score(), 28)

    def test_spare_on_frame_10(self):
        self.roll_many(18, 0)
        self.g.roll(5)
        self.g.roll(5) 
        self.g.roll(3)
        self.assertEqual(self.g.score(), 13)

    def test_perfect_game(self):
        self.roll_many(9, 10)
        self.g.roll(10)
        self.g.roll(10)
        self.g.roll(10)
        self.assertEqual(self.g.score(), 300)


if __name__ == '__main__':
    unittest.main()
