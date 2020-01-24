import numpy as np 
import matplotlib.pyplot as plt

from helper import scale, draw_coordinate_frame


# define screw hole points
dist = 0.1145
screw_holes = np.array([
    [0, 0, 0, 1],
    [dist, 0, 0, 1],
    [0, dist, 0, 1],
    [dist, dist, 0, 1]
])


# import intrinsic parameters
f = open('heli_intrinsics.txt', 'r') 
lines = list()
for i in range(4):
    lines.append(f.readline())
[fx, fy, cx, cy] = [float(line.split()[-1]) for line in lines]


# make camera and perspective projection matrix
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


# import platfrom to camera matrix
T_pc = np.loadtxt('heli_pose.txt')


# load and draw quanser
quanser = plt.imread('quanser.jpg')
plt.imshow(quanser)

# transform and draw screw holes 
points_unscaled = K.dot(P).dot(T_pc).dot(screw_holes.T).T
points_scaled = scale(points_unscaled)
plt.scatter(points_scaled[:,0], points_scaled[:,1])


# draw coordinate frame
draw_coordinate_frame(K.dot(P).dot(T_pc), size=0.1)


plt.show()

