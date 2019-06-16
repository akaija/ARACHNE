import copy

import numpy as np

from arachne.utilities import *

def add_monomer_A(monomer, ref, ref_vectors, bonds):
    old = monomer
    new = copy.deepcopy(monomer)
    head = ref_vectors[0]
    tail = ref_vectors[1]
    tail_atom = get_ref(old, tail[1])
    tail_vector = vector(get_ref(old, tail[0]), tail_atom)
    new_coord = np.array([tail_atom.x, tail_atom.y, tail_atom.z]) + tail_vector
    translate_monomer(new, new_coord, ref)
    rotate_monomer(new, tail_vector, ref, head)
    ab = vector(*[get_ref(old, bonds[e][1]) for e in [0, 1]])
    cd = [bonds[0][0], bonds[1][0]]
    rotate_monomer(new, ab, ref, cd)
    return new

def add_monomer_B(monomer, ref, ref_vectors, bonds):
    new = add_monomer_A(monomer, ref, ref_vectors, bonds)
    axis = vector(*[get_ref(new, ref_vectors[0][e]) for e in [0, 1]])
    rotate_180(new, ref, axis)
    tail = ref_vectors[1]
    tail_atom = get_ref(monomer, tail[1])
    tail_vector = vector(get_ref(monomer, tail[0]), tail_atom)
    new_coord = np.array([tail_atom.x, tail_atom.y, tail_atom.z]) + tail_vector
    translate_monomer(new, new_coord, bonds[1][0])
    return new

def add_monomer_C(monomer, ref, ref_vectors, bonds):
    new = add_monomer_A(monomer, ref, ref_vectors, bonds)
    a, b = ref_vectors[0]
    c = bonds[1][0]
    reflect(new, ref, a, b, c)
    return new

def add_monomer_D(monomer, ref, ref_vectors, bonds):
    new = add_monomer_A(monomer, ref, ref_vectors, bonds)
    a, b = ref_vectors[0]
    c = bonds[1][0]
    reflect(new, ref, a, b, c)
    axis = vector(*[get_ref(new, ref_vectors[0][e]) for e in [0, 1]])
    rotate_180(new, ref, axis)
    tail = ref_vectors[1]
    tail_atom = get_ref(monomer, tail[1])
    tail_vector = vector(get_ref(monomer, tail[0]), tail_atom)
    new_coord = np.array([tail_atom.x, tail_atom.y, tail_atom.z]) + tail_vector
    translate_monomer(new, new_coord, bonds[1][0])
    return new
