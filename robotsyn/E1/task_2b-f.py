from numpy import array, sin, cos, loadtxt, sqrt, deg2rad
from matplotlib import pyplot as plt 

from helper import scale, draw_coordinate_frame, translate, rotate_x, rotate_y, rotate_z


# define screw hole points
screw_hole_dist = 0.1145
screw_holes = array([
    [0, 0, 0, 1],
    [screw_hole_dist, 0, 0, 1],
    [0, screw_hole_dist, 0, 1],
    [screw_hole_dist, screw_hole_dist, 0, 1]
])


# import intrinsic parameters
f = open('heli_intrinsics.txt', 'r') 
lines = list()
for i in range(4):
    lines.append(f.readline())
[fx, fy, cx, cy] = [float(line.split()[-1]) for line in lines]


# make camera and perspective projection matrix
K = array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])
P = array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
])


# import platfrom to camera matrix
T_platform_camera = loadtxt('robotsyn/E1/heli_pose.txt')


# load and draw quanser
quanser = plt.imread('robotsyn/E1/quanser.jpg')
plt.imshow(quanser)

# transform and draw screw holes 
points_unscaled = K.dot(P).dot(T_platform_camera).dot(screw_holes.T).T
points_scaled = scale(points_unscaled)
plt.scatter(points_scaled[:,0], points_scaled[:,1])


# draw coordinate frame
draw_coordinate_frame(K.dot(P).dot(T_platform_camera))


""" Rotations and translations """

# Task 2c
psi = deg2rad(11.77)

T1 = translate(screw_hole_dist / 2, screw_hole_dist / 2, 0)
R1 = rotate_z(psi)

T_base_platform = T1.dot(R1)

draw_coordinate_frame(K.dot(P)
                        .dot(T_platform_camera)
                        .dot(T_base_platform))


# Task 2d
theta = deg2rad(28.87)

T2 = translate(0, 0, 0.325)
R2 = rotate_y(theta)

T_hinge_base = T2.dot(R2)

draw_coordinate_frame(K.dot(P)
                        .dot(T_platform_camera)
                        .dot(T_base_platform)
                        .dot(T_hinge_base))

T_arm_hinge = translate(0, 0, -0.0552)

draw_coordinate_frame(K.dot(P)
                        .dot(T_platform_camera)
                        .dot(T_base_platform)
                        .dot(T_hinge_base)
                        .dot(T_arm_hinge))


# Task 2e
phi = deg2rad(-0.5)

T3 = translate(0.653, 0, -0.0312)
R3 = rotate_x(phi)

T_rotors_arm = T3.dot(R3)

draw_coordinate_frame(K.dot(P)
                        .dot(T_platform_camera)
                        .dot(T_base_platform)
                        .dot(T_hinge_base)
                        .dot(T_arm_hinge)
                        .dot(T_rotors_arm))


# Tassk 2f
heli_points = loadtxt('heli_points.txt')

T_arm_image = (K.dot(P)
                    .dot(T_platform_camera)
                    .dot(T_base_platform)
                    .dot(T_hinge_base)
                    .dot(T_arm_hinge))

T_rotors_image = (K.dot(P)
                        .dot(T_platform_camera)
                        .dot(T_base_platform)
                        .dot(T_hinge_base)
                        .dot(T_arm_hinge)
                        .dot(T_rotors_arm))

for i in range(3):
    point = scale(T_arm_image.dot(heli_points[i].T).T)
    plt.scatter(point[0], point[1], color='yellow')

for i in range(3, 7):
    point = scale(T_rotors_image.dot(heli_points[i].T).T)
    plt.scatter(point[0], point[1], color='yellow')


plt.show()
