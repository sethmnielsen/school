import numpy as np

pts = [[0]*2]*5
pts[0] = [.8, .7]
pts[1] = [-.1, .2]
pts[2] = [.9, .8]
pts[3] = [0., .2]
pts[4] = [.2, .1]

dists = np.zeros((5,5))
for i in range(5):
    for j in range(5):
        dists[i][j] = abs(pts[i][0] - pts[j][0]) + abs(pts[i][1]-pts[j][1])

print(dists)
print('Min:',np.min(dists[np.nonzero(dists)]))
