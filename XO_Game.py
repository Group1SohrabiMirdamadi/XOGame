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


class Game_Eng:

    def __init__(self, player1: Union[_Player, Literal['x', 'o']], player2: Union[_Player, Literal['x', 'o']],
                 rounds: int = 1):
        self.player1 = player1
        self.player2 = player2
        self.rounds = rounds
        self.game = _XOGame(self.player1, self.player2)

    @property
    def player1(self):
        return self._player1

    @player1.setter
    def player1(self, value: Union[_Player, Literal['x', 'o']]):
        try:
            if isinstance(value, _Player or Literal['x', 'o']):
                self._player1 = value
            else:
                raise _XOGame.InvalidPlayer("Player 1 type is not right", value)
        except _XOGame.InvalidPlayer as e:
            print("Error in assigning player1-->", e)

    @property
    def player2(self):
        return self._player2

    @player2.setter
    def player2(self, value: Union[_Player, Literal['x', 'o']]):
        try:
            if isinstance(value, _Player or Literal['x', 'o']):
                self._player2 = value
            else:
                raise _XOGame.InvalidPlayer("Player 2 type is not right", value)
        except _XOGame.InvalidPlayer as e:
            print("Error in assigning player2-->", e)

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        try:
            if value > 0 and isinstance(value, int):
                self._rounds = value
            else:
                raise _XOGame.InvalidRounds("Number of rounds should be a number and bigger than zero", value)
        except _XOGame.InvalidRounds as e:
            print("Error in Assigning Rounds-->", e)

    def run_game(self):
        player1_counter = 0
        player2_counter = 0

        for i in range(1, self.rounds):
            # self.game.reset_xo_map()
            except_checker = False
            _XOTable.xo_map = {k: None for k in range(1, 10)}
            result = None
            print(self.game.__str__())
            for j in range(9):
                result = self.game.winner()
                if result == None:
                    while True:
                        try:
                            print(f"Please {self.player1.name} Enter your mark number: ")
                            mark_player = int(input())
                            if 1 <= mark_player <= 9:
                                if _XOTable.xo_map[mark_player]:
                                    raise _XOGame.InvalidCellError('It filled before', mark_player)
                                # assert not _XOTable.xo_map[mark_player]
                                break

                            else:
                                # assert mark_player > 9 and mark_player < 1
                                raise _XOGame.InvalidCellError('Invalid input', mark_player)

                        except _XOGame.InvalidCellError as e:
                            print(e)
                            print('Try again!')
                            continue
                        except ValueError as v:
                            print(v)
                            print('Try again!')
                            continue
                if 0 < mark_player < 10 and result == None:
                    self.game.mark(mark_player, self.player1)
                    result = self.game.winner()
                result = self.game.winner()
                if result == None:
                    while True:
                        try:
                            print(f"Please {self.player2.name} Enter your mark number: ")
                            mark_player = int(input())
                            if 1 <= mark_player <= 9:
                                if _XOTable.xo_map[mark_player]:
                                    raise _XOGame.InvalidCellError('It filled before', mark_player)
                                # assert not _XOTable.xo_map[mark_player]
                                break

                            else:
                                # assert mark_player > 9 and mark_player < 1
                                raise _XOGame.InvalidCellError('Invalid input', mark_player)

                        except _XOGame.InvalidCellError as e:
                            print(e)
                            print('Try again!')
                            continue
                        except ValueError as v:
                            print(v)
                            print('Try again!')
                            continue
                if 0 < mark_player < 10 and result == None:
                    self.game.mark(mark_player, self.player2)
                    result = self.game.winner()

                try:
                    if result:
                        if result == self.player1.sign:
                            player1_counter += 1
                        if result == self.player2.sign:
                            player2_counter += 1

                        raise self.game.FinishedGameError(f"You Won in Round {i}", result)

                except self.game.FinishedGameError as e:
                    if except_checker == False:
                        print("Ended and", e)
                        except_checker = True

        try:
            if player1_counter > ((self.rounds) / 2):
               raise self.game.FinishedGameError("Won All The Game", self.player1.name)
        except self.game.FinishedGameError as e:
            print(e)


        try:
            if player2_counter > ((self.rounds) / 2):
               raise self.game.FinishedGameError("Won All The Game", self.player1.name)
        except self.game.FinishedGameError as e:
            print(e)


def main():

    player1 = _Player("Mamad", "x")
    player2 = _Player("Saeed", "o")
    rounds = 3

    x = Game_Eng(player1,player2, rounds)
    x.run_game()



main()
