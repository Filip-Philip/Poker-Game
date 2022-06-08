from enum import Enum, auto


class PlayerStatus(Enum):
    TO_MOVE = auto()  # player has yet to take a turn

    IN = auto()  # player in game with enough chips

    TO_CALL = auto()  # player should add chips to match the pull

    CHECKED = auto()  # player skips this turn given none other player made a currentBet

    OUT = auto()  # player folded

    ALL_IN = auto()