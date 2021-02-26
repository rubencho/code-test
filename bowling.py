from dataclasses import dataclass


PINS_IN_A_FRAME = 10
FRAMES_IN_A_MATCH = 10

class More10FramesInThisGame(Exception):
    pass

class GameOver(Exception):
    pass

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
        return self.first + self.second + self.third
    
    def make_score(self):
        self.frame_score = self.sum_pins()

    def is_strike(self) -> bool:
        return bool(self.first == PINS_IN_A_FRAME)

    def is_spare(self) -> bool:
        return bool((self.first < PINS_IN_A_FRAME) and (self.frame_score == PINS_IN_A_FRAME))


class BowlingGame:
    """ Give the score for a single bowling player
    """

    def __init__(self):
        self._match_frames = list()
        self._rolls_frame = 0
        self._game_over = False

    def score(self) -> int:
        return sum(f.frame_score for f in self._match_frames)

    def roll(self, pins: int):
        self._fill_frames_rolls(pins)
        self._update_frame_score(pins)

    #========== Fill rolls on frames ===========
    def _fill_frames_rolls(self, pins: int):
        self._check_if_frames_is_valid()
        self._check_if_invalid_roll(pins)

        if self._frame_10th():
            self._fill_frame_10th(pins)

        elif self._rolls_frame == 0:
            self._match_frames[-1].first = pins
            if  pins != PINS_IN_A_FRAME:  # Case IS NOT a strike
                self._rolls_frame = 1

        elif self._rolls_frame == 1:
            self._check_sum_of_pins_in_last_frame(pins)
            self._match_frames[-1].second = pins
            self._rolls_frame = 0

    def _fill_frame_10th(self, pins: int):
        if self._rolls_frame == 0:
            self._match_frames[-1].first = pins
            self._rolls_frame = 1

        elif self._rolls_frame == 1:
            self._match_frames[-1].second = pins
            self._match_frames[-1].make_score()
            if self._match_frames[-1].is_strike() or self._match_frames[-1].is_spare() or pins == PINS_IN_A_FRAME:
                self._rolls_frame = 2
            else:
                self._game_over = True

        elif self._rolls_frame == 2:
            self._match_frames[-1].third = pins
            self._game_over = True

    #============ Score code ================

    def _update_frame_score(self, pins: int):
        self._make_frame_score()
        self._update_strike_or_spare_extra_rolls()
        self._update_frame_bonus(pins)

    def _make_frame_score(self):
        self._match_frames[-1].make_score()
        if not self._frame_10th() and self._match_frames[-1].frame_score > 10:
            raise Exception(
                f'The sum of pins is incorret! Check if total score is between 0 and 10.')

    def _update_strike_or_spare_extra_rolls(self):
        """ Give the extra rolls to get the bonus point -2 or 1-
            in case strike or spare, respectivelly.
        """
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
    
    #======== Validation functions =========

    def _total_pins(self):
        return self._match_frames[-1].sum_pins()
    
    def _frame_10th(self):
        return len(self._match_frames) == FRAMES_IN_A_MATCH
    
    def _check_if_invalid_roll(self, pins: int):
        if not 0 <= pins <= 10 or not isinstance(pins, int):
            raise Exception(
                f'The value of {pins} pins is incorret! Check if rolls is between 0 and {PINS_IN_A_FRAME}.')

    def _check_sum_of_pins_in_last_frame(self, pins: int):
        if self._match_frames[-1].first + pins > PINS_IN_A_FRAME:
            raise ValueError(
                f'Something wrong with the sum of pins in this frame. Check if is frame score is between 0 and {PINS_IN_A_FRAME}.')

    def _check_if_frames_is_valid(self):
        if self._game_over:
            raise GameOver('The game is finish')

        if self._rolls_frame == 0:  # Check if a new frame is needed
            if self._frame_10th():
                raise More10FramesInThisGame(
                    f'There is more than {FRAMES_IN_A_MATCH} frames in this game.')            
            self._match_frames.append(Frame())


