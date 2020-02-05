import numpy as np 
import matplotlib.pyplot as plt 

fx = 9.842439e+02
cx = 6.900000e+02
fy = 9.808141e+02
cy = 2.331966e+02
k1 = -3.728755e-01
k2 = 2.037299e-01
p1 = 2.219027e-03
p2 = 1.383707e-03
k3 = -7.233722e-02


def u_trans(x: float, y: float) -> int: 
    r = np.linalg.norm([x, y])
    dx = (k1*r**2 + k2*r**4 + k3*r**6)*x + 2*p1*x*y + p2*(r**2 + 2*x**2)
    return int(round(cx + fx * (x + dx)))

def v_trans(x: float, y: float) -> int:
    r = np.linalg.norm([x, y])
    dy = (k1*r**2 + k2*r**4 + k3*r**6)*y + 2*p2*x*y + p1*(r**2 + 2*y**2)
    return int(round(cy + fy*(y + dy)))

T1 = np.array([
    [1/fx, 0, -cx/fx],
    [0, 1/fy, -cy/fy],
])

img_src = plt.imread('robotsyn/E2/kitti.jpg')
img_undist = np.empty(img_src.shape, dtype=np.uint8)


for v_dst in range(img_src.shape[0]):
    for u_dst in range(img_src.shape[1]):

        # transform to x, y
        vec = np.array([u_dst, v_dst, 1])
        (x, y) = T1.dot(vec.T).T

        # map to distored image coordinates
        v_src = v_trans(x, y)
        u_src = u_trans(x, y)

        # fill undistored image
        img_undist[v_dst, u_dst] = img_src[v_src, u_src]

plt.imshow(img_undist)
plt.imsave('undist.png', img_undist)
plt.show()
