from PyQt4 import QtCore, QtGui
from gameState import gameState
from Towers import Tower
import os
import sys
import json


class gameField(QtGui.QFrame):

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.parent = parent
        self.var = parent.var
        self.mouse_x = -1
        self.mouse_y = -1
        self.x = -1
        self.y = -1
        self.pic = QtGui.QPixmap(os.getcwd() + "/pictures/flippyboard.png")
        self.pic = self.pic.scaled(self.var.boardWidth, self.var.boardHeight)
        self.mouseIn = False
        self.setFixedSize(self.var.boardWidth, self.var.boardHeight)
        self.state = gameState(self)
        self.pos_time = 0
        self.enemy_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(), "pictures", "mob.png")).scaled(
            self.var.blockSize, self.var.blockSize)
        self.road_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(),
                         "pictures", "minrcraftdirt.png")).scaled(
            self.var.blockSize, self.var.blockSize)
        self.tower1_pic = QtGui.QPixmap(os.path.join(
            os.getcwd(), "pictures", "Bashnya1.png")).scaled(
            self.var.blockSize, self.var.blockSize)
        self.tower2_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(), "pictures", "Bashnya2.png")).scaled(
            self.var.blockSize, self.var.blockSize)
        self.tower3_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(), "pictures", "Bashnya3.png")).scaled(
            self.var.blockSize, self.var.blockSize)
        self.tower4_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(), "pictures", "Bashnya4.png")).scaled(
            self.var.blockSize, self.var.blockSize)
        self.tower_pic = {1: self.tower1_pic,
                          2: self.tower2_pic,
                          3: self.tower3_pic,
                          4: self.tower4_pic}
        self.gameover_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(), "pictures", "gameover.png")).scaled(
            self.var.boardWidth, self.var.boardHeight)
        self.winner_pic = QtGui.QPixmap(
            os.path.join(os.getcwd(), "pictures", "winner.png")).scaled(
            self.var.boardWidth, self.var.boardHeight)

    def start(self, road):
        if road:
            self.state.start(road)
        else:
            self.loadLevel()

    def placeTowerOrBomb(self):
        if self.mouseIn and self.state.isPlaceGoodForNewTower(self.x, self.y):
            self.state.addTower(self.x, self.y)
            if not self.var.shiftPressed:
                self.parent.parent.menuboard.noTower.setChecked(True)
        else:
            t = self.state.aboveSameTower(self.x, self.y)
            if (self.state.isTowerPicked() and
                    self.var.money >= Tower.cost[self.state.tower] and
                    self.mouseIn and t is not None):
                self.state.upgradeTower(t)
                if not self.var.shiftPressed:
                    self.parent.parent.menuboard.noTower.setChecked(True)
        if (self.state.tower == 5 and self.var.numOfBombs > 0 and
           self.var.money >= self.var.BOOM_coast and self.var.numOfBombs > 0):
            self.state.makeBoom(self.mouse_x, self.mouse_y)
            if not self.var.shiftPressed:
                self.parent.parent.menuboard.noTower.setChecked(True)

    def selectTower(self, n):
        self.state.tower = n

    def callWave(self):
        self.state.waveCalled = True

    def updateMouse(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        if ([x // self.var.blockSize, y // self.var.blockSize]
                == [self.x, self.y]):
            self.pos_time += 1
        else:
            self.x = x // self.var.blockSize
            self.y = y // self.var.blockSize
            self.pos_time = 0
        self.repaint()

    def paintEvent(self, event):
        """
        Overridden method for painting
        """
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.state.gameOver:
            self.gameOver(qp)
        elif self.state.winner:
            self.winner(qp)
        else:
            self.drawBackground(qp)
            self.drawRoad(qp)
            self.drawTowers(qp)
            self.drawEnemies(qp)
            self.drawAttackLine(qp)
            if self.state.isTowerPicked():
                self.drawOutline(qp)
            elif self.pos_time >= 7:
                self.drawTowerInfo(qp)
            if self.state.tower == 5:
                self.drawBOOM(qp)
        qp.end()

    def loadLevel(self):
        filename = os.path.join("levels", "maps", "level_{}.py".format(
            self.var.level))
        try:
            with open(filename) as f:
                road = json.load(f)
                print(self.var.level)
                self.state.start(road)
        except OSError as err:
            print("Problem with file:", err, file=sys.stderr)

    def newLevel(self):
        if (not self.state.enemies and not self.state.enemiesToGo and
                self.state.enemiesGone):
            if self.var.level < self.var.numOfLevels:
                self.var.level += 1
                self.var.reset()
                self.loadLevel()
            else:
                self.state.winner = True

    def getUnits(self):
        if self.var.campaign:
            filename = os.path.join(
                "levels", "enemies",
                "level_{}.py".format(self.var.level))
        elif self.var.endlessmode:
            filename = "enemies_endless.py"
        else:
            filename = os.path.join(os.getcwd(), "enemies.txt")
        with open(filename) as f:
            enemies = json.load(f)
        return enemies

    '''Drawing methods'''

    def winner(self, qp):
        qp.setBrush(QtGui.QColor("chartreuse"))
        qp.drawRect(0, 0, self.var.boardWidth, self.var.boardHeight)
        qp.drawPixmap(0, 0, self.winner_pic)

    def gameOver(self, qp):
        qp.setBrush(QtGui.QColor("chartreuse"))
        qp.drawRect(0, 0, self.var.boardWidth, self.var.boardHeight)
        qp.drawPixmap(0, 0, self.gameover_pic)

    def drawBackground(self, qp):
        qp.drawPixmap(0, 0, self.pic)

    def drawRoad(self, qp):
        for block in self.state.road:
            qp.drawPixmap(block[0] * self.var.blockSize,
                          block[1] * self.var.blockSize,
                          self.road_pic)

    def drawTowers(self, qp):
        for tower in self.state.towers:
            qp.drawPixmap(tower.x * self.var.blockSize,
                          tower.y * self.var.blockSize,
                          self.tower_pic[tower.type])

    def drawMesh(self, qp):
        qp.setPen(QtGui.QPen())
        for i in range(20):
            qp.drawLine(0, i * self.var.blockSize,
                        self.var.boardWidth, i * self.var.blockSize)
            qp.drawLine(i * self.var.blockSize,
                        0, i * self.var.blockSize, self.var.boardHeight)

    def drawOutline(self, qp):
        if self.mouseIn:
            qp.setPen(QtGui.QColor("gray"))
            qp.drawPixmap(self.x * self.var.blockSize,
                          self.y * self.var.blockSize,
                          self.tower_pic[self.state.tower])
            qp.setBrush(QtGui.QColor(0, 0, 0, 55))
            qp.setPen(QtCore.Qt.NoPen)
            center = QtCore.QPoint(
                self.x * self.var.blockSize + self.var.blockSize // 2,
                self.y * self.var.blockSize + self.var.blockSize // 2)
            qp.drawEllipse(center, Tower.radius[self.state.tower],
                           Tower.radius[self.state.tower])
        if [self.x, self.y] in self.state.occupied and self.mouseIn:
            qp.setPen(QtCore.Qt.NoPen)
            qp.setBrush(QtGui.QColor(255, 255, 255, 155))
            qp.drawRect(self.x * self.var.blockSize,
                        self.y * self.var.blockSize,
                        self.var.blockSize, self.var.blockSize)

    def drawEnemies(self, qp):
        for e in self.state.enemies:
            qp.setBrush(QtGui.QColor(e.color))
            qp.setPen(QtGui.QColor("white"))
            qp.drawPixmap(e.posx, e.posy, self.enemy_pic)
            """
            qp.drawEllipse(QtCore.QPoint(e.getCenter()[0],
                                         e.getCenter()[1]),
                           e.size, e.size)"""
            qp.setFont(QtGui.QFont('Decorative', 12))
            qp.drawText(e.posx, e.posy, "{}".format(
                int(e.health * 100 // e.maxHealth)))

    def drawAttackLine(self, qp):
        qp.setPen(QtGui.QColor("black"))
        for t in self.state.towers:
            for e in t.targets:
                qp.drawLine(t.center[0], t.center[1],
                            e.getCenter()[0], e.getCenter()[1])

    def drawTowerInfo(self, qp):
        if self.state.tower == 0:
            for t in self.state.towers:
                if self.x == t.x and self.y == t.y:
                    qp.setPen(QtCore.Qt.NoPen)
                    qp.setBrush(QtGui.QColor(0, 0, 0, 55))
                    center = QtCore.QPoint(
                        t.x * self.var.blockSize + self.var.blockSize // 2,
                        t.y * self.var.blockSize + self.var.blockSize // 2)
                    qp.drawEllipse(center, Tower.radius[t.type],
                                   Tower.radius[t.type])
                    qp.setPen(QtGui.QColor("black"))
                    qp.setBrush(QtGui.QColor(155, 155, 155, 155))
                    qp.setFont(QtGui.QFont('Decorative', 12))
                    qp.drawRect(self.mouse_x + 10,
                                self.mouse_y + 10, 150, 55)
                    step = 16
                    textStartX = self.mouse_x + 15
                    textStartY = self.mouse_y + 11
                    if t.type != 1:
                        qp.drawText(textStartX,
                                    textStartY + step,
                                    "Damage: " + str(t.damage))
                    else:
                        qp.drawText(textStartX,
                                    textStartY + step,
                                    "Power: " + str(t.power))
                    qp.drawText(textStartX,
                                textStartY + step * 2,
                                "Range: " + str(t.radius))
                    qp.drawText(textStartX,
                                textStartY + step * 3,
                                "Level: " + str(t.level))

    def drawBOOM(self, qp):
        if self.mouseIn:
            qp.setBrush(QtGui.QColor(255, 0, 0, 55))
            center = QtCore.QPoint(self.mouse_x, self.mouse_y)
            qp.drawEllipse(center, self.state.bombRadius,
                           self.state.bombRadius)
