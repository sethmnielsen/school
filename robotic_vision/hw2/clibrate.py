import cv2
import numpy as np
import glob

w = 11
h = 11

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, w*h, 0.001)

objp = np.zeros((w*h,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)

objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

images = glob.glob('./undistort/*.jpg')

for file in images:
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
    print(ret)
    print(corners.shape)

    objpoints.append(objp)

    corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
    imgpoints.append(corners)
    cv2.drawChessboardCorners(img, (w,h), corners, ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                      gray.shape[::-1], None, None)

    cv2.imshow('img', img)
    cv2.waitKey(1000)
    # cv2.imwrite('task1_output.jpg', img)

cv2.destroyAllWindows()
