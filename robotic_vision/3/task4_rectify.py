import cv2
import numpy as np
import pickle as pkl
from IPython.core.debugger import Pdb

def findCorners(img):
    size = (10,7)
    flgs = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
    retval, corners = cv2.findChessboardCorners(img, size, flgs)
    pts = np.array([corners[25,0], corners[31,0], corners[57,0]])

    return pts

def drawLines(img):
    pts = findCorners(img)
    color = (255,0,0)
    x1, x2 = 0, 640
    for pt in pts:
        cv2.line(img, (x1, pt.y), (x2, pt.y), color)
    
def read_files(img_file, param_file):
    img = cv2.imread(img_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    with open(param_file, 'rb') as f:
        mtx, dist, _, _, _ = pkl.load(f)

    return gray, mtx, dist

def rectify(img, mtx, dist, R1, P1):
    map1, map2 = cv2.initUndistortRectifyMap(mtx, dist, R1, P1, img.shape, cv2.CV_32FC1)
    output = cv2.remap(img, map1, map2, cv2.INTER_LINEAR)
    # cv2.imshow("hi", output)
    # cv2.waitKey(0)
    diff = cv2.absdiff(img, output)
    drawLines(img)

    return output, diff

left_img_file  = './3/my_imgs/stereo/stereoL80.bmp'
right_img_file = './3/my_imgs/stereo/stereoR80.bmp'
left_params = './3/left_cam.pkl'
right_params = './3/right_cam.pkl'

imgL, mtxL, distL = read_files(left_img_file, left_params)
imgR, mtxR, distR = read_files(right_img_file, right_params)

with open('./3/RTEF.pkl', 'rb') as f:
    R, T, E, F = pkl.load(f)

R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mtxL, distL, mtxR, distR, imgL.shape, R, T)

outputL, diffL = rectify(imgL, mtxL, distL, R1, P1)
outputR, diffR = rectify(imgR, mtxR, distR, R1, P1)

cv2.imshow('imgL', imgL)
cv2.imshow('outputL', outputL)
cv2.imshow('diffL', diffL)
cv2.imshow('imgR', imgR)
cv2.imshow('outputR', outputR)
cv2.imshow('diffR', diffR)
cv2.waitKey(0)