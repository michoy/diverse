import numpy as np 
from numpy import cos, sin
import matplotlib.pyplot as plt 

from helper import scale, draw_coordinate_frame

# task 1c: T_o_c = T_z * R_x * R_y


""" define rotations """

theta = np.pi / 6.0

R_x = np.array([
    [1, 0, 0, 0],
    [0, cos(theta), -sin(theta), 0],
    [0, sin(theta), cos(theta), 0],
    [0, 0, 0, 1],
])

R_y = np.array([
    [cos(theta), 0, sin(theta), 0],
    [0, 1, 0, 0],
    [-sin(theta), 0, cos(theta), 0],
    [0, 0, 0, 1],
])

R_z = np.array([
    [cos(theta), -sin(theta), 0, 0],
    [sin(theta), cos(theta), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])

R = R_x.dot(R_y)


""" define projection and camera matrix """

cx=320 
cy=240
fx=1000
fy=1100
tz=6.0

K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])
P = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
])
T_z = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, tz],
    [0, 0, 0, 1],
])


""" Apply transformations and draw """

box = np.loadtxt('box.txt')
T = K.dot(P).dot(T_z).dot(R)

draw_coordinate_frame(T, size=0.5)

box_trans_unscaled = T.dot(box.T).T
box_trans = scale(box_trans_unscaled)
plt.scatter(box_trans[:,0], box_trans[:,1])

plt.xlim([0, 640])
plt.ylim([480, 0]) # <---- flipped arguments

plt.show()

