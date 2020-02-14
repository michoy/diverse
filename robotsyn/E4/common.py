import numpy as np
import matplotlib.pyplot as plt

K                  = np.loadtxt('data/cameraK.txt')
p_model            = np.loadtxt('data/model.txt')
platform_to_camera = np.loadtxt('data/pose.txt')

def calculate_residuals(uv, weights, yaw, pitch, roll):

    # Helicopter model from Exercise 1 (you don't need to modify this).
    base_to_platform = translate(0.1145/2, 0.1145/2, 0.0)@rotate_z(yaw)
    hinge_to_base    = translate(0, 0, 0.325)@rotate_y(pitch)
    arm_to_hinge     = translate(0, 0, -0.0552)
    rotors_to_arm    = translate(0.653, 0, -0.0312)@rotate_x(roll)

    base_to_camera   = platform_to_camera@base_to_platform
    hinge_to_camera  = base_to_camera@hinge_to_base
    arm_to_camera    = hinge_to_camera@arm_to_hinge
    rotors_to_camera = arm_to_camera@rotors_to_arm

    # Create projection matrix
    P = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
    ])
    
    # Generate marker coordinate estimates given "theta" values
    markers_c = np.array([
        K @ P @ arm_to_camera @ p_model[0],
        K @ P @ arm_to_camera @ p_model[1],
        K @ P @ arm_to_camera @ p_model[2],
        K @ P @ rotors_to_camera @ p_model[3],
        K @ P @ rotors_to_camera @ p_model[4],
        K @ P @ rotors_to_camera @ p_model[5],
        K @ P @ rotors_to_camera @ p_model[6]
    ])

    # Scale est. marker coordinates with their homogenous part
    u_hat = homogenous_to_euclidean(markers_c)

    # Subtrakt observed marker coordinates from the ones estimated and 
    # calculate their euclidean distances, called residuals
    residuals = np.linalg.norm(u_hat-uv, axis=1) 

    # Set all residuals without observed marker to 0
    return residuals * weights


def normal_equations(uv, weights, yaw, pitch, roll):
    epsilon = 0.00001

    residuals = calculate_residuals(uv, weights, yaw, pitch, roll)

    diff_yaw = calculate_residuals(uv, weights, yaw+epsilon, pitch, roll) - residuals
    diff_pitch = calculate_residuals(uv, weights, yaw, pitch+epsilon, roll) - residuals
    diff_roll = calculate_residuals(uv, weights, yaw, pitch, roll+epsilon) - residuals

    jacobi = np.array([diff_yaw, diff_pitch, diff_roll]).T / epsilon

    JTJ = jacobi.T @ jacobi
    JTr = jacobi.T @ residuals

    return JTJ, JTr


def gauss_newton(uv, weights, yaw, pitch, roll):
    max_iter = 100
    step_size = 0.25

    theta = np.array([yaw, pitch, roll]).T

    for iter in range(max_iter):
        JTJ, JTr = normal_equations(uv, weights, theta[0], theta[1], theta[2])
        delta = np.linalg.solve(JTJ, -JTr)
        theta = theta + step_size * delta

    return theta[0], theta[1], theta[2]


def levenberg_marquardt(uv, weights, yaw, pitch, roll):
    max_iter = 100
    step_size = 0.25
    lamb = 0.001
    tolerance = 0.001
    iter_count = 0

    theta = np.array([yaw, pitch, roll]).T
    log = list()

    for iter in range(max_iter):
        iter_count = iter_count + 1

        JTJ, JTr = normal_equations(uv, weights, theta[0], theta[1], theta[2])
        delta = np.linalg.solve((JTJ + lamb*np.eye(3)), -JTr)
        theta_new = theta + step_size * delta
        log.append([*theta_new.tolist(), lamb])

        if np.linalg.norm(theta_new - theta) < tolerance:
            theta = theta_new
            break

        residual_old = np.sum(calculate_residuals(uv, weights, theta[0], theta[1], theta[2]))
        residual_new = np.sum(calculate_residuals(uv, weights, theta_new[0], theta_new[1], theta_new[2]))

        if residual_new < residual_old:
            lamb = lamb / 10
        else: 
            lamb = lamb * 10

        theta = theta_new

    # print('Levenberg-Marquardt iterations: %d' % iter_count)

    # log = np.array(log)
    # plt.plot(log[:,0], label='yaw')
    # plt.plot(log[:,1], label='pitch')
    # plt.plot(log[:,2], label='roll')
    # plt.legend()
    # plt.show()

    # plt.plot(log[:,3], label='lambda')
    # plt.legend()
    # plt.show()

    return theta[0], theta[1], theta[2]


def rotate_x(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c,-s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

def rotate_y(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c, 0, s, 0],
                     [ 0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [ 0, 0, 0, 1]])

def rotate_z(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c,-s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def translate(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]])


def homogenous_to_euclidean(coordinates):
    scale = lambda X: [X[0]/X[-1], X[1]/X[-1]]
    return np.array(list(map(scale, coordinates)))
