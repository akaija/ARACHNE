import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def set_axes_equal(ax):
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()
    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])
    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)
    radius = 0.5 * max([x_range, y_range, z_range])
    ax.set_xlim3d([x_middle - radius, x_middle + radius])
    ax.set_ylim3d([y_middle - radius, y_middle + radius])
    ax.set_zlim3d([z_middle - radius, z_middle + radius])

def get_label(id_, atoms):
    for a in atoms:
        if a.id == int(id_):
            return "ID : {}\nType : {}\nq : {}\nx : {}\ny : {}\nz : {}" \
            .format(a.id, a.type, a.q, a.x, a.y, a.z)

def annotated_plot(monomer, color):
    fig = plt.figure()
    ax = fig.gca(projection = "3d")
    dist = [-10, 10]
    zero = [0, 0]
    ax.plot(dist, zero, zero, "-r")
    ax.plot(zero, dist, zero, "-g")
    ax.plot(zero, zero, dist, "-b")
    x, y, z, n, atoms = [], [], [], [], []
    for atom in monomer.atoms:
        x.append(atom.x)
        y.append(atom.y)
        z.append(atom.z)
        n.append(atom.id)
        atoms.append(atom)
    sc = ax.scatter(x, y, z, color=color)
    for bond in monomer.bonds:
        bond.plot(ax, color)
    
    set_axes_equal(ax)
    ax.set_axis_off()

    annot = ax.annotate("ORIGIN", xy=(0, 0), xytext=(20, 20),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"))
    annot.set_visible=(True)

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        id_ = "{}".format(" ".join([str(n[e]) for e in ind["ind"]]))
        annot.set_text(get_label(id_, atoms))
        annot.get_bbox_patch().set_facecolor("r")
        
    def click(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible=(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visiblei=(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("button_press_event", click)

    plt.show()

def plot_polymers(polymers):
    fig = plt.figure()
    ax = fig.gca(projection = "3d")
    dist = [-10, 10]
    zero = [0, 0]
    ax.plot(dist, zero, zero, "-r")
    ax.plot(zero, dist, zero, "-g")
    ax.plot(zero, zero, dist, "-b")
    for polymer in polymers:
        c = np.random.rand(3, )
        polymer.plot(ax, c)
    set_axes_equal(ax)
    ax.set_axis_off()
    plt.show()


