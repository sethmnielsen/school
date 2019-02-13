import cv2
import numpy as np

img = cv2.imread('./calibration_imgs/AR1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, corners = cv2.findChessboardCorners(gray, (10,7), None)

if ret:
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 70, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (10,7), (-1,-1), criteria)
    cv2.drawChessboardCorners(img, (10,7), corners, ret)

    cv2.imshow('img', img)
    cv2.waitKey(4000)
    cv2.imwrite('task1_output.jpg', img)
