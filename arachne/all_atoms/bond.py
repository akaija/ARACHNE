class Bond:
    def __init__(self, atom_a, atom_b):
        self.a = atom_a
        self.b = atom_b

    def plot(self, axes, color):
        x = [getattr(self, e).x for e in "ab"]
        y = [getattr(self, e).y for e in "ab"]
        z = [getattr(self, e).z for e in "ab"]
        axes.plot(x, y, z, linestyle = "-", color = color)
