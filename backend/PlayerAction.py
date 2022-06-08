from enum import Enum, auto


class PlayerAction(Enum):
    RAISE = auto()  # player in game with enough chips

    FOLD = auto()  # player should add chips to match the pull

    CHECK = auto()  # player skips this turn given none other player made a raise (Game.cur_raise == 0)

    CALL = auto()  # player folded

    ALL_IN = auto()     # player went all in

    def __str__(self):
        if self == PlayerAction.CALL:
            return "CALL"
        elif self == PlayerAction.FOLD:
            return "FOLD"
        elif self == PlayerAction.CHECK:
            return "CHECK"
        elif self == PlayerAction.RAISE:
            return "RAISE"
        elif self == PlayerAction.ALL_IN:
            return "ALL IN"
