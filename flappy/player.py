from pyglet import image
from pyglet.sprite import Sprite

from flappy import Grid

class Player:
    SCALE = 0.4

    def __init__(self, x=1, y=4, batch=None):
        self.image = image.load('resources/triangle.png')
        self.sprite = Sprite(self.image, Grid.x(x), Grid.y(y), batch=batch)
        self.resize()
        self.speed = -1

    def resize(self):
        self.sprite.scale_x = Grid.x(self.SCALE) / self.image.width
        self.sprite.scale_y = Grid.y(self.SCALE) / self.image.height

    def update(self, delta):
        self.sprite.y += Grid.y(self.speed) * delta
        self.speed -= 0.1

    def jump(self):
        self.speed = 3

    @property
    def center(self):
        return (
            self.sprite.x + (self.sprite.width / 2),
            self.sprite.y + (self.sprite.height / 2)
        )

    def is_offscreen(self):
        return (
            self.sprite.x < 0 or
            self.sprite.x + self.sprite.width > Grid.width or
            self.sprite.y < 0 or
            self.sprite.y + self.sprite.height > Grid.height
        )

    def cleared(self, pipe):
        if pipe.cleared:
            return False
        result = pipe.x + pipe.WIDTH < self.center[0]
        pipe.cleared = result
        return result
