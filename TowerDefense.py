from PyQt4 import QtCore, QtGui
from gameField import gameField
from menuBoard import menuBoard
from editField import editField
from var import Vars
import os
import sys
import json


class TowerDefense(QtGui.QMainWindow):
    """
    Main class
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.var = Vars()

        self.setFixedSize(self.var.boardWidth + 250, self.var.boardHeight)
        self.setWindowTitle('Tower Defense!')

        self.menuwindow = menuWindow(self)
        self.menuwindow.show()

        self.road = []

        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.menuboard = menuBoard(self)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(self.var.gameSpeed, self)
        self.update()

    def campaign(self):
        self.pause(False)
        self.var.level = 1
        self.var.campaign = True
        self.var.reset()
        self.board.setCurrentIndex(0)
        self.board.gameBoard.start([])
        self.menuwindow.hide()
        self.var.mode = self.var.GameMode.game

    def startGame(self):
        """
        Starting game after choosing a map
        """
        self.pause(False)
        self.var.campaign = False
        self.var.reset()
        self.board.setCurrentIndex(0)
        self.menuwindow.selectMap()
        self.board.gameBoard.start(self.road)
        self.menuwindow.hide()
        self.var.mode = self.var.GameMode.game

    def default(self):
        """
        Starting game with default map
        """
        self.pause(False)
        self.var.campaign = False
        self.var.reset()
        self.board.setCurrentIndex(0)
        self.menuwindow.defaultMap()
        self.board.gameBoard.start(self.road)
        self.menuwindow.hide()
        self.var.mode = self.var.GameMode.game

    def toMapEditor(self):
        """
        Opens map editor
        """
        self.pause(False)
        self.board.setCurrentIndex(1)
        self.board.editBoard.start()
        self.menuwindow.hide()
        self.var.mode = self.var.GameMode.edit

    '''Event handlers'''

    def keyPressEvent(self, event):
        """
        handler for ke
        """
        if (event.key() == QtCore.Qt.Key_S and
                self.var.mode == self.var.GameMode.edit):
            self.board.editBoard.save()
        if (event.key() == QtCore.Qt.Key_M and
                self.var.mode == self.var.GameMode.edit):
            self.board.editBoard.changeMode()
        if (event.key() == QtCore.Qt.Key_P and
                self.var.mode == self.var.GameMode.game):
            self.pause(True)
        if (event.key() == QtCore.Qt.Key_Shift and
                self.var.mode == self.var.GameMode.game):
            self.var.shiftPressed = True

    def keyReleaseEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Shift and
                self.var.mode == self.var.GameMode.game):
            self.var.shiftPressed = False

    def mousePressEvent(self, event):
        """
        handler for mousePress event
        """
        if self.var.mode == self.var.GameMode.game:
            self.board.gameBoard.placeTowerOrBomb()
        if self.var.mode == self.var.GameMode.edit:
            self.board.editBoard.setRoad()

    def eventFilter(self, source, event):
        """
        handler for mouseMove event
        """
        if event.type() == QtCore.QEvent.MouseMove:
            if (event.buttons() == QtCore.Qt.NoButton
                and (str(source).find("gameField") > 0
                     or str(source).find("editField") > 0)):
                mouse = event.pos()
                if self.var.mode == self.var.GameMode.game:
                    self.board.gameBoard.updateMouse(mouse.x(), mouse.y())
                    self.board.gameBoard.mouseIn = True
                    self.board.gameBoard.repaint()
                elif self.var.mode == self.var.GameMode.edit:
                    self.board.editBoard.updateMouse(mouse.x(), mouse.y())
                    self.board.editBoard.mouseIn = True
            else:
                if self.var.mode == self.var.GameMode.game:
                    self.board.gameBoard.mouseIn = False
                elif self.var.mode == self.var.GameMode.edit:
                    self.board.editBoard.mouseIn = False
                    self.update()
        return QtGui.QMainWindow.eventFilter(self, source, event)

    def timerEvent(self, event):
        """
        game thread
        moves mobs
        """
        if event.timerId() == self.timer.timerId():
            self.board.gameBoard.state.enemyManager()
            self.board.gameBoard.newLevel()
            self.board.gameBoard.state.countDamage()
            self.board.gameBoard.state.isGameOver()
            self.board.gameBoard.state.isWinner()
            self.menuboard.repaint()
            self.board.gameBoard.repaint()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def quit(self):
        self.timer.stop()
        self.deleteLater()

    def pause(self, f=None):
        if f is None:
            f = not self.var.pause
        if f:
            self.timer.stop()
            self.menuboard.pauseBtn.setText("Play")
            self.var.pause = True
        else:
            self.timer.start(self.var.gameSpeed, self)
            self.update()
            self.menuboard.pauseBtn.setText("Pause")
            self.var.pause = False


class Board(QtGui.QStackedWidget):
    """
    Class which represents main field and
    allows to switch between game and editor easily
    """

    def __init__(self, parent):
        QtGui.QStackedWidget.__init__(self, parent)
        self.parent = parent
        self.var = parent.var
        self.gameBoard = gameField(self)
        self.editBoard = editField(self)
        self.addWidget(self.gameBoard)
        self.addWidget(self.editBoard)


class menuWindow(QtGui.QDialog):
    """
    Class for starting menu window
    """

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setFixedSize(200, 250)

        self.campaign = QtGui.QPushButton("Start campaign", self)
        self.campaign.clicked.connect(self.parent.campaign)

        self.default = QtGui.QPushButton("Start (default map)", self)
        self.default.clicked.connect(self.parent.default)

        self.startButton = QtGui.QPushButton("Start a new game", self)
        self.startButton.setChecked(True)
        self.startButton.clicked.connect(self.parent.startGame)

        self.endlessButton = QtGui.QCheckBox("Endeless Mode", self)

        self.editButton = QtGui.QPushButton("Edit", self)
        self.editButton.clicked.connect(self.parent.toMapEditor)

        self.quitButton = QtGui.QPushButton("Quit", self)
        self.quitButton.clicked.connect(self.parent.quit)

        self.menubox = QtGui.QVBoxLayout()
        self.menubox.addWidget(self.campaign)
        self.menubox.addWidget(self.default)
        self.menubox.addWidget(self.startButton)
        self.menubox.addWidget(self.endlessButton)
        self.menubox.addWidget(self.editButton)
        self.menubox.addWidget(self.quitButton)
        self.setLayout(self.menubox)

    def selectMap(self):
        """
        opens selected map
        """
        self.isEndelessMode()
        filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open file', os.path.join(
                os.getcwd(), "maps"), "*.py")
        if filename == '':
            filename = os.path.join(os.getcwd(), "maps", "default.py")
        try:
            with open(filename) as f:
                self.parent.road = json.load(f)
        except OSError:
            print("Problem with file", file=sys.stderr)
            print("Choose another file")
            self.selectMap()

    def defaultMap(self):
        """
        opens default map
        """
        self.isEndelessMode()
        filename = os.path.join("maps", "default.py")
        try:
            with open(filename) as f:
                self.parent.road = json.load(f)
        except OSError:
            print("Problem with file", file=sys.stderr)
            print("Choose another file")
            self.selectMap()

    def isEndelessMode(self):
        self.parent.var.endlessmode = self.endlessButton.isChecked()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    towdef = TowerDefense()
    towdef.show()
    app.installEventFilter(towdef)
    sys.exit(app.exec_())
