from enum import Enum, auto


class PlayerStatus(Enum):
    IN = auto()  # player in game with enough chips

    TO_CALL = auto()  # player should add chips to match the pull

    CHECK = auto()  # player skips this turn given none other player made a currentBet

    OUT = auto()  # player folded
