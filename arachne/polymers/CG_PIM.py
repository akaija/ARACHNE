import copy

import numpy as np

from arachne.utilities import *

def add_monomer_A(monomer, ref, ref_vectors, align_planes):
    old = monomer
    new = copy.deepcopy(monomer)
    head = ref_vectors[0]
    tail = ref_vectors[1]
    tail_atom = get_ref(old, tail[1])
    tail_vector = vector(get_ref(old, tail[0]), tail_atom)
    new_coord = np.array([tail_atom.x, tail_atom.y, tail_atom.z]) + tail_vector
    translate_monomer(new, new_coord, ref)
    rotate_monomer(new, tail_vector, ref, head)
    axis = vector(get_ref(new, head[0]), get_ref(new, head[1]))
    angle = angle_between_planes(old, new, *align_planes)
    rotate_along_axis(new, ref, axis, angle)
    return new

def add_monomer_B(monomer, ref, ref_vectors, align_planes):
    new = add_monomer_A(monomer, ref, ref_vectors, align_planes)
    axis = vector(*[get_ref(new, ref_vectors[0][e]) for e in [0, 1]])
    rotate_along_axis(new, ref, axis, np.pi)
    tail = ref_vectors[1]
    tail_atom = get_ref(monomer, tail[1])
    tail_vector = vector(get_ref(monomer, tail[0]), tail_atom)
    new_coord = np.array([tail_atom.x, tail_atom.y, tail_atom.z]) + tail_vector
    translate_monomer(new, new_coord, ref)
    return new

def add_monomer_C(monomer, ref, ref_vectors, align_planes):
    new = add_monomer_A(monomer, ref, ref_vectors, align_planes)
    a, b, c = align_planes[0]
    reflect(new, ref, a, b, c)
    return new

def add_monomer_D(monomer, ref, ref_vectors, align_planes):
    new = add_monomer_A(monomer, ref, ref_vectors, align_planes)
    a, b, c = align_planes[0]
    reflect(new, ref, a, b, c)
    axis = vector(*[get_ref(new, ref_vectors[0][e]) for e in [0, 1]])
    rotate_along_axis(new, ref, axis, np.pi)
    tail = ref_vectors[1]
    tail_atom = get_ref(monomer, tail[1])
    tail_vector = vector(get_ref(monomer, tail[0]), tail_atom)
    new_coord = np.array([tail_atom.x, tail_atom.y, tail_atom.z]) + tail_vector
    translate_monomer(new, new_coord, ref)
    return new
