class Bond:
    def __init__(self, bead_a, bead_b):
        self.a = bead_a
        self.b = bead_b

    def plot(self, axes, color):
        x = [getattr(self, e).x for e in "ab"]
        y = [getattr(self, e).y for e in "ab"]
        z = [getattr(self, e).z for e in "ab"]
        axes.plot(x, y, z, linestyle = "-", color = color)
