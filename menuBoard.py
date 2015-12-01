from PyQt4 import QtCore, QtGui
from Towers import Tower


class menuBoard(QtGui.QFrame):

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.parent = parent
        self.var = parent.var
        self.isPaused = False
        self.setStyleSheet(
            "QWidget { background: goldenrod; font-size: 13pt;};")
        self.setGeometry(self.var.boardWidth, 0, 250, self.var.boardHeight)

        self.buttonbox = QtGui.QVBoxLayout()

        self.noTower = QtGui.QRadioButton("No tower", self)
        self.noTower.setChecked(True)

        self.tower1Btn = QtGui.QRadioButton("Helper, cost: "
                                            "{}".format(Tower.cost[1]), self)

        self.tower2Btn = QtGui.QRadioButton(
            "Near && Strong, cost: {}".format(Tower.cost[2]), self)

        self.tower3Btn = QtGui.QRadioButton(
            "Super Balanced!, cost: {}".format(Tower.cost[3]), self)

        self.tower4Btn = QtGui.QRadioButton(
            "Far && Weak, cost: {}".format(Tower.cost[4]), self)

        self.bombBtn = QtGui.QRadioButton(
            "Bomb, cost: {}".format(self.var.BOOM_coast), self)

        self.buttonbox.addSpacing(200)
        spacing = 5
        self.buttonbox.addWidget(self.noTower)
        self.buttonbox.addSpacing(spacing)
        self.buttonbox.addWidget(self.tower1Btn)
        self.buttonbox.addSpacing(spacing)
        self.buttonbox.addWidget(self.tower2Btn)
        self.buttonbox.addSpacing(spacing)
        self.buttonbox.addWidget(self.tower3Btn)
        self.buttonbox.addSpacing(spacing)
        self.buttonbox.addWidget(self.tower4Btn)
        self.buttonbox.addSpacing(spacing)
        self.buttonbox.addWidget(self.bombBtn)
        self.buttonbox.addSpacing(spacing)

        self.newWaveBtn = QtGui.QPushButton("New Wave", self)
        self.connect(self.newWaveBtn,
                     QtCore.SIGNAL("clicked()"), self.callWave)
        self.buttonbox.addWidget(self.newWaveBtn)
        self.buttonbox.addSpacing(spacing)

        self.autoSendingBtn = QtGui.QCheckBox("Auto send new wave", self)
        self.buttonbox.addWidget(self.autoSendingBtn)

        self.buttonbox.addSpacing(70)

        self.pauseBtn = QtGui.QPushButton("Pause", self)
        self.connect(self.pauseBtn,
                     QtCore.SIGNAL("clicked()"), self.parent.pause)
        self.buttonbox.addWidget(self.pauseBtn)

        self.menuBtn = QtGui.QPushButton("Open Menu", self)
        self.connect(self.menuBtn,
                     QtCore.SIGNAL("clicked()"), self.showMenu)
        self.buttonbox.addWidget(self.menuBtn)
        self.setLayout(self.buttonbox)

    def showMenu(self):
        self.parent.pause(True)
        self.parent.menuwindow.show()

    def callWave(self):
        if self.var.mode == self.var.GameMode.game:
            self.parent.board.gameBoard.callWave()

    def checkedTower(self):
        if self.noTower.isChecked():
            return 0
        elif self.tower1Btn.isChecked():
            return 1
        elif self.tower2Btn.isChecked():
            return 2
        elif self.tower3Btn.isChecked():
            return 3
        elif self.tower4Btn.isChecked():
            return 4
        elif self.bombBtn.isChecked():
            return 5

    def paintEvent(self, event):
        self.checkMoney()
        qp = QtGui.QPainter()
        qp.begin(self)
        self.gameStats(qp)
        qp.end()

    def checkMoney(self):
        if not self.var.shiftPressed:
            if self.var.money < Tower.cost[1]:
                self.tower1Btn.setDisabled(True)
            else:
                self.tower1Btn.setDisabled(False)
            if self.var.money < Tower.cost[2]:
                self.tower2Btn.setDisabled(True)
            else:
                self.tower2Btn.setDisabled(False)
            if self.var.money < Tower.cost[3]:
                self.tower3Btn.setDisabled(True)
            else:
                self.tower3Btn.setDisabled(False)
            if self.var.money < Tower.cost[4]:
                self.tower4Btn.setDisabled(True)
            else:
                self.tower4Btn.setDisabled(False)
            if self.var.money < self.var.BOOM_coast or self.var.numOfBombs == 0:
                self.bombBtn.setDisabled(True)
            else:
                self.bombBtn.setDisabled(False)

    def gameStats(self, qp):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        qp.drawRect(5, 5, 240, 95)
        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 12))
        x_start = 10
        y_start = 22
        y_offset = 18
        qp.drawText(x_start, y_start + y_offset * 0,
                    "Money: " + str(self.var.money))
        qp.drawText(x_start, y_start + y_offset * 1,
                    "Lives: " + str(self.var.lives))
        if not self.var.endlessmode:
            qp.drawText(x_start, y_start + y_offset * 2, "Waves left: " +
            "{}".format(len(self.parent.board.gameBoard.state.enemiesToGo)))
            if self.var.campaign:
                qp.drawText(x_start, y_start + y_offset * 4,
                            "Level: {}".format(self.var.level))
        else:
            qp.drawText(x_start, y_start + y_offset * 2, "Wave: " +
                        str(self.parent.board.gameBoard.state.wave))

        if self.var.mode == self.var.GameMode.edit:
            qp.drawText(x_start, y_start + y_offset * 3,
                        "Mode: " +
                        self.parent.board.editBoard.mode.name +
                        " ([M] to change)")
        else:
            qp.drawText(x_start, y_start + y_offset * 3, "Bombs left: " +
                        "{}".format(self.var.numOfBombs))