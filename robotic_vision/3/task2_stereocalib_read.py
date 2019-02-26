import cv2
import numpy as np
import glob
from IPython.core.debugger import Pdb

np.set_printoptions(suppress=True)

fs_readL = cv2.FileStorage('./3/left_cam.yaml', cv2.FILE_STORAGE_READ)
mtxL = fs_readL.getNode('mtx').mat()
distL = fs_readL.getNode('dist').mat()
objpoints = fs_readL.getNode('objpoints').mat().aslist()
imgpoints_L = fs_readL.getNode('imgpoints').mat().aslist()
shape_arr = fs_readL.getNode('shape').mat()
shape = (shape_arr[0], shape_arr[1])
fs_readL.release()

fs_readR = cv2.FileStorage('./3/right_cam.yaml', cv2.FILE_STORAGE_READ)
mtxR = fs_readR.getNode('mtx').mat()
distR = fs_readR.getNode('dist').mat()
imgpoints_L = fs_readR.getNode('imgpoints').mat().aslist()
fs_readR.release()

# Pdb().set_trace()
retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
    cv2.stereoCalibrate(objpoints, imgpoints_L, imgpoints_R, mtxL, distL, mtxR, distR, shape,
    flags=cv2.CALIB_FIX_INTRINSIC)

fs_write = cv2.FileStorage('RTEF.yaml', cv2.FILE_STORAGE_WRITE)
fs_write.write('R', R)
fs_write.write('T', T)
fs_write.write('E', E)
fs_write.write('F', F)

print('R:\n', R)
print('T:\n', T)
print('E:\n', E)
print('F:\n', F)