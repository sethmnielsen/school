import cv2
import numpy as np

w = 9
h = 7

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, w*h, 0.001)

objp = np.zeros((w*h,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)

objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

video = cv2.VideoCapture(0)
frame = np.array([])
count = 0
while count < 50:
    ret, frame = video.read()
    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )

    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)

    if ret:
        corners = cv2.cornerSubPix(gray, corners, (w,h), (-1,-1), criteria)
        cv2.drawChessboardCorners(frame, (w,h), corners, ret)
        imgpoints.append(corners)
        objpoints.append(objp)
        count += 1

    cv2.imshow('frame', frame)
    key = cv2.waitKey(100)
    if key == ord('q'):
        break

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

fs_write = cv2.FileStorage('webcam_param.yaml', cv2.FILE_STORAGE_WRITE)
fs_write.write("mtx", mtx)
fs_write.write("dist", dist)
fs_write.release()

print('mtx=', mtx)
print('dist=', dist)

video.release()
cv2.destroyAllWindows()
