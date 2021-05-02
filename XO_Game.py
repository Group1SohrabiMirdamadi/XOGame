from typing import Literal, Union, Optional
from typing import Dict
from os import system
import os


class _Player:
    def __init__(self, name: str, sign: Literal['x', 'o']) -> None:
        self.name = name
        self.sign = sign


class _XOTable:
    xo_map = {k: None for k in range(1, 10)}  # {1:x, 2: None, 3: o, ...}

    def __str__(self):

        map = self.xo_map
        return """
 -----------------
|  {}  |  {}  |  {}  |
 -----------------
|  {}  |  {}  |  {}  |
 -----------------
|  {}  |  {}  |  {}  |
 -----------------
""".format(*[map[i] if map[i] else i for i in map])

    def reset_xo_map(self):
        self.xo_map = {k: None for k in range(1, 10)}

    def mark(self, cell_no, player: _Player):
        assert isinstance(cell_no, int) and 1 <= cell_no <= 9, "Enter a valid cell no [1, 9]"
        assert not self.xo_map[cell_no], "Cell is filled"
        sign = str(player.sign).lower()
        # assert sign in 'xo', 'Invalid sign' + sign
        self.xo_map[cell_no] = sign


class _XOGame(_XOTable):
    class UnFinishedGameError(Exception):
        def __init__(self, message, field):
            self.message = message
            self.field = field

        def __str__(self):
            return f"{self.message} and Game Finished with No Winner--->>{self.field}"

    class FinishedGameError(Exception):
        def __init__(self, message, field):
            self.message = message
            self.field = field

        def __str__(self):
            return f"{self.message} Winner is--->> {self.field}"

    class InvalidCellError(Exception):
        def __init__(self, message, field):
            self.message = message
            self.field = field

        def __str__(self):
            return f"{self.message} Invalid Cell--->>{self.field}"

    class InvalidPlayer(Exception):
        def __init__(self, message, field):
            self.message = message
            self.field = field

        def __str__(self):
            return f"{self.message} --->>{self.field}"

    class InvalidRounds(Exception):
        def __init__(self, message, field):
            self.message = message
            self.field = field

        def __str__(self):
            return f"{self.message} --->>{self.field}"

    def __init__(self, player1: _Player, player2: _Player) -> None:
        try:
            if not player1.sign == player2.sign and isinstance(player1, _Player) and isinstance(player2, _Player):
                self.player1 = player1
                self.player2 = player2
            else:
                raise _XOGame.InvalidPlayer("Please Enter different signs for players", self.player2.sign + ' , ' \
                                            + self.player2.sign)

        except _XOGame.InvalidPlayer as e:
            print("Error Occured in assigning players -->> ", e)

    def _calculate_result(self):
        if super(_XOGame, self).xo_map[1] == super(_XOGame, self).xo_map[2] == super(_XOGame, self).xo_map[3]:
            return super(_XOGame, self).xo_map[1]
        if super(_XOGame, self).xo_map[4] == super(_XOGame, self).xo_map[5] == super(_XOGame, self).xo_map[6]:
            return super(_XOGame, self).xo_map[4]
        if super(_XOGame, self).xo_map[7] == super(_XOGame, self).xo_map[8] == super(_XOGame, self).xo_map[9]:
            return super(_XOGame, self).xo_map[7]
        if super(_XOGame, self).xo_map[1] == super(_XOGame, self).xo_map[4] == super(_XOGame, self).xo_map[7]:
            return super(_XOGame, self).xo_map[1]
        if super(_XOGame, self).xo_map[2] == super(_XOGame, self).xo_map[5] == super(_XOGame, self).xo_map[8]:
            return super(_XOGame, self).xo_map[2]
        if super(_XOGame, self).xo_map[3] == super(_XOGame, self).xo_map[6] == super(_XOGame, self).xo_map[9]:
            return super(_XOGame, self).xo_map[3]
        if super(_XOGame, self).xo_map[1] == super(_XOGame, self).xo_map[5] == super(_XOGame, self).xo_map[9]:
            return super(_XOGame, self).xo_map[1]
        if super(_XOGame, self).xo_map[3] == super(_XOGame, self).xo_map[5] == super(_XOGame, self).xo_map[7]:
            return super(_XOGame, self).xo_map[3]

        return None

    def mark(self, cell_no, player: Union[_Player, Literal['x', 'o'], int]):
            super(_XOGame, self).mark(cell_no, player)
            print(super(_XOGame, self).__str__())


    def winner(self) -> Optional[_Player]:
        result = None
        result = self._calculate_result()
        return result
