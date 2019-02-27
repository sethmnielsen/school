import cv2
import numpy as np
import glob
import pickle as pkl
from IPython.core.debugger import Pdb

np.set_printoptions(suppress=True)

def calibrationMono(img_files, param_file):
    w = 10
    h = 7

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-5)
    objp = np.zeros((w*h,3), np.float32)
    objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2) * 3.88636
    
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane
    images = sorted(glob.glob(img_files))
    count = 0
    for file in images:
        count += 1
        if count % 3 == 0:
            continue
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (w,h), None)

        objpoints.append(objp)

        corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, (w,h), corners, ret)

        cv2.imshow('img', img)
        cv2.waitKey(100)

    shape = gray.shape[::-1]
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                       shape, None, None)

    with open(param_file, 'wb') as f:
        data = [mtx, dist, objpoints, imgpoints, shape]
        pkl.dump(data, f)

print("Calibrating left camera...")
calibrationMono('./3/my_imgs/left/leftL*.bmp', './3/left_cam.pkl')
print("Done!")
print("Calibrating right camera...")
calibrationMono('./3/my_imgs/right/rightR*.bmp', './3/right_cam.pkl')
print("Done!")
print("Pickle files successfully written")
