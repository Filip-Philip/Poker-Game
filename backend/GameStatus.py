from enum import Enum, auto


class GameStatus(Enum):
    STARTED = auto()

    PREFLOP = auto()

    FLOP = auto()

    TURN = auto()

    RIVER = auto()

    SHOWDOWN = auto()
    
    ENDED = auto()
