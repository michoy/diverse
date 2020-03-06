import numpy as np

def epipolar_match(Im1, Im2, F, uv1):
    """
    For each point in uv1, finds the matching point in image 2 by
    an epipolar line search.

    Args:
        I1:  (H x W matrix) Grayscale image 1
        I2:  (H x W matrix) Grayscale image 2
        F:   (3 x 3 matrix) Fundamental matrix mapping points in image 1 to lines in image 2
        uv1: (n x 2 array) Points in image 1

    Returns:
        uv2: (n x 2 array) Best matching points in image 2.
    """

    # practical definitions
    height, width = Im2.shape
    uv2 = list()


    # For every point in uv1
    for point in uv1: 

        # get line equation
        point = np.append(point, 1)
        l1, l2, l3 = F @ point      # FIXME: l1 blir veldig liten, og det gir umulige u
        
        # iterate over the points epipolar line and save their similarity scores
        score = dict()
        for v in range(width):
            u = int(-(v*l2 + l3) / l1)
            score[(u,v)] = similarity_score(Im1, Im2, point[0], point[1], u, v)   

        # add point with highest score to uv2
        u, v = min(score, key=score.get)
        uv2.append([u, v])


    return np.array(uv2)


def similarity_score(Im1, Im2, u1: int, v1: int, u2: int, v2: int) -> float:
    """
    Calculates a similarity score using SSD.
    A low score means high similarity
    """

    d = 10
    height, width = Im2.shape

    # check if point will end up out of bounds
    if u1+d > height or u1-d < 0 or u2+d > height or u2-d < 0:
        return np.inf
    if v1+d > width or v1-d < 0 or v2+d > width or v2-d < 0:
        return np.inf

    # calculate sum of square difference
    score = 0
    for du in range(-d, d):
        for dv in range(-d, d):
            diff = Im1[int(u1+du), int(v1+dv)] - Im2[int(u2+du), int(v2+dv)]
            score += diff**2

    return score
