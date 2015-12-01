import unittest
from gameState import gameState
from enemy import Enemy
import json
import os


class Test(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(os.getcwd(), "maps", "default.py")) as f:
            self.road = json.load(f)
        self.state = gameState(road=self.road)

    def tearDown(self):
        pass

    def test_distance(self):
        e = Enemy(self.road, 100, "red", self.state)
        e.posx = -20
        e.posy = -20
        x = 300
        y = 400
        self.assertEqual(gameState.distance(e, x, y), 500)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()