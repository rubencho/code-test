
from dataclasses import dataclass

PINS_IN_A_FRAME = 10
FRAMES_IN_A_MATCH = 10

@dataclass
class Frame:
    """ Better than nametuples or simple list type
    """
    first: int = 0
    second: int = 0
    third: int = 0  # Third field for 10th frame in case of spare of strike
    frame_score: int = 0
    bonus_rolls: int = 0

    def sum_pins(self):
        total_pins = self.first + self.second + self.third
        if not isinstance(total_pins, int) and 0 < total_pins > 10 :
            raise ValueError(f'There is something wrong with pins on frame {self}.') 
        self.frame_score = total_pins

    def is_strike(self) -> bool:
        return bool(self.first == PINS_IN_A_FRAME)
    
    def is_spare(self) -> bool:
        return bool((self.first < PINS_IN_A_FRAME) and (self.frame_score == PINS_IN_A_FRAME))


class More10FramesInThisGame(Exception):
    pass

class BowlingGame:
    """ Give the score for a single bowling player
    """
    def __init__(self):
        self._match_frames = list()
        self._first_roll = True

    def score(self) -> int:
        return sum(f.frame_score for f in self._match_frames)

    def roll(self, pins: int):
        self._check_if_frames_is_valid()
        self._check_if_invalid_roll(pins)
        self._fill_frames_rolls(pins)
        self._update_frame_score()
        self._update_strike_or_spare()
        self._update_frame_bonus(pins)

    def _fill_frames_rolls(self, pins: int):
        if len(self._match_frames) >= 9 and pins == 10:
            if self._first_roll == True:
                self._match_frames.append(Frame(first=pins))
                self._first_roll = False
            if self._first_roll == False:
                self._match_frames[-1].second = pins
                self._first_roll = 3
            if self._first_roll == 3:
                self._match_frames[-1].third = pins

        elif pins == PINS_IN_A_FRAME and self._first_roll == True: # Case of strike
            self._match_frames.append(Frame(first=pins))

        elif self._first_roll == True:
            self._match_frames.append(Frame(first=pins))
            self._first_roll = False

        elif self._first_roll == False:
            self._check_sum_of_pins_in_last_frame(pins)
            self._match_frames[-1].second = pins
            self._first_roll = True

    def _update_frame_score(self):
        self._match_frames[-1].sum_pins()

    def _update_strike_or_spare(self):
        cf = self._match_frames[-1]
        if cf.is_strike():
            rolls_extra = 2
        elif cf.is_spare():
            rolls_extra = 1
        else:
            rolls_extra = 0
        self._match_frames[-1].bonus_rolls = rolls_extra

    def _update_frame_bonus(self, pins: int):
        """ Check if last two frames need a bonus
            due to frame is strike or spare
        """
        for frame in self._match_frames[-3:-1]:
            if frame.bonus_rolls > 0:
                frame.frame_score += pins
                frame.bonus_rolls -= 1

    def _check_if_frames_is_valid(self):
        if len(self._match_frames) > 10:
            raise More10FramesInThisGame('There is more than {FRAMES_IN_A_MATCH} in this game.')
    
    def _check_sum_of_pins_in_last_frame(self, pins: int):
        if self._match_frames[-1].first + pins > PINS_IN_A_FRAME:
            raise ValueError('Something wrong with the sum of pins in this frame.')

    @staticmethod
    def _check_if_invalid_roll(pins: int):
        if pins > 10 or pins < 0:
            raise Exception(f" The value of {pins} pins is incorret! Check if is between 0 and 10")


