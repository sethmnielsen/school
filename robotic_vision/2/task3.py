import cv2
import numpy as np
import glob

fs_read = cv2.FileStorage('camera_param.yaml', cv2.FILE_STORAGE_READ)
mtx = fs_read.getNode('mtx').mat()
dist = fs_read.getNode('dist').mat()
fs_read.release()

images = glob.glob('./undistort/*.jpg')

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
