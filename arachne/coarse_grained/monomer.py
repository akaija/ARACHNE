class CG_Monomer:
    def __init__(self, atoms, bonds):
        self.atoms = atoms
        self.bonds = bonds

    def plot(self, axes, color, beads="off"):
        if beads != "off":
            for atom in self.atomss:
                atom.plot(axes)
        for bond in self.bonds:
            bond.plot(axes, color)
