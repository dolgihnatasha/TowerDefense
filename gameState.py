from copy import copy
from Towers import Tower
from enemy import Enemy
from math import sqrt


class gameState:

    def __init__(self, parent=None):
        self.parent = parent
        if self.parent is None:
            # for tests
            from Towers import Tower
            from var import Vars
            self.var = Vars()
        else:
            self.var = parent.var
        self.gameOver = False
        self.winner = False
        self.enemiesGone = False
        self.road = []
        self.occupied = []
        self.wave = 1
        self.waveSent = False
        self.waveCalled = False
        self.enemies = []
        self.towers = []
        self.tower = 0
        self.enemiesToGo = {}
        self.bombRadius = 100
        self.bombDamage = 1000

    def start(self, road):
        self.road = road
        self.occupied = copy(road)
        self.gameOver = False
        self.winner = False
        self.enemiesGone = False
        self.wave = 1
        self.waveSent = False
        self.waveCalled = False
        self.enemies = []
        self.towers = []
        self.tower = 0
        self.enemiesToGo = self.getUnits()

    def isTowerPicked(self):
        self.tower = self.parent.parent.parent.menuboard.checkedTower()
        return 0 < self.tower < 5

    def isPlaceGoodForNewTower(self, x, y):
        return (self.isTowerPicked() and
                self.var.money >= Tower.cost[self.tower] and
                [x, y] not in self.occupied)

    def addTower(self, x, y):
        self.towers.append(Tower(x, y, self.tower, self))
        self.occupied.append([x, y])
        self.var.money -= Tower.cost[self.tower]

    def makeBoom(self, x, y):
        self.var.money -= 100
        self.var.numOfBombs -= 1
        for e in self.enemies:
            if gameState.distance(e, x, y) <= self.bombRadius:
                e.getDamage(self.bombDamage)

    @staticmethod
    def distance(e, x, y):
        return sqrt((e.getCenter()[0] - x) *
                    (e.getCenter()[0] - x) +
                    (e.getCenter()[1] - y) *
                    (e.getCenter()[1] - y))

    def enemyManager(self):
        """
        moves enemies
        """
        if not self.var.endlessmode:
            self.sendEnemies()
        else:
            self.sendEnemiesEndless()
        i = 0
        while i < len(self.enemies):
            e = self.enemies[i]
            if e.dead:
                self.enemies.remove(e)
                if not self.var.endlessmode:
                    self.var.money += e.value
                if self.var.money > self.var.moneyLimit:
                    self.var.money = self.var.moneyLimit
            if e.finished:
                self.enemies.remove(e)
                self.var.lives -= 1
            else:
                e.moveUnit()
                i += 1

    def sendEnemies(self):
        if self.waveCalled and self.enemiesToGo:
            self.enemiesGone = True
            if len(self.enemies) != 0:
                if (self.enemies[-1].distance >=
                        self.enemiesToGo[str(self.wave)]["delay"]):
                    self.enemies.append(Enemy(
                        self.road, self.enemiesToGo[str(self.wave)]["HP"],
                        self.enemiesToGo[str(self.wave)]["color"], self))
                    self.enemiesToGo[str(self.wave)]["units"] -= 1
                if self.enemiesToGo[str(self.wave)]["units"] == 0:
                    del self.enemiesToGo[str(self.wave)]
                    self.wave += 1
                    self.waveCalled = False
                else:
                    self.waveCalled = True
            else:
                self.enemies.append(Enemy(
                    self.road, self.enemiesToGo[str(self.wave)]["HP"],
                    self.enemiesToGo[str(self.wave)]["color"], self))
                self.enemiesToGo[str(self.wave)]["units"] -= 1
        if (not self.enemies and self.enemiesGone
                and self.parent.parent.parent
                    .menuboard.autoSendingBtn.isChecked()):
            self.waveCalled = True

    def sendEnemiesEndless(self):
        if self.waveCalled:
            if len(self.enemies) != 0:
                if self.enemies[-1].distance >= self.enemiesToGo["delay"]:
                    self.enemies.append(Enemy(
                        self.road, self.enemiesToGo["HP"] * self.wave,
                        self.enemiesToGo["color"], self))
                    self.enemiesToGo["units"] -= 1
                if self.enemiesToGo["units"] == 0:
                    if not (self.parent.parent.parent.
                            menuboard.autoSendingBtn.isChecked()):
                        self.waveCalled = False
                    self.wave += 1
                    self.enemiesToGo["units"] += self.wave
            else:
                self.enemies.append(Enemy(
                    self.road, self.enemiesToGo["HP"] * self.wave,
                    self.enemiesToGo["color"], self))
                self.enemiesToGo["units"] -= 1
        if len(self.enemies) == 0 and self.wave != 1:
            self.waveCalled = True

    def countDamage(self):
        for t in self.towers:
            if t.type == 1:
                t.checkUpgrades(self.towers)
            else:
                gameState.giveDamage(t, self.enemies)

    @staticmethod
    def giveDamage(tower, enemies):
        tower.targets = []
        numOfTargets = tower.numOfTargets
        for e in enemies:
            if gameState.distance(
                    e, tower.center[0], tower.center[1]) <= tower.radius:
                tower.targets.append(e)
                e.getDamage(tower.damage)
                numOfTargets -= 1
                if numOfTargets == 0:
                    break

    def getUnits(self):
        return self.parent.getUnits()

    def isGameOver(self):
        self.var.gameOver = self.var.lives <= 0

    def isWinner(self):
        self.var.winner = (not self.enemiesToGo and
                           self.enemiesGone and not self.enemies)

    def aboveSameTower(self, x, y):
        for t in self.towers:
            if [t.x, t.y] == [x, y] and t.type == self.tower:
                return t
        return None

    def upgradeTower(self, tower):
        if tower.type == 1:
            tower.power += Tower.level[tower.type]
        else:
            tower.damage += tower.damage * Tower.level[tower.type]
        tower.level += 1
        self.var.money -= Tower.cost[tower.type] // 2
