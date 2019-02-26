import cv2
import numpy as np
import glob
from IPython.core.debugger import Pdb

np.set_printoptions(suppress=True)

def calibrationMono(filenames):
    w = 10
    h = 7

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-5)
    objp = np.zeros((w*h,3), np.float32)
    objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2) * 3.88636
    
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane
    images = sorted(glob.glob(filenames))
    for file in images:
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

    return imgpoints, ret, mtx, dist, rvecs, tvecs, objpoints, shape


imgpoints_L, ret, mtxL, distL, rvecsL, tvecsL, _, shape = calibrationMono('./3/my_imgs/stereo/stereoL*.bmp')
imgpoints_R, ret, mtxR, distR, rvecsR, tvecsR, objpoints, _ = calibrationMono('./3/my_imgs/stereo/stereoR*.bmp')

# Pdb().set_trace()
retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
    cv2.stereoCalibrate(objpoints, imgpoints_L, imgpoints_R, mtxL, distL, mtxR, distR, shape,
    flags=cv2.CALIB_FIX_INTRINSIC)

print('R:\n', R)
print('T:\n', T)
print('E:\n', E)
print('F:\n', F)