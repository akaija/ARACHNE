from parse import parse

import yaml

from arachne.all_atoms.atom import Atom
from arachne.all_atoms.bond import Bond
from arachne.errors import WrongNumberOfAtoms

def read_config(file_path):
    with open(file_path) as f:
        return yaml.load(f)

def read_file(file_path):
    with open(file_path) as f:
        return f.read().splitlines()

def get_number(lines, string):
    for line in lines:
        r = parse("{:s}{number}{:s}" + "{}".format(string), line)
        if r != None:
            return int(r["number"])

def get_block(lines, title):
    start = 0
    for line in lines:
        if title in line:
            break
        start += 1
    end = start
    for line in lines[start + 1:]:
        if parse("{:l}", line) != None:
            break
        end += 1
    return [e for e in lines[start + 1:end] if e != ""]

def parse_atoms(lines):
    atom_count = get_number(lines, "atoms")
    lines = get_block(lines, "Atoms")
    atom_format = "{:s}{id}{:s}{:d}{:s}{:d}{:s}{q}{:s}{x}{:s}{y}{:s}{z}{:s}#{:s}{type}"
    atoms = []
    for line in lines:
        r = parse(atom_format, line)
        atoms.append(Atom(int(r["id"]), r["type"], *[float(r[e]) for e in "qxyz"]))
    # Make a proper exception!
    if len(atoms) != atom_count:
        print("There appears to be a mismatch between the number of atoms listed in the header")
        print("and the actual number of atoms defined. Please review monomer definitions.")
    else:
        return atoms

def parse_bonds(lines, atoms):
    bond_count = get_number(lines, "bonds")
    lines = get_block(lines, "Bonds")
    bond_format = "{:s}{:d}{:s}{:d}{:s}{atom_a}{:s}{atom_b}{:s}#{:s}{:S}"
    bonds = []
    for line in lines:
        r = parse(bond_format, line)
        for atom in atoms:
            if atom.id == int(r["atom_a"]):
                atom_a = atom
            elif atom.id == int(r["atom_b"]):
                atom_b = atom
        bonds.append(Bond(atom_a, atom_b))
    if len(bonds) != bond_count:
        print("There appears to be a mismatch between the number of bonds listed in the header")
        print("and the actual number of bonds defined. Please review monomer definitions.")
    else:
        return bonds

def parse_data(file_path):
    lines = read_file(file_path)
    atoms = parse_atoms(lines)
    bonds = parse_bonds(lines, atoms)
    return atoms, bonds
