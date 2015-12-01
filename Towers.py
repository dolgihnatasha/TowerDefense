from copy import copy
from math import sqrt


class Tower:

    color = {
        0: "black",
        1: "chartreuse",
        2: "blue",
        3: "darkMagenta",
        4: "cyan"
    }
    radius = {
        0: 0,
        1: 60,
        2: 80,
        3: 150,
        4: 220
    }
    cost = {
        0: 0,
        1: 15,
        2: 10,
        3: 10,
        4: 12
    }
    damage = {
        0: 0,
        1: 0,
        2: 3,
        3: 2,
        4: 1
    }
    level = {
        0: 0,
        1: 0.1,
        2: 0.2,
        3: 0.3,
        4: 0.4
    }  # how much better become damage/power after level upgrade

    def __init__(self, x, y, towerType, parent):
        self.var = parent.var
        self.parent = parent
        self.type = towerType
        self.x = x
        self.y = y
        self.radius = copy(Tower.radius[self.type])
        self.cost = copy(Tower.cost[self.type])
        self.color = copy(Tower.color[self.type])
        if self.type == 1:
            self.power = 1.5
        else:
            self.basicDamage = copy(Tower.damage[towerType])
            self.damage = copy(Tower.damage[towerType])
        self.level = 1
        self.upgrades = []
        self.targets = []
        self.numOfTargets = 2
        self.center = [(x + 0.5) * self.var.blockSize,
                       (y + 0.5) * self.var.blockSize]

    def checkUpgrades(self, towers):
        """
        Calls from upgrading tower
        gives upgrades for closest towers
        """
        for t in towers:
            if self != t and t.type != 1:
                if self not in t.upgrades:
                    distance = sqrt((t.center[0] - self.center[0]) *
                                    (t.center[0] - self.center[0]) +
                                    (t.center[1] - self.center[1]) *
                                    (t.center[1] - self.center[1]))
                    if distance <= self.radius:
                        t.damage *= self.power
                        t.damage = round(t.damage, 3)
                        t.upgrades.append(self)

    def newLevel(self):
        """
        defines damage for new level of tower
        """
        if self.type == 1:
            self.power += Tower.level[self.type]
        else:
            self.basicDamage += Tower.level[self.type]
            self.basicDamage = round(self.basicDamage)
            self.damage = round(self.basicDamage)
            self.checkUpgrades(self.parent.towers)
        self.level += 1
