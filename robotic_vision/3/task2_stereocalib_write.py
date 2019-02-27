import cv2
import numpy as np
import glob
import pickle as pkl
from IPython.core.debugger import Pdb

np.set_printoptions(suppress=True)

def calibrationMono(img_files, param_file):
    w = 10
    h = 7

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((w*h,3), np.float32)
    objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2) * 3.88636
    
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane
    images = sorted(glob.glob(img_files))
    for file in images:
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        flgs = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
        ret, corners = cv2.findChessboardCorners(gray, (w,h), flgs)

        objpoints.append(objp)

        corners = cv2.cornerSubPix(gray, corners, (5,5), (-1,-1), criteria)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, (w,h), corners, ret)

        cv2.imshow('img', img)
        cv2.waitKey(10)

    shape = gray.shape[::-1]
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                       shape, None, None)

    with open(param_file, 'wb') as f:
        data = [mtx, dist, objpoints, imgpoints, shape]
        pkl.dump(data, f)

print("Calibrating right camera...")
calibrationMono('./3/my_imgs/right/rightR*.bmp', './3/right_cam.pkl')
print("Done!")
print("Calibrating left camera...")
calibrationMono('./3/my_imgs/left/leftL*.bmp', './3/left_cam.pkl')
print("Done!")
print("Pickle files successfully written")
