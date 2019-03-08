import cv2
import numpy as numpy

f = './stereoL26.bmp'


def chessboard(filename):
    w = 9
    h = 7
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, w*h, 0.001)

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
    corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
    img_und = cv2.undistort(img, mtx, dist)
    