import cv2
import numpy as np
import glob
import pickle as pkl
from IPython.core.debugger import Pdb

np.set_printoptions(suppress=True)

def createImgPoints(img_files):
    w = 10
    h = 7

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((w*h,3), np.float32)
    objp[:,:2] = np.mgrid[:w,:h].T.reshape(-1,2) * 3.88636
    
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane
    images = sorted(glob.glob(img_files))
    for file in images:
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        flgs = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
        ret, corners = cv2.findChessboardCorners(gray, (w,h), flgs)

        objpoints.append(objp)
        
        corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, (w,h), corners, ret)

        cv2.imshow('img', img)
        cv2.waitKey(10)

    shape = gray.shape[::-1]
    return imgpoints, objpoints, shape


with open("./3/left_cam.pkl", 'rb') as f:
    mtxL, distL, _, _, _ = pkl.load(f)

with open("./3/right_cam.pkl", 'rb') as f:
    mtxR, distR, _, _, _ = pkl.load(f)

print('Left intrinsic params:\n', mtxL)
print('Left distortion coeff:\n', distL)
print('Right intrinsic params:\n', mtxR)
print('Right distortion coeff:\n', distR)

imgpoints_L, objpoints, shape = createImgPoints('./3/my_imgs/stereo/stereoL*.bmp')
imgpoints_R, objpoints, shape = createImgPoints('./3/my_imgs/stereo/stereoR*.bmp')

print("Files successfully read. Performing stereo calibration...")
criteria = (cv2.TERM_CRITERIA_COUNT + cv2.TERM_CRITERIA_EPS, 30, 0.001)
retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
    cv2.stereoCalibrate(objpoints, imgpoints_L, imgpoints_R, mtxL, distL, mtxR, distR, shape,
    flags=cv2.CALIB_FIX_INTRINSIC)

print("Done!")
print("\nWriting RTEF pickle file...")
with open("./3/RTEF.pkl", 'wb') as f:
    data = [R, T, E, F]
    pkl.dump(data, f)

print('\nR:\n', R)
print('T:\n', T)
print('E:\n', E)
print('F:\n', F)