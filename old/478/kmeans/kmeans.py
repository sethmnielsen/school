import numpy as np

pts = [[0]*2]*5
pts[0] = [.9, .8]
pts[1] = [.2, .2]
pts[2] = [.7, .6]
pts[3] = [-.1, -.6]
pts[4] = [.5, .5]

adists = np.zeros(5)
bdists = np.zeros(5)
for i in range(2,5):
    adists[i] = abs(pts[i][0] - pts[0][0]) + abs(pts[i][1]-pts[0][1])
    bdists[i] = abs(pts[i][0] - pts[1][0]) + abs(pts[i][1]-pts[1][1])

print('adists =', adists)
print('bdists =', bdists)
# print('Min:',np.min(dists[np.nonzero(dists)]))
