import matplotlib.pyplot as plt
import numpy as np
from common import draw_frame

def estimate_H(xy, XY):
    #
    # Task 2: Implement estimate_H
    #

    A = []
    
    for i in range(len(xy)):

        x = xy[i][0]
        y = xy[i][1]
        X = XY[i][0]
        Y = XY[i][1]
        
        A.append([X, Y, 1, 0, 0, 0, -X*x, -Y*x, -x])
        A.append([0, 0, 0, X, Y, 1, -X*y, -Y*y, -y])
    
    A = np.array(A)

    (_u, _s, vh) = np.linalg.svd(A)

    H = np.array([
        vh[-1][0:3],
        vh[-1][3:6],
        vh[-1][6:9]
    ])

    return H

def decompose_H(H):
    #
    # Task 3a: Implement decompose_H
    #

    # find scaling factor and scale 
    scaling_factor = np.linalg.norm(H[0][:])
    T1 = H / scaling_factor
    T2 = H / scaling_factor * (-1)

    # Compute thrid rotational vector and insert it into H
    T1_r3 = np.cross(T1[0][:], T1[1][:])
    T1 = np.insert(T1, 2, T1_r3, axis=1)
    
    T2_r3 = np.cross(T2[0][:], T2[1][:])
    T2 = np.insert(T2, 2, T2_r3, axis=1)

    # Homogenify
    T1 = np.insert(T1, 3, [0,0,0,1], axis=0)
    T2 = np.insert(T2, 3, [0,0,0,1], axis=0)

    return T1, T2

def choose_solution(T1, T2):
    #
    # Task 3b: Implement choose_solution
    #

    tz = T1[2,3]

    if tz > 0:
        return T1
    else:
        return T2


K           = np.loadtxt('data/cameraK.txt')
all_markers = np.loadtxt('data/markers.txt')
XY          = np.loadtxt('data/model.txt')
n           = len(XY)

for image_number in range(23):
    I = plt.imread('data/video%04d.jpg' % image_number)
    markers = all_markers[image_number,:]
    markers = np.reshape(markers, [n, 3])
    matched = markers[:,0].astype(bool) # First column is 1 if marker was detected
    uv = markers[matched, 1:3] # Get markers for which matched = 1

    # Convert pixel coordinates to normalized image coordinates
    xy = (uv - K[0:2,2])/np.array([K[0,0], K[1,1]])

    H = estimate_H(xy, XY[matched, :2])
    T1,T2 = decompose_H(H)
    T = choose_solution(T1, T2)

    # Compute predicted corner locations using model and homography
    uv_hat = (K@H@XY.T)
    uv_hat = (uv_hat/uv_hat[2,:]).T

    plt.clf()
    plt.imshow(I, interpolation='bilinear')
    draw_frame(K, T, scale=7)
    plt.scatter(uv[:,0], uv[:,1], color='red', label='Observed')
    plt.scatter(uv_hat[:,0], uv_hat[:,1], marker='+', color='yellow', label='Predicted')
    plt.legend()
    plt.xlim([0, I.shape[1]])
    plt.ylim([I.shape[0], 0])
    plt.savefig('data/out%04d.png' % image_number)
