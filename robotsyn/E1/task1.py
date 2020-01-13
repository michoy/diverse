import numpy as np 
import matplotlib.pyplot as plt

# load image
roomba_rgb = plt.imread('robotsyn/E1/roomba.jpg')

# print dimensions
(height, width) = roomba_rgb.shape[0:2]
print('height: ', height)
print('width:  ', width)


channel_red = roomba_rgb[:,:,0]

channel_red_thresh = channel_red > 200
plt.imshow(channel_red_thresh)
plt.show()
