import random
from pyglet.shapes import Rectangle

from flappy import Grid

class Pipe:
    GAP_HEIGHT = 2
    WIDTH = 1
    COLOR = (0, 255, 0)

    def __init__(self, x=0, y=None, batch=None):
        self.cleared = False
        y = y or random.choice(range(self.GAP_HEIGHT, Grid.rows - self.GAP_HEIGHT))
        pos_x = Grid.width + Grid.x(x)
        gap_y = Grid.y(y)
        gap_h = Grid.x(self.GAP_HEIGHT)
        width = Grid.y(self.WIDTH)
        self.lower = Rectangle(
            pos_x, 0, width, gap_y,
            color=self.COLOR, batch=batch,
        )
        self.upper = Rectangle(
            pos_x, gap_y + gap_h, width, Grid.height - gap_y - gap_h,
            color=self.COLOR, batch=batch,
        )
        self.rects = [self.lower, self.upper]

    def scroll(self, x):
        self.lower.x -= x
        self.upper.x -= x

    def resize(self):
        for r in self.rects:
            r.width = Grid.y(self.WIDTH)

    @property
    def x(self):
        return self.lower.x

    @property
    def width(self):
        return self.lower.width

    def is_offscreen(self):
        return (self.x + self.width) < 0

    def collides(self, position):
        x, y = position
        if x < self.x or x > (self.x + self.width):
            return False
        if y > self.lower.height and y < self.upper.y:
            return False
        return True
