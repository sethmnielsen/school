import cv2
import numpy as np
import glob

fs_read = cv2.FileStorage('camera_param.yaml', cv2.FILE_STORAGE_READ)
mtx = fs_read.getNode('mtx').mat()
dist = fs_read.getNode('dist').mat()
fs_read.release()

img = cv2.imread('./object-corners.jpg')

xp = np.array([])
yp = np.array([])

x = np.array([])
y = np.array([])
z = np.array([])

with open('data_points.txt') as file:
    for line in file:
        nums = line.split()
        if len(nums) == 2:
            xp = np.append(xp, float(nums[0]))
            yp = np.append(yp, float(nums[1]))
        else:
            x = np.append(x, float(nums[0]))
            y = np.append(y, float(nums[1]))
            z = np.append(z, float(nums[2]))

imgpts = np.array([xp,yp]).T
objpts = np.array([x,y,z]).T

retval, rvec, tvec = cv2.solvePnP(objpts, imgpts, mtx, dist)
R, jacobian = cv2.Rodrigues(rvec)

print('R: ', R)
print('T: ', tvec)
