import cv2
import numpy as np

video = cv2.VideoCapture(0)

n = 0
i = 50
output = np.array([])
frame = np.array([])
prev_frame = np.array([])
write = False
fourCC = cv2.VideoWriter_fourcc(*'MPEG')
while 1:
    prev_frame = frame
    ret, frame = video.read()
    gscale = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )

    if n == 0:
        ret, output = cv2.threshold(gscale, 100, 255, cv2.THRESH_BINARY )
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    elif n == 1:
        output = cv2.Canny( gscale, 50, 150)
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    elif n == 2:
        gscale = np.float32(gscale)
        output = cv2.cornerHarris(gscale, 2, 3, 0.04)
        output = cv2.dilate(output, None)
        ret, output = cv2.threshold(output, 0.1*output.max(), 255, 0)
        output = np.uint8(output)

        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(output)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 500, .001)
        corners = cv2.cornerSubPix(gscale, np.float32(centroids),
                                   (5,5), (-1,-1), criteria)
        corners = np.int0(corners)
        for x,y in corners:
            cv2.circle(frame, (x,y), 2, (0,0,255))

        output = frame
    elif n == 3:
        edges = cv2.Canny( gscale, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 150)
        try:
            lines[0] == None
        except TypeError:
            continue
        for line in lines:
            for r, theta in line:
                c = np.cos(theta)
                s = np.sin(theta)
                x0 = r*c
                y0 = r*s
                x1 = int(x0+1000*-s)
                y1 = int(y0+1000*c)
                x2 = int(x0-1000*-s)
                y2 = int(y0-1000*c)
                cv2.line(frame, (x1,y1), (x2,y2), (0,0,255), 2)
        output = frame
    elif n == 4:
        diff = cv2.absdiff(frame, prev_frame)
        output = diff

    cv2.imshow('Window', output)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break
    elif key == ord('w'):
        if not write:
            write = True
            out = cv2.VideoWriter('feature_{}.avi'.format(i),fourCC,25.0,(640,480))
            print('Recording video...')
        else:
            write = False
            out.release()
            print('Video feature_{}.avi saved!'.format(i))
            i += 1
    elif key != -1:
        n += 1
        if n > 4:
            n = 0

    if write:
        out.write(output)

video.release()
cv2.destroyAllWindows()
