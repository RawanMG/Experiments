import sys
sys.path.append('/usr/local/lib/python2.7/site-packages') #SET PYTHONPATH to this on MAC
sys.path.append('/usr/local/lib')
sys.path.append('/usr/local/lib/python')
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python')

import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from sklearn import svm, grid_search

import cPickle


import networkx as nx

sampling_size = 10**5
grid_param = {'C':[1, 10, 100], 'gamma':[0.0001, 0.01, 0.1, 1]}
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
def make_data(filename):
	#init line map
	#init obstacles
	obst = (3*(10**6))/2 #[random.randint(0, 1000000) for i in range(10)]
	print obst
	#init points

	"""
	points = []
	for i in xrange(sampling_size):
		num = random.randint(0, 3*(10**6))
		points.append(num)
	"""
	points = np.linspace(0, 3*(10**6), num=sampling_size)
	print len(points)
	plt.plot(obst, 10, 'rx')
	plt.plot(points,[10 for y in range(len(points))] ,  'bo')
	plt.show()

	#create data set
	data_size = 10**6
	"""
	dataset = []
	
	while len(dataset) < data_size:
		i = random.randint(0, len(points))
		j = random.randint(0, len(points))
		dataset.append([points[i], points[j]])
	"""
	"""
	for i in range(0, len(points)):
		for j in range(0, len(points)):
			if i != j:
				dataset.append([points[i], points[j]])
	"""


	#extract training data from dataset
	x = []
	y = []
	train_len = int(data_size*90.0/100) #90% of dataset for training
	print "Creating training set of size = %d" % train_len

	while len(x) < train_len:
		i = random.randint(0, len(points)-1)
		j = random.randint(0, len(points)-1)
		x1, x2 = points[i], points[j]
		p = obst
		#if [x1, x2] not in x:
		x.append([x1, x2])	
		y.append( not is_between(x1, x2, p)) #True if there is a path



	#validation data
	val_len = data_size - train_len
	print "Creating validation set of size = %d" % val_len
	x_val = []
	y_val = []
	while len(x_val)< val_len:
		i = random.randint(0, len(points)-1)
		j = random.randint(0, len(points)-1)
		x1, x2 = points[i], points[j]
		p = obst
		#if [x1, x2] not in x_val:
		x_val.append([x1, x2])
		y_val.append(not is_between(x1, x2, p))

	with open('%d_uni_tr.csv'%filename, 'w') as f:
		for i in range(len(y)):
			f.write("%d,%d,%d\n"%(y[i], x[i][0], x[i][1]))

	with open('%d_uni_val.csv'%filename, 'w') as f:
		for i in range(len(y_val)):
			f.write("%d,%d,%d\n"%(y_val[i], x_val[i][0], x_val[i][1]))

def read_data(filename):
	y =[]
	x =[]
	with open(filename, 'r') as f:
		for line in f:
			line = line.split(',')
			y.append(int(line[0]))
			x.append([int(line[1]), int(line[2])])

	return y, x
def crossvalidate(x, y):
	svr= svm.SVC()
	clf = grid_search.GridSearchCV(svr, grid_param, n_jobs=2, cv=5, verbose=1)
	clf.fit(x, y)
	print clf.best_estimator_
	print clf.best_params_
	with open('crossvalidationresult.txt', 'w') as f_out:
		f_out.write(clf.best_estimator_)
		f_out.write("\n")
		f_out.write(clf.best_params_)

if __name__ == '__main__':

	make_data(sampling_size)
	y_val, x_val = read_data("%d_uni_val.csv"%sampling_size)
	#crossvalidate(x_val, y_val)
	#sys.exit(0)
	y, x = read_data("%d_uni_tr.csv"%sampling_size)
	
 	#sys.exit(0)


	#train SVM
	print "Training SVM"
	clf = svm.SVC(C=1.0, gamma=0.0001, max_iter=10**5, verbose=3)
	clf.fit(x, y)

	with open("%d_1_uni.pkl"%(sampling_size), 'wb') as f:
		cPickle.dump(clf, f)

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


