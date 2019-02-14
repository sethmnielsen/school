import cv2
import numpy as np

fs_read = cv2.FileStorage('webcam_param.yaml', cv2.FILE_STORAGE_READ)
mtx = fs_read.getNode('mtx').mat()
dist = fs_read.getNode('dist').mat()
fs_read.release()

video = cv2.VideoCapture(0)
frame = np.array([])
count = 0
while count < 50:
    ret, frame = video.read()

    # Distortion correction
    h, w = frame.shape[:2]
    img_undst = cv2.undistort(frame, mtx, dist)

    diff = cv2.absdiff(frame, img_undst)

    cv2.imshow('img', diff)
    cv2.waitKey(100)
    count += 1

cv2.imwrite('task6_diff.jpg', diff)
video.release()
cv2.destroyAllWindows()
