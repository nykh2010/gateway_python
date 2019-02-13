import numpy as np
import cv2
import time


PATH = r"C:\Users\xulf4\Downloads\4K.bmp"
img = cv2.imread(PATH)
imgArray = np.array(img,dtype=np.uint8)

# def rgb2yuv(red,green,blue,y,u,v):
#     y = (77 * red + 150 * green + 29 * blue) >> 8
#     u = ((-44 * red - 87 * green + 131 * blue)>>8) + 128
#     v = ((131*red - 110*green - 21*blue)>>8) + 128

M = np.array([
    [77,-44,131],
    [150,-87,-110],
    [29,131,-21]
])
D = np.array([0,128,128])

# print(M)
rgb = imgArray[:][0][0]
# print(rgb.shape)
# print(imgArray[:][0][0])


yuv = np.dot(M ,rgb)
yuv = np.right_shift(yuv,8)
yuv = np.add(yuv, D)
print(yuv)

print(imgArray.shape)