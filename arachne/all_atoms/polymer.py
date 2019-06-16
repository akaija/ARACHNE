class Polymer:
    def __init__(self, monomers):
        self.chain = monomers

    def plot(self, axes, color):
        for monomer in self.chain:
            monomer.plot(axes, color)
