from enum import Enum
from copy import copy
import os


class Vars:
    """
    global variables
    """
    cmpgn = {
        'm': {1: 30,
              2: 50,
              3: 70,
              4: 100,
              5: 100},
        'l': {1: 10,
              2: 10,
              3: 15,
              4: 20,
              5: 20},
        'b': {1: 0,
              2: 0,
              3: 1,
              4: 1,
              5: 1}}

    def __init__(self):
        self.blockSize = 30
        self.boardWidth = self.blockSize * 18
        self.boardHeight = self.blockSize * 18
        self.mode = self.GameMode.none
        self.BOOM_coast = 100
        self.moneyLimit = 1000
        self.pause = False
        self.shiftPressed = False
        self.endlessmode = False
        self.campaign = False
        self.gameSpeed = 30
        self.level = 1
        self.numOfLevels = self.getNumOfLevels()
        self.towerLimit = 18 * 18
        self.money = 0
        self.lives = 0
        self.numOfBombs = 0

    def reset(self):
        """
        sets variables to default
        """
        if self.campaign:
            self.moneyLimit = 100
            self.money = copy(Vars.cmpgn['m'][self.level])
            self.lives = copy(Vars.cmpgn['l'][self.level])
            self.numOfBombs = copy(Vars.cmpgn['b'][self.level])
        elif self.endlessmode:
            self.moneyLimit = 2000
            self.money = 2000
            self.lives = 20
            self.numOfBombs = 5
        else:
            self.moneyLimit = 1000
            self.money = 200
            self.lives = 20
            self.numOfBombs = 5

    def getNumOfLevels(self):
        files1 = next(os.walk(
            os.path.join(os.getcwd(), 'levels', "enemies")))
        files2 = next(os.walk(
            os.path.join(os.getcwd(), 'levels', "maps")))
        return min(len(files1[2]), len(files2[2]))

    class GameMode(Enum):
        none = 0
        game = 1
        edit = 2
