import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


class K_means:
    def __init__(self):
        self.classifier = None
        self.category = None
        self.data = None
        self.n_clusters = 3 #  cooresponding to centers
        self.iter_times = 300

    def train(self, data):
        self.data = data
        self.classifier = KMeans(n_clusters=self.n_clusters,
                                 max_iter=self.iter_times).fit(self.data)
        self.category = self.classifier.labels_

    def show_category(self):
        plt.subplot(121)
        plt.scatter(self.data[:, 0], self.data[:, 1])
        plt.grid()
        plt.title('Raw Data')

        plt.subplot(122)
        plt.scatter(self.data[:, 0], self.data[:, 1], c=self.category)
        plt.grid()
        plt.title('After Classification')
        plt.savefig('category.png')
        plt.show()

    def print_category(self): print(self.category)


if __name__ == '__main__':
    seed = np.random.randint(int(1e6))
    x, y = make_blobs(n_samples=1500, n_features=2, centers=5, random_state=seed)
    print(type(x))
    #  y is the true category
    kmeans = K_means()
    data_ = [[0.697, 0.460], [0.774, 0.376], [0.634, 0.264], [0.608, 0.318], [0.556, 0.215], [0.403, 0.237],
            [0.481, 0.149], [0.437, 0.211], [0.666, 0.091], [0.243, 0.267], [0.245, 0.057], [0.343, 0.099],
            [0.639, 0.141], [0.657, 0.198], [0.360, 0.370], [0.593, 0.042], [0.719, 0.103], [0.359, 0.188],
            [0.339, 0.241], [0.282, 0.257], [0.748, 0.232], [0.714, 0.346], [0.483, 0.312], [0.478, 0.437],
            [0.525, 0.369], [0.751, 0.489], [0.532, 0.472], [0.473, 0.376], [0.725, 0.455], [0.446, 0.459]]
    data_ = np.array(data_)
    print(data_)
    kmeans.train(data_)
    kmeans.show_category()
    kmeans.print_category()
