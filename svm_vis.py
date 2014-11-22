import sys
sys.path.append('/usr/local/lib/python2.7/site-packages') #SET PYTHONPATH to this on MAC

import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from sklearn import svm, grid_search
import cPickle

from onedimSVM import read_data

def load_svm(filename):
	with open(filename, 'rb') as f:
		clf = cPickle.load(f)
	return clf
def set_color(i):
	if i == 0:
		return "red"
	return "green"

def plot_svm(clf, X, Y):
	h = 1000
	# create a mesh to plot in
	x_min, x_max = 0, 3*(10**6)
	y_min, y_max = 0, 3*(10**6)
	#x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	#y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.linspace(x_min, x_max, num=20), np.linspace(y_min, y_max,num=20))
	print "created meshgrid"
	Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
	print "after decision_function"
	vcolor= np.vectorize(set_color)
	colors = vcolor(Z)
	print colors
	
	# Put the result into a color plot
	#Z = Z.reshape(xx.shape)
	#plt.contourf(xx, yy, -Z, cmap=plt.cm.jet)

	# Plot also the training points
	plt.scatter(X[:, 0], X[:, 1], color=colors)
	plt.xlabel('X1')
	plt.ylabel('X2')
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	#plt.xticks(())
	#plt.yticks(())
	plt.show()
	Z = Z.reshape(xx.shape)
	plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
	plt.axis('off')
	#plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
	plt.show()
def heat_map(clf, X, Y):
	h = 1
	# create a mesh to plot in
	x_min, x_max = (3*(10**6))/2 - (10**2), (3*(10**6))/2 + (10**2) #3*(10**6) 15 00 000
	y_min, y_max = (3*(10**6))/2 - (10**2), (3*(10**6))/2 + (10**2) 
	#x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	#y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max,h))
	print "created meshgrid"
	Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	print "after decision_function"

	
	# Put the result into a color plot
	#Z = Z.reshape(xx.shape)
	#plt.contourf(xx, yy, -Z, cmap=plt.cm.jet)

	Z = Z.reshape(xx.shape)
	plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
	plt.axis('off')
	#plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
	plt.show()
def main(argv):
	clf = load_svm(argv[0])

	Y, X = read_data(argv[1])
	Y = np.matrix(Y[:(10**3)])
	X = X[:(10**3)]
	X = np.matrix(X)
	heat_map(clf, X, Y)
	sys.exit(0)
	plot_svm(clf, X, Y)


if __name__ == '__main__':
	main(sys.argv[1:])









