import cv2
import numpy as np
import glob
import pickle as pkl

num = 25

with open('./3/left_cam.pkl', 'rb') as f:
    mtxL, distL = pkl.load(f)

with open('./3/right_cam.pkl', 'rb') as f:
    mtxR, distR = pkl.load(f)

images = glob.glob('./undistort/{}.bmp'.format(num))

for file in images:

    img = cv2.imread(file)

    # Distortion correction
    h, w = img.shape[:2]
    img_undst = cv2.undistort(img, mtx, dist)

    diff = cv2.absdiff(img, img_undst)

    cv2.imshow('img', diff)
    cv2.waitKey(0)
    cv2.imwrite(file[:-4] + '_diff.jpg', diff)

cv2.destroyAllWindows()
