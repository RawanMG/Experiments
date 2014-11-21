import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from sklearn import svm, grid_search
import sys
import cPickle

from onedimSVM import read_data

def load_svm(filename):
	with open(filename, 'rb') as f:
		clf = cPickle.load(f)
	return clf

def plot_svm(X, Y, clf):
	# create a mesh to plot in
	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
	                     np.arange(y_min, y_max, h))
	Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
	# Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    plt.show()

def main(argv):
	clf = load_svm(argv[0])
	Y, X = read_data(argv[1])
	plot_svm(X, Y, clf)


if __name__ == '__main__':
	main(sys.argv[1:])









