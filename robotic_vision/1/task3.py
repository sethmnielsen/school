import cv2
import numpy as np

frame = np.array([])
fourCC = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('baseball_0.avi',fourCC,25.0,(640,480))

k = 5
loc = 'baseball_imgs/'
side = 'L'
filename = loc + '1{}{:02}.jpg'.format(side,k)
frame0 = cv2.imread(filename)
while 1:
    k += 1
    if k > 40 and side == 'L':
        k = 6
        side = 'R'
        frame0 = cv2.imread(loc + '1R05.jpg')
    elif k > 40 and side == 'R':
        break

    filename = loc + '1{}{:02}.jpg'.format(side,k)
    frame = cv2.imread(filename)

    diff = cv2.absdiff(frame, frame0)

    gscale = cv2.cvtColor( diff, cv2.COLOR_BGR2GRAY )
    ret, dt = cv2.threshold(gscale, 15, 255, cv2.THRESH_BINARY )
    kernel = np.ones((5,5), np.uint8)
    erode_img = cv2.erode(dt, kernel, iterations=1)
    dilate_img = cv2.dilate(erode_img, kernel, iterations=1)
    dst = np.uint8(dilate_img)

    ret,labels,stats,centroids = cv2.connectedComponentsWithStats(dst)
    for x,y in centroids:
        x = int(x)
        y = int(y)
        if (x < 316 or x > 321 and y > 241 or y < 238):
            cv2.circle(frame,(x,y),10,(0,0,255))
    cv2.imshow('Window', frame)

    key = cv2.waitKey(50)
    if key == ord('q'):
        break

    out.write(frame)

out.release()
cv2.destroyAllWindows()
