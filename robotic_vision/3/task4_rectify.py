import cv2
import numpy as np
import pickle as pkl

def findCorners(img, pts):
    pass

def drawLines(img):
    pass

def read_files(img_file, param_file):
    img = cv2.imread(img_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    with open(param_file, 'rb') as f:
        mtx, dist, _, _, _ = pkl.load(f)

    return img, gray, mtx, dist

left_img_file = './3/stereo/stereoL80.bmp'
right_img_file = './3/stereo/stereoR80.bmp'
left_params = './3/left_cam.pkl'
right_params = './3/right_cam.pkl'

imgL, grayL, mtxL, distL read_files(left_img_file, left_params)
imgR, grayR, mtxR, distR read_files(right_img_file, right_params)

cv2.stereoRectify(mtxL, distL, mtxR, distR)

with open('./3/RTEF.pkl', 'rb') as f:
    R, T, E, F = pkl.load(f)
