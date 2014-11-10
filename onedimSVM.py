import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from sklearn import svm
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import networkx as nx

def is_between(x1, x2, p):
	if p < x2 and p > x1:
		return 1
	if p < x1 and p > x2:
		return 1
	return 0
def comp_acc(y, y_pred):
	num_correct = 0
	for i in range(len(y)):
		if y[i] == y_pred[i]:
			num_correct = num_correct + 1

	return 100*(float(num_correct)/len(y))

if __name__ == '__main__':
	#init line map
	#init obstacles
	obst = random.randint(0, 3*(10**6)) #[random.randint(0, 1000000) for i in range(10)]
	print obst
	#init points
	sampling_size = 10**3
	points = []
	for i in xrange(5*(10**2)):
		num = random.randint(0, 3*(10**6))
		points.append(num)

	print len(points)
	plt.plot(obst, 10, 'rx')
	plt.plot(points,[10 for y in range(len(points))] ,  'bo')
	plt.show()

	#create data set
	dataset = []
	for i in range(0, len(points)):
		for j in range(0, len(points)):
			if i != j:
				dataset.append([points[i], points[j]])


	#extract training data from dataset
	x = []
	y = []
	train_len = int(len(dataset)*90.0/100) #90% of dataset for training
	print "Creating training set of size = %d" % train_len
	i = 0
	while len(x) < train_len:
		x1, x2 = dataset[0]
		p = obst
		#if [x1, x2] not in x:
		x.append([x1, x2])	
		y.append( not is_between(x1, x2, p)) #True if there is a path
		dataset.pop(0)



	#validation data
	print "Creating validation set of size = %d" % len(dataset)
	x_val = []
	y_val = []
	while len(dataset):
		x1, x2 = dataset[0]
		p = obst
		#if [x1, x2] not in x_val:
		x_val.append([x1, x2])
		y_val.append(not is_between(x1, x2, p))
		dataset.pop(0)


	#train SVM
	print "Training SVM"
	clf = svm.SVC()
	clf.fit(x, y)

	num_correct = 0
	for i in range(0, len(y_val)):
		x1, x2 = x_val[i]
		y = y_val[i]
		y_pred = clf.predict([x1, x2])
		if y_pred == y:
			num_correct = num_correct + 1


	ACC = num_correct /float(len(y_val))
	print "ACC = %f" %ACC
	#print comp_acc(y, y_val)


