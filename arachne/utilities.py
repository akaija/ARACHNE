import math

import numpy as np

from arachne.coarse_grained.atom import Atom
from arachne.coarse_grained.bond import Bond

def vector(a, b):
    return np.array([b.x, b.y, b.z]) - np.array([a.x, a.y, a.z])

class Vector:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.v = vector(a, b)

def get_ref(monomer, ref):
    for atom in monomer.atoms:
        if atom.id == ref:
            return atom

def get_vectors(monomer, ref):
    vectors = []
    a = get_ref(monomer, ref)
    for b in monomer.atoms:
        vectors.append(Vector(a, b))
    return vectors

def translate_atom(atom, v):
    atom.x += v[0]
    atom.y += v[1]
    atom.z += v[2]

def translate_monomer(monomer, coord, ref):
    a = get_ref(monomer, ref)
    delta = np.array(coord) - np.array([a.x, a.y, a.z])
    for atom in monomer.atoms:
        translate_atom(atom, delta)

def angle(a, b):
    return np.arctan2(np.linalg.norm(np.cross(a, b)), np.dot(a, b))

def normal(a, b):
    return np.cross(a, b)

def rotation_matrix(axis, theta):
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotate(v, a, t):
    return np.dot(rotation_matrix(a, t), np.transpose(v))

def rotate_monomer(monomer, new_vector, ref, ref_vector):
    a = get_ref(monomer, ref)
    old_vector = vector(get_ref(monomer, ref_vector[0]), get_ref(monomer, ref_vector[1]))
    theta = angle(new_vector, old_vector)
    axis = normal(new_vector, old_vector)
    old_vectors = get_vectors(monomer, ref)
    new_vectors = []
    for v in old_vectors:
        new_vectors.append(rotate(v.v, axis, -theta))
    for i in range(len(new_vectors)):
        monomer.atoms[i].x = a.x + new_vectors[i][0]
        monomer.atoms[i].y = a.y + new_vectors[i][1]
        monomer.atoms[i].z = a.z + new_vectors[i][2]

def rotate_along_axis(monomer, ref, axis, angle):
    a = get_ref(monomer, ref)
    old_vectors = get_vectors(monomer, ref)
    new_vectors = []
    for v in old_vectors:
        new_vectors.append(rotate(v.v, axis, angle))
    for i in range(len(new_vectors)):
        monomer.atoms[i].x = a.x + new_vectors[i][0]
        monomer.atoms[i].y = a.y + new_vectors[i][1]
        monomer.atoms[i].z = a.z + new_vectors[i][2]

def magnitude(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

def unit(v):
    return v / magnitude(v)

def dfp(atom, a, b, c, d):
    d_ = a * atom.x + b * atom.y + c * atom.z + d
    e_ = math.sqrt(a ** 2 + b ** 2 + c ** 2)
    return d_ / e_

def reflect(monomer, ref, a0, a1, a2):
    a0 = get_ref(monomer, a0)
    a1 = get_ref(monomer, a1)
    a2 = get_ref(monomer, a2)
    v0 = vector(a0, a1)
    v1 = vector(a0, a2)
    cross = normal(v0, v1)
    a, b, c = cross
    d = -1 * (a * a0.x + b * a0.y + c * a0.z)
    for atom in monomer.atoms:
        distance = dfp(atom, a, b, c, d)
        atom.x -= 2 * unit(cross)[0] * distance
        atom.y -= 2 * unit(cross)[1] * distance
        atom.z -= 2 * unit(cross)[2] * distance

def distance(a0, a1):
    return math.sqrt((a0.x - a1.x) ** 2 + (a0.y - a1.y) ** 2 + (a0.z - a1.z) ** 2)

def coarse_grain(all_atom_monomer, beads, bead_bonds):
    super_atoms, bonds = [], []
    for bead in beads:
        x, y, z, q = 0, 0, 0, 0
        for atom_id in beads[bead]["atoms"]:
            atom = get_ref(all_atom_monomer, atom_id)
            x += atom.x
            y += atom.y
            z += atom.z
            q += atom.q
        x /= len(beads[bead]["atoms"])
        y /= len(beads[bead]["atoms"])
        z /= len(beads[bead]["atoms"])
        super_atoms.append(Atom(bead, beads[bead]["type"], q, x, y, z))
    for bond in bead_bonds:
        for bead in super_atoms:
            if bead.id == bond[0]:
                bead_a = bead
            elif bead.id == bond[1]:
                bead_b = bead
        bonds.append(Bond(bead_a, bead_b))
    return super_atoms, bonds

def angle_between_planes(m0, m1, p0, p1):
    v00 = vector(get_ref(m0, p0[0]), get_ref(m0, p0[1]))
    v01 = vector(get_ref(m0, p0[0]), get_ref(m0, p0[2]))
    v10 = vector(get_ref(m1, p1[0]), get_ref(m1, p1[1]))
    v11 = vector(get_ref(m1, p1[0]), get_ref(m1, p1[2]))
    v0 = normal(v00, v01)
    v1 = normal(v10, v11)
    return angle(v0, v1)
