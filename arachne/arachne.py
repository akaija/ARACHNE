from math import sqrt

import numpy as np

from arachne.files import parse_data
from arachne.all_atoms.monomer import Monomer
from arachne.coarse_grained.monomer import CG_Monomer
from arachne.all_atoms.polymer import Polymer
from arachne.plotting import annotated_plot, plot_polymers, plot_CG_monomer
from arachne.polymers import PIM, CG_PIM
from arachne.utilities import coarse_grain, translate_monomer, rotate_monomer, distance

def view_monomer(config):
    monomer = Monomer(*parse_data(config["monomer_path"]))
    annotated_plot(monomer, "k")

def view_CG_monomer(config):
    AA_monomer = Monomer(*parse_data(config["monomer_path"]))
    CG_monomer = CG_Monomer(*coarse_grain(AA_monomer, config["beads"], config["bead_bonds"]))
    plot_CG_monomer(AA_monomer, CG_monomer)

def all_atom_polymer(config):
    monomer = Monomer(*parse_data(config["monomer_path"]))
    atoms, bonds = [], []
    for atom in monomer.atoms:
        if atom.id not in config["omit_atoms"]:
            atoms.append(atom)
    for bond in monomer.bonds:
        if bond.a.id not in config["omit_atoms"] and bond.b.id not in config["omit_atoms"]:
            bonds.append(bond)
    polymers = []
    while len(polymers) < config["number_of_chains"]:
        monomers = []
        try:
            print("Adding chain : {}".format(len(polymers) + 1))
            starting_monomer = Monomer(atoms, bonds)
            coord = np.array([np.random.uniform(- config["starting_box"] / 2,
                config["starting_box"] / 2) for e in range(3)])
            translate_monomer(starting_monomer, coord, config["reference_atom"])
            rotate_monomer(starting_monomer, 
                    np.array([np.random.random() for e in range(3)]),
                    config["reference_atom"], config["reference_vectors"][0])
            monomers.append(starting_monomer)
            while len(monomers) < config["repeat_units"]:
                a = PIM.add_monomer_A(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["bonds"])
                b = PIM.add_monomer_B(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["bonds"])
                c = PIM.add_monomer_C(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["bonds"])
                d = PIM.add_monomer_D(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["bonds"])
                potential_monomers = []
                if config["buffer"] == 0:
                    potential_monomers = [a, b, c, d]
                else:
                    for new_monomer in [a, b, c, d]:
                        distances = []
                        for new_atom in new_monomer.atoms:
                            for old_monomer in monomers:
                                for old_atom in old_monomer.atoms:
                                    distances.append(distance(new_atom, old_atom))
                        if min(distances) >= config["buffer"]:
                            potential_monomers.append(new_monomer)
                monomers.append(np.random.choice(potential_monomers))
            polymers.append(Polymer(monomers))
        except:
            pass
    plot_polymers(polymers)

def CG_polymer(config):
    AA_monomer = Monomer(*parse_data(config["monomer_path"]))
    polymers = []
    while len(polymers) < config["number_of_chains"]:
        monomers = []
        try:
            print("Adding chain : {}".format(len(polymers) + 1))
            starting_monomer = CG_Monomer(*coarse_grain(AA_monomer, config["beads"], config["bead_bonds"]))
            coord = np.array([np.random.uniform(- config["starting_box"] / 2,
                config["starting_box"] / 2) for e in range(3)])
            translate_monomer(starting_monomer, coord, config["reference_atom"])
            rotate_monomer(starting_monomer, 
                    np.array([np.random.random() for e in range(3)]),
                    config["reference_atom"], config["reference_vectors"][0])
            monomers.append(starting_monomer)
            while len(monomers) < config["repeat_units"]:
                a = CG_PIM.add_monomer_A(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["alignment_planes"])
                b = CG_PIM.add_monomer_B(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["alignment_planes"])
                c = CG_PIM.add_monomer_C(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["alignment_planes"])
                d = CG_PIM.add_monomer_D(monomers[-1], config["reference_atom"],
                    config["reference_vectors"], config["alignment_planes"])
                potential_monomers = []
                if config["buffer"] == 0:
                    potential_monomers = [a, b, c, d]
                else:
                    for new_monomer in [a, b, c, d]:
                        distances = []
                        for new_atom in new_monomer.atoms:
                            for old_monomer in monomers:
                                for old_atom in old_monomer.atoms:
                                    distances.append(distance(new_atom, old_atom))
                        if min(distances) >= config["buffer"]:
                            potential_monomers.append(new_monomer)
                monomers.append(np.random.choice(potential_monomers))
            polymers.append(Polymer(monomers))
        except:
            pass
    plot_polymers(polymers)


