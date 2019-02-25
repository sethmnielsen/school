import cv2
import numpy as np
import glob

np.set_printoptions(suppress=True)

w = 10
h = 7

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, w*h, 0.001)

objp = np.zeros((w*h,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)

objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

images = sorted(glob.glob('./3/imgs_catcher/imageL*.bmp'))

for file in images:
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)

    objpoints.append(objp)

    corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
    imgpoints.append(corners)
    cv2.drawChessboardCorners(img, (w,h), corners, ret)

    print(file)
    cv2.imshow('img', img)
    cv2.waitKey(1000)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                   gray.shape[::-1], None, None)

fs_write = cv2.FileStorage('./3/left_cam.yaml', cv2.FILE_STORAGE_WRITE)
fs_write.write("mtx", mtx)
fs_write.write("dist", dist)
fs_write.release()

print('mtx=', mtx)
print('dist=', dist)

# cv2.destroyAllWindows()
