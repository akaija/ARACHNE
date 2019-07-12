import numpy as np

class Atom:
    def __init__(self, bead_id, bead_type, charge, x_coord, y_coord, z_coord):
        self.id = bead_id
        self.type = bead_type
        self.q = charge
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord

    def plot(self, axes):
        if self.type == "SC1" or self.type == "C1":
            color = "lightgreen"
        elif self.type == "SP1":
            color = "red"
        elif self.type == "Na":
            color = "purple"
        else:
            print("BEAD TYPE NOT RECOGNIZED, USING DEFAULT COLOR.")
            color = "black"
        r = 1.75
        u = np.linspace(0, 2 * np.pi, 24)
        v = np.linspace(0, np.pi, 24)
        x = r * np.outer(np.cos(u), np.sin(v)) + self.x
        y = r * np.outer(np.sin(u), np.sin(v)) + self.y
        z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + self.z
        axes.plot_surface(x, y, z, color=color, alpha=0.2)
