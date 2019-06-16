class Monomer:
    def __init__(self, atoms, bonds):
        self.atoms = atoms
        self.bonds = bonds

    def plot(self, axes, color):
        for bond in self.bonds:
            bond.plot(axes, color)
