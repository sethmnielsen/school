import cv2
import numpy as np
import glob
import pickle as pkl
from matplotlib import pyplot as plt

def drawlines(img1,img2,lines,pts1,pts2):
  ''' img1 - image on which we draw the epilines for the points in img2
      lines - corresponding epilines '''
  r,c, ch = img1.shape
  for r,pt1,pt2 in zip(lines,pts1,pts2):
      r = r.flatten()
      color = tuple(np.random.randint(0,255,3).tolist())
      x0,y0 = map(int, [0, -r[2]/r[1] ])
      x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
      img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
      img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
      img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
      return img1, img2


num = 25

with open('./3/left_cam.pkl', 'rb') as f:
    mtxL, distL, _, _, _ = pkl.load(f)

with open('./3/right_cam.pkl', 'rb') as f:
    mtxR, distR, _, _, _ = pkl.load(f)

with open('./3/RTEF.pkl', 'rb') as f:
    R, T, E, F = pkl.load(f)

imgL = cv2.imread('./3/my_imgs/stereo/stereoL{}.bmp'.format(num))
imgR = cv2.imread('./3/my_imgs/stereo/stereoR{}.bmp'.format(num))

# Distortion correction
img_undstL = cv2.undistort(imgL, mtxL, distL)
img_undstR = cv2.undistort(imgR, mtxR, distR)

ptsL = np.array([[200,200], [300,250], [300,300]])
ptsR = np.array([[200,300], [400,350], [250,400]])

for i in range(3):
    cv2.circle(img_undstL, (ptsL[i,0], ptsL[i,1]), 10, (0, 0, 255))
    cv2.circle(img_undstR, (ptsR[i,0], ptsR[i,1]), 10, (0, 0, 255))

# lines = np.zeros(3)
linesL = cv2.computeCorrespondEpilines(ptsL, 1, F)
linesR = cv2.computeCorrespondEpilines(ptsR, 1, F)

img3, img4 = drawlines(imgL, imgR, linesR, ptsL, ptsR)
img5, img6 = drawlines(imgR, imgL, linesL, ptsR, ptsL)

# cv2.imshow('imgL', img_undstL)
# cv2.imshow('imgR', img_undstR)
# cv2.waitKey(0)

plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()
