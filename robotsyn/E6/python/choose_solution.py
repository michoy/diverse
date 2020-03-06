import numpy as np
from linear_triangulation import *
from camera_matrices import *

def choose_solution(uv1, uv2, K1, K2, Rts):
    """
    Chooses among the rotation and translation solutions Rts
    the one which gives the most points in front of both cameras.

    RTs:
        Solution 1
            R (3x3)
            t (3,)
        Solution 2
            ...

    """

    NUM_OF_CORRESPONDENCES = 3

    soln = 0
    solution_score = dict()

    for R, t in Rts:

        P1,P2 = camera_matrices(K1, K2, R, t)
        
        for i in range(NUM_OF_CORRESPONDENCES):
            x_1 = linear_triangulation(uv1[i], uv2[i], P1, P2)
            x_2 = linear_triangulation(uv2[i], uv1[i], P2, P1) # x from perspective of image 2

            if x_1[2] > 0 and x_2[2] > 0:
                solution_score[soln] = solution_score.get(soln, 0) + 1
                
        soln = soln + 1

    # select solution with the most hits
    best_solution = max(solution_score, key=solution_score.get)
    print('Choosing solution %d' % best_solution)

    return Rts[best_solution]
