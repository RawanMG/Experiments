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
	obst = [random.randint(0, 1000000) for i in range(10)]
	#init points
	points = []
	while len(points) <1000:
		num = random.randint(0, 1000000)
		if num not in points and num not in obst:
			points.append(num)

	plt.plot(obst, [10 for y in range(len(obst))], 'rx')
	plt.plot(points,[10 for y in range(len(points))] ,  'bo')
	plt.show()

	#create training data
	x = []
	y = []
	train_len = int(len(points)*90.0/100)
	while len(x) < train_len:
		x1 = random.randint(0, len(points))
		x2 = random.randint(0, len(points))
		p = random.randint(0, len(obst))
		if [x1, x2, p] not in x:
			x.append([x1, x2, p])
			
			print  is_between(x1, x2, p)
			y.append( not is_between(x1, x2, p)) #True if there is a path


	#train SVM
	clf = svm.SVC()
	clf.fit(x, y)

	#validation data
	x_val = []
	y_val = []
	while len(x_val) < 10:
		x1 = random.randint(0, len(points))
		x2 = random.randint(0, len(points))
		p = random.randint(0, len(obst))
		if [x1, x2, p] not in x_val:
			x_val.append([x1, x2, p])
			y_val.append(clf.predict([x1, x2, p]))


	y = []
	for   val in x_val:
		y.append(not is_between(val[0], val[1], val[2]))

	print comp_acc(y, y_val)


