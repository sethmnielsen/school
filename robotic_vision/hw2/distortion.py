import cv2
import numpy as np
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 70, 0.001)

a = 10
b = 7
objp = np.zeros((a*b,3), np.float32)
objp[:,:2] = np.mgrid[0:a,0:b].T.reshape(-1,2)

objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

images = glob.glob('./undistort/*.jpg')

for file in images:
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (a,b), None)

    objpoints.append(objp)

    corners = cv2.cornerSubPix(gray, corners, (a,b), (-1,-1), criteria)
    imgpoints.append(corners)
    cv2.drawChessboardCorners(img, (a,b), corners, ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                      gray.shape[::-1], None, None)

    # Distortion correction
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    # cv2.imwrite('calibresult.jpg', dst)

    # break

    # cv2.imshow('img', img)
    # cv2.waitKey(400)
    # cv2.imwrite('task1_output.jpg', img)

cv2.destroyAllWindows()
