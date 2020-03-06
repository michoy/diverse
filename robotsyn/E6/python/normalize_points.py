import numpy as np

def normalize_points(pts):
    """ 
    Computes a normalizing transformation of the points such that
    the points are centered at the origin and their mean distance from
    the origin is equal to sqrt(2).

    See HZ, Ch. 4.4.4: Normalizing transformations (p107).

    Args:
        pts:    Input 2D point array of shape n x 2

    Returns:
        pts_n:  Normalized 2D point array of shape n x 2
        T:      The normalizing transformation in 3x3 matrix form, such
                that for a point (x,y), the normalized point (x',y') is
                found by multiplying T with the point:

                    |x'|       |x|
                    |y'| = T * |y|
                    |1 |       |1|
    """

    # calculate normalization constants
    centroid = np.mean(pts, axis=0, dtype='float64')
    sigma = np.mean([np.linalg.norm(x - centroid) for x in pts])

    # Create transformation
    a = (np.sqrt(2) / sigma)
    T = np.array([
        [a, 0, -a*centroid[0]],
        [0, a, -a*centroid[1]],
        [0, 0, 1]
    ])

    # calculate normalized points from homogenous points
    pts_n = T @ np.column_stack((pts, np.ones(len(pts)))).T
    pts_fin = pts_n[0:3, :].T

    return pts_fin, T
