import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans


data = [[0.697, 0.460], [0.774, 0.376], [0.634, 0.264], [0.608, 0.318], [0.556, 0.215], [0.403, 0.237],
         [0.481, 0.149], [0.437, 0.211], [0.666, 0.091], [0.243, 0.267], [0.245, 0.057], [0.343, 0.099],
         [0.639, 0.141], [0.657, 0.198], [0.360, 0.370], [0.593, 0.042], [0.719, 0.103], [0.359, 0.188],
         [0.339, 0.241], [0.282, 0.257], [0.748, 0.232], [0.714, 0.346], [0.483, 0.312], [0.478, 0.437],
         [0.525, 0.369], [0.751, 0.489], [0.532, 0.472], [0.473, 0.376], [0.725, 0.455], [0.446, 0.459]]
data = np.array(data)
def standard(x: np.ndarray):
    return (x - x.mean(axis=0)) / x.std(axis=0)
data = standard(data)


init_center = np.array((data[0],data[2]))
center, distortion = kmeans(data, init_center, iter=100) # 获取聚类中心 和 distortion
center = np.array(center)
#print(center)

# 根据距离最近的中心进行分类
category = [[] for i in range(len(center))]
label = [0 for _ in range(len(data))]
for i, points in enumerate(data):
    dis = []
    for j, pos in enumerate(center):
        dis.append(sum((points - pos) ** 2))
    idx = np.array(dis).argmin()
    category[idx].append(points)
    label[i] = idx
for i, x in enumerate(category):
    print("第 %d 类有 %d 个: " % (i, len(x)), x)
print(label)

plt.scatter(data[:, 0], data[:, 1], c=label)
plt.grid()
plt.title('After Classification')
plt.show()


'''
distortion [float]:
 The mean (non-squared) Euclidean distance between the observations passed and the
 centroids generated. Note the difference to the standard definition of distortion in the context
 of the K-means algorithm, which is the sum of the squared distances
'''
