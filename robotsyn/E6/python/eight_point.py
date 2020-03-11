import numpy as np
from normalize_points import *

def eight_point(uv1, uv2):
    """ Given n >= 8 point matches, (u1 v1) <-> (u2 v2), compute the
    fundamental matrix F that satisfies the equations

        (u2 v2 1)^T * F * (u1 v1 1) = 0

    Args:
        uv1: (n x 2 array) Pixel coordinates in image 1.
        uv2: (n x 2 array) Pixel coordinates in image 2.

    Returns:
        F:   (3 x 3 matrix) Fundamental matrix mapping points in image 1
             to lines in image 2.

    See HZ Ch. 11.2: The normalized 8-point algorithm (p.281).
    """

    # normalize points
    uv1, T1 = normalize_points(uv1)
    uv2, T2 = normalize_points(uv2)

    # make data matrix A from uv1 and uv2
    x = uv1[:,0]
    y = uv1[:,1]
    xm = uv2[:,0]
    ym = uv2[:,1]
    ones = uv1[:,2]
    A = np.array([xm*x, xm*y, xm, ym*x, ym*y, ym, x, y, ones]).T

    # singular value decomposition
    U, s, Vh = np.linalg.svd(A)

    # desired solution f is col of vh corresponding to smallest sigular value
    f = Vh[-1]

    # reshape f to a (3,3) matrix
    F = np.reshape(f, (3,3))

    # calculate new F that satisfies the fundamental matrix properties
    F =  closest_fundamental_matrix(F)
    
    # denormalize
    F = T1.T @ F @ T2

    return F


def closest_fundamental_matrix(F):
    """
    Computes the closest fundamental matrix in the sense of the
    Frobenius norm. See HZ, Ch. 11.1.1 (p.280).
    """

    # compute sigular value decomposition
    U, s, Vh = np.linalg.svd(F)

    # zero out last part of sigular matrix
    s[-1] = 0
    S = np.diag(s)

    # calculate F that minimizes the Frobenius norm
    F_singular = U @ S @ Vh

    return F_singular
