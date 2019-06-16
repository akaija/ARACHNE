class Atom:
    def __init__(self, atom_id, atom_type, charge, x_coord, y_coord, z_coord):
        self.id = atom_id
        self.type = atom_type
        self.q = charge
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord

    def plot(self, axes, color):
        axes.scatter(self.x, self.y, self.z, color=color)
