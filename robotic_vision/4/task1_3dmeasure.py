import cv2
import numpy as np
import pickle as pkl


def chessboard(img_file, param_file):
    w = 10
    h = 7
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, w*h, 0.001)
    
    with open(param_file, 'rb') as f:
            mtx, dist, _, _, _ = pkl.load(f)

    img_raw = cv2.imread(img_file)
    gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
    corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
    corners2 = np.squeeze(corners)
    outer = np.array(corners[0,0], corners[0,9], corners[6,0], corners[6,9])
    # img_undst = cv2.undistort(img_raw, mtx, dist)
    print("Done")

img_file = '../3/my_imgs/stereo/stereoL31.bmp'
param_file = '../3/left_cam.pkl'

chessboard(img_file, param_file)