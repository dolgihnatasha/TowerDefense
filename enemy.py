import copy
from enum import Enum


class Enemy:

    class Direction(Enum):
        up = 1
        right = 2
        down = 3
        left = 4

    def __init__(self, road, hp, color, parent):
        self.road = copy.deepcopy(road)
        self.var = parent.var

        self.health = hp
        self.maxHealth = hp
        self.speed = 2
        self.color = color

        self.dead = False
        self.finished = False
        self.distance = 0
        if self.health < 200:
            self.value = 1
        else:
            self.value = self.health // 200

        self.size = self.var.blockSize // 2 - 2
        self.posx = road[0][0] * self.var.blockSize
        self.posy = road[0][1] * self.var.blockSize

        self.currentBlock = self.road.pop(0)
        self.nextBlock = self.road.pop(0)
        self.direction = self.Direction.right
        self.defineDirection()
        self.defineCurrentBlock()

    def moveUnit(self):
        """
        Moves enemy
        """
        self.defineCurrentBlock()
        self.distance += self.speed
        if self.direction == self.Direction.right:
            self.posx += self.speed
        elif self.direction == self.Direction.down:
            self.posy += self.speed
        elif self.direction == self.Direction.left:
            self.posx -= self.speed
        elif self.direction == self.Direction.up:
            self.posy -= self.speed

    def defineCurrentBlock(self):
        """
        defines current block from coordinates
        """
        x = self.posx // self.var.blockSize
        y = self.posy // self.var.blockSize
        if self.direction == self.Direction.up:
            y = (self.posy + self.var.blockSize - 1) // self.var.blockSize
        if self.direction == self.Direction.left:
            x = (self.posx + self.var.blockSize - 1) // self.var.blockSize
        if self.posx < 0:
            x = 0
        if self.posy < 0:
            y = 0
        self.currentBlock = [x, y]
        if self.currentBlock == self.nextBlock:
            if len(self.road) > 1:
                self.nextBlock = self.road.pop(0)
                self.defineDirection()
            else:
                self.finished = True

    def defineDirection(self):
        """
        defines direction of the mob
        if nextBlock been changed
        """
        if (self.currentBlock[0] == self.nextBlock[0]
           and self.currentBlock[1] > self.nextBlock[1]):
            self.direction = self.Direction.up
        if (self.currentBlock[0] == self.nextBlock[0]
           and self.currentBlock[1] < self.nextBlock[1]):
            self.direction = self.Direction.down
        if (self.currentBlock[0] > self.nextBlock[0]
           and self.currentBlock[1] == self.nextBlock[1]):
            self.direction = self.Direction.left
        if (self.currentBlock[0] < self.nextBlock[0]
           and self.currentBlock[1] == self.nextBlock[1]):
            self.direction = self.Direction.right

    def getCenter(self):
        """
        returns coordinates of center
        """
        return [self.posx + self.size + 2, self.posy + self.size + 2]

    def getDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
            self.var.money += self.value