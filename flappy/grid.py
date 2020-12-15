import logging

class GridUninitializedException(Exception):
    pass

class Grid:
    cell_width = None
    cell_height = None
    height = None
    width = None
    columns = 12
    rows = 10
    initialized = False

    def __init__(self, x=1, y=1):
        if not self.initialized:
            raise GridUninitializedException()
        self.x = x * self.cell_height
        self.y = y * self.cell_width

    def __str__(self):
        if not self.initialized:
            raise GridUninitializedException()
        return 'Cells {0.cell_width}:{0.cell_height} | Size {0.height}:{0.width}'.format(self)

    @classmethod
    def update_factor(cls, x, y):
        cls.initialized = True
        cls.width, cls.height = x, y
        cls.cell_width = x // cls.columns
        cls.cell_height = y // cls.rows
        logging.info('Updated grid, Cell {cw}:{ch} | Size {ww}:{wh}'.format(
            cw=cls.cell_width, ch=cls.cell_width,
            ww=cls.width, wh=cls.height
        ))

    @classmethod
    def x(cls, i=1):
        if not cls.initialized:
            raise GridUninitializedException()
        return cls.cell_width * i

    @classmethod
    def y(cls, i=1):
        if not cls.initialized:
            raise GridUninitializedException()
        return cls.cell_height * i

    @classmethod
    def px(cls, percent=1):
        return (percent / 100) * cls.width

    @classmethod
    def py(cls, percent=1):
        return (percent / 100) * cls.height
