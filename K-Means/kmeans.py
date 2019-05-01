import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

#  raw data
seed = np.random.randint(int(1e6))
x, y = make_blobs(n_samples=1500, n_features=2, centers=5, random_state=seed)
#  plot
plt.subplot(121)
plt.scatter(x[:, 0], x[:, 1])
plt.grid()
plt.title('Raw Data')

#  k-means
clf = KMeans(n_clusters=5, max_iter=300, random_state=seed).fit(x)
#  plot
plt.subplot(122)
plt.scatter(x[:, 0], x[:, 1], c=clf.labels_)
plt.grid()
plt.title('After Classification')
print(clf.labels_)

plt.savefig('Classification.png')
plt.show()
