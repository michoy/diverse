import numpy as np 
from numpy import cos, sin
import matplotlib.pyplot as plt 


def scale(points_homogenous):
    """ 
    Scales coordinates by the homogenous part. 
    Returns a numpy array of normalized homogenous coordinates.
    """

    if len(points_homogenous.shape) < 2:
        p = points_homogenous
        return [p[0]/p[2], p[1]/p[2], 1]

    else:
        return np.array(list(map(lambda p: [p[0]/p[2], p[1]/p[2], 1], points_homogenous)))


def draw_coordinate_frame(T, size=0.05, linewidth=2.5, zorder=1):

    basic_frame = np.array([
        [size, 0, 0, 1],
        [0, size, 0, 1],
        [0, 0, size, 1]
    ])

    origo = np.array([
        [0, 0, 0, 1]
    ])

    origo_trans = scale(T.dot(origo.T).T)
    frame_trans = scale(T.dot(basic_frame.T).T)

    plt.plot([origo_trans[0][0], frame_trans[0][0]], [origo_trans[0][1], frame_trans[0][1]], 
            color='red', zorder=zorder, linewidth=linewidth)
    plt.plot([origo_trans[0][0], frame_trans[1][0]], [origo_trans[0][1], frame_trans[1][1]], 
            color='yellow', zorder=zorder, linewidth=linewidth)
    plt.plot([origo_trans[0][0], frame_trans[2][0]], [origo_trans[0][1], frame_trans[2][1]], 
            color='blue', zorder=zorder, linewidth=linewidth)



def translate(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],
    ])

def rotate_x(rads):
    return np.array([
        [1, 0, 0, 0],
        [0, cos(rads), -sin(rads), 0],
        [0, sin(rads), cos(rads), 0],
        [0, 0, 0, 1],
    ])

def rotate_y(rads):
    return np.array([
        [cos(rads), 0, sin(rads), 0],
        [0, 1, 0, 0],
        [-sin(rads), 0, cos(rads), 0],
        [0, 0, 0, 1],
    ])

def rotate_z(rads):
    return np.array([
        [cos(rads), -sin(rads), 0, 0],
        [sin(rads), cos(rads), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])



