import cv2
import numpy as np

from IPython.core.debugger import Pdb

video = cv2.VideoCapture('./ECEn_631_Group_1-master/media/chex.avi')

n = 0
i = 0
frame = np.array([])
prev_frame = np.array([])
write = False
fourCC = cv2.VideoWriter_fourcc(*'MPEG')
while 1:
    ret, frame = video.read()
    prev_frame = frame
    gscale = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )

    diff = cv2.absdiff(frame, prev_frame)

    cv2.imshow('Window', diff)

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
