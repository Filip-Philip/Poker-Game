from enum import Enum, auto


class PlayerAction(Enum):
    RAISE = auto()  # player in game with enough chips

    FOLD = auto()  # player should add chips to match the pull

    CHECK = auto()  # player skips this turn given none other player made a raise (Game.cur_raise == 0)

    CALL = auto()  # player folded

    ALL_IN = auto()     # player went all in
