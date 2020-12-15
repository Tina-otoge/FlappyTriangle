import logging
from pyglet.graphics import Batch
from pyglet.shapes import Rectangle
from pyglet.window import Window
from pyglet import app, clock, media

from flappy import Grid, Pipe, Player


class Game():
    def __init__(self):
        self.batch = Batch()
        self.background = Rectangle(0, 0, 0, 0)
        self.window = Window()
        self.window.push_handlers(self)
        self.on_resize(self.window.width, self.window.height)
        clock.schedule_interval(self.update, 1 / 60)
        clock.schedule_interval(self.log, 1)
        self.sounds = {
            'fail': media.load('resources/failure.mp3', streaming=False),
            'jump': media.load('resources/jump.wav', streaming=False),
            'score': media.load('resources/score.wav', streaming=False),
        }
        self.reset()

    def log(self, delta):
        logging.info('Current speed: {}'.format(self.speed))
        logging.info('Current score: {}'.format(self.points))

    def reset(self):
        self.pipes = []
        self.points = 0
        self.speed = 2
        self.player = Player(batch=self.batch)
        self.create_pipe()
        self.create_pipe(x=(Grid.columns / 2) + (Pipe.WIDTH / 2))

    def fail(self):
        self.sounds['fail'].play()
        self.reset()

    def create_pipe(self, *args, **kwargs):
        kwargs['batch'] = kwargs.get('batch', self.batch)
        self.pipes.append(Pipe(*args, **kwargs))

    def update(self, delta):
        self.player.update(delta)
        self.speed += delta * 0.1
        delta_x = delta * Grid.x() * self.speed
        if self.player.is_offscreen():
            self.fail()
            return
        for pipe in self.pipes:
            pipe.scroll(delta_x)
            if pipe.is_offscreen():
                self.pipes.remove(pipe)
                self.create_pipe()
            if pipe.collides(self.player.center):
                self.fail()
            if self.player.cleared(pipe):
                self.score()

    def score(self):
        self.sounds['score'].play()
        self.points += 1

    def jump(self):
        logging.info('jumping')
        self.sounds['jump'].play()
        self.player.jump()

    def on_key_press(self, symbol, modifiers):
        self.jump()

    def on_mouse_press(self, x, y, button, modifiers):
        self.jump()

    def on_draw(self):
        self.window.clear()
        self.background.draw()
        self.batch.draw()

    def on_resize(self, width, height):
        Grid.update_factor(width, height)
        self.background.width, self.background.height = width, height
        if getattr(self, 'player', None):
            self.player.resize()

def run():
    game = Game()
    app.run()
