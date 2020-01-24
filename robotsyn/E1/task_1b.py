import numpy as np 
from numpy import sin, cos
import matplotlib.pyplot as plt

box = np.loadtxt('box.txt')

c_x = 320
c_y = 240
f_x = 1000
f_y = 1100

t_z = 6.0

# Word fram to camera frame transform
T_z = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, t_z],
    [0, 0, 0, 1],
])

proj = np.array([
    [f_x, 0, 0, 0],
    [0, f_y, 0, 0],
    [0, 0, 1, 0],
])

shift = np.array([
    [1, 0, c_x],
    [0, 1, c_y],
    [0, 0, 1],
])

T = shift.dot(proj).dot(T_z)


# apply transform
box_fin = np.array(list(map(lambda p: [p[0]/p[2], p[1]/p[2], 1], T.dot(box.T).T)))


# Show image
plt.scatter(box_fin[:, 0], box_fin[:, 1])
plt.xlim([0, 640])
plt.ylim([480, 0]) # <---- flipped arguments
plt.show()
