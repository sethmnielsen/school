import cv2
import numpy as np
import glob
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

    shape_arr = np.asarray(shape)
    objpoints_arr = np.asarray(objpoints)
    imgpoints_arr = np.asarray(imgpoints)
    fs_write = cv2.FileStorage(param_file, cv2.FILE_STORAGE_WRITE)
    fs_write.write("mtx", mtx)
    fs_write.write("dist", dist)
    fs_write.write("objpoints", objpoints_arr)
    fs_write.write("imgpoints", imgpoints_arr)
    fs_write.write("shape", shape_arr)
    fs_write.release()



calibrationMono('./3/my_imgs/stereo/stereoL*.bmp', 'left_cam.yaml')
calibrationMono('./3/my_imgs/stereo/stereoR*.bmp', 'right_cam.yaml')
