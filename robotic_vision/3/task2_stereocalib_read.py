import cv2
import numpy as np
import glob
import pickle as pkl
from IPython.core.debugger import Pdb

np.set_printoptions(suppress=True)

data = []
with open("./3/left_cam.pkl", 'rb') as f:
    mtxL, distL, objpoints, imgpoints_L, shape = pkl.load(f)

with open("./3/right_cam.pkl", 'rb') as f:
    mtxR, distR, _, imgpoints_R, _ = pkl.load(f)

print("Files successfully read. Performing stereo calibration...")
# Pdb().set_trace()
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