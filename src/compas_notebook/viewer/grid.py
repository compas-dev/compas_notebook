from compas.colors import Color


class Grid:
    def __init__(self, xsize=10, ysize=10, xstep=1, ystep=1, color=None):
        self.xsize = xsize
        self.ysize = ysize
        self.xstep = xstep
        self.ystep = ystep
        self.color = color or Color.from_hex("#cccccc")
