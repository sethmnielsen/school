import cv2
import numpy as np
import pickle as pkl
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)

def findCorners(imgL, imgR):
    size = (10,7)
    flgs = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
    retval, cornersL = cv2.findChessboardCorners(imgL, size, flgs)
    retval, cornersR = cv2.findChessboardCorners(imgR, size, flgs)
    
    ptsL = np.array([cornersL[25,0], cornersL[31,0], cornersL[57,0]])
    ptsR = np.array([cornersR[5,0], cornersR[13,0], cornersR[67,0]])

    return ptsL, ptsR
    

def drawlines(img1,img2,lines,pts1,pts2):
    ''' 
    img1 - image on which we draw the epilines for the points in img2
    lines - corresponding epilines 
    '''
    r, c, ch = img1.shape
    color = tuple(np.random.randint(0,255,3).tolist())
    for line,pt1,pt2 in zip(lines,pts1,pts2):
        line = line.flatten()
        x0,y0 = map(int, [0, -line[2]/line[1] ])
        x1,y1 = map(int, [c, -(line[2]+line[0]*c)/line[1] ])
        # Pdb().set_trace()
        cv2.line(img1, (x0,y0), (x1,y1), color,1)
  
        cv2.circle(img1,tuple(pt1),5,color,-1)
        cv2.circle(img2,tuple(pt2),5,color,-1)
  
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

ptsL, ptsR = findCorners(img_undstL, img_undstR)

for ptL, ptR in zip(ptsL, ptsR):
    cv2.circle(img_undstL, tuple(ptL), 10, (0, 0, 255))
    cv2.circle(img_undstR, tuple(ptR), 10, (0, 0, 255))

# lines = np.zeros(3)
linesL = cv2.computeCorrespondEpilines(ptsL, 1, F)
linesR = cv2.computeCorrespondEpilines(ptsR, 1, F)

imgL, imgR = drawlines(img_undstL, img_undstR, linesL, ptsR, ptsL)
# imgR, imgL = drawlines(imgR, imgL, linesL, ptsL, ptsR)

cv2.imshow('imgL', imgL)
cv2.imshow('imgR', imgR)
cv2.waitKey(0)

# plt.subplot(121),plt.imshow(imgL)
# plt.subplot(122),plt.imshow(imgR)
# plt.show()
