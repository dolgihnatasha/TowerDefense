from PyQt4 import QtCore, QtGui
import os
import json
from enum import Enum


class editField(QtGui.QFrame):
    """
    Class for creating a map for a game
    """
    class EditMode(Enum):
        add_road = 1
        delete = 2
        add_block = 3

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.var = parent.var
        self.parent = parent
        self.roadblocks = []
        self.saved = False
        self.mouse_x = self.x = -1
        self.mouse_y = self.y = -1
        self.mode = self.EditMode.add_road
        self.savedialog = saveWindow(self)

    def start(self):
        if len(self.roadblocks) > 0 and self.saved:
            self.roadblocks = []
            self.saved = False
        self.setFixedSize(self.var.boardWidth, self.var.boardHeight)

    def updateMouse(self, x, y):
        """
        updates mouse position
        """
        self.mouse_x = x
        self.mouse_y = y
        self.x = x // self.var.blockSize
        self.y = y // self.var.blockSize
        self.repaint()

    def save(self):
        """
        saves map
        """
        if (len(self.roadblocks) > 0 and
                self.roadblocks[-1][0] ==
                (self.var.boardWidth / self.var.blockSize - 1)):
            self.savedialog.save()
            self.saved = True
        else:
            print("finish at the right")

    def setRoad(self):
        """
        Method for proper adding and deleting road
        """
        if self.mode == self.EditMode.add_road:
            if len(self.roadblocks) > 0 and self.isNeighbour():
                self.roadblocks.append([self.x, self.y])
                self.repaint()
            elif len(self.roadblocks) == 0 and self.x == 0:
                self.roadblocks.append([self.x, self.y])
        elif self.mode == self.EditMode.delete:
            if len(self.roadblocks) == 0:
                self.changeMode()
            else:
                if [self.x, self.y] in self.roadblocks:
                    i = self.roadblocks.index([self.x, self.y])
                    self.roadblocks = self.roadblocks[:i]

    def isNeighbour(self):
        """
        Returns "True" if block under the
        mouse is good for adding in the road
        """
        last = self.roadblocks[-1]
        if abs(last[0] - self.x) == 1 and last[1] == self.y:
            return True
        elif abs(last[1] - self.y) == 1 and last[0] == self.x:
            return True
        else:
            return False

    def changeMode(self):
        if self.mode == self.EditMode.add_road:
            self.mode = self.EditMode.delete
        else:
            self.mode = self.EditMode.add_road

    def paintEvent(self, event):
        """
        Overridden method for painting
        """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.setStyleSheet("QWidget { background: green }")
        self.drawMesh(qp)
        self.drawRoad(qp)
        qp.end()

    '''Drawing methods'''

    def drawRoad(self, qp):
        """
        draws road
        :param qp: QPainter object
        """
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QBrush(QtGui.QColor("red")))
        for block in self.roadblocks:
            qp.drawRect(block[0] * self.var.blockSize,
                        block[1] * self.var.blockSize,
                        self.var.blockSize, self.var.blockSize)

    def drawMesh(self, qp):
        """
        draws mesh
        """
        qp.setPen(QtGui.QPen())
        for i in range(20):
            qp.drawLine(0, i * self.var.blockSize,
                        self.var.boardWidth, i * self.var.blockSize)
            qp.drawLine(i * self.var.blockSize, 0,
                        i * self.var.blockSize, self.var.boardHeight)


class saveWindow():

    def __init__(self, parent):
        self.parent = parent

    def save(self):
        name = QtGui.QFileDialog.getSaveFileName(
            self.parent, "Save map", self.getNewFileName(), "*.py")
        with open(name, 'w') as f:
            json.dump(self.parent.roadblocks, f)

    def getNewFileName(self):
        i = 0
        while True:
            if not os.path.exists(os.path.join(
                    "maps", "userCreatedMap({}).py".format(i))):
                return os.path.join(
                    "maps", "userCreatedMap({}).py".format(i))
            else:
                i += 1

