import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import sys

def get_dist(point1, point2):
	x = point1[0]-point2[0]
	y = point1[1] - point2[1]
	dist = np.sqrt(x**2 + y**2)
	return dist

def get_shortest(start, pointlist):
	min_dist = 100000000000
	min_point = (-1, -1)

	for (x, y) in pointlist:
		#compute Eucalidean dist
		dist = get_dist(start, (x, y))
		if dist < min_dist:
			min_point = (x, y)
			min_dist = dist

	return min_point

def is_inside(point, polygons):
	for poly in polygons:
		size = len(poly)
		for i in range(0, size):
			p1 = np.array([poly[i][0], poly[i][1]]) # (x1, y1) in line l1
			p2 = np.array([poly[(i+1)%size][0], poly[(i+1)%size][1]]) # (x2, y2) in line l2
			l1 = p2-p1
			if i-1 < 0:
				p2 = np.array([poly[size-1][0], poly[size-1][1]])
			else:
				p2 = np.array([poly[i-1][0], poly[i-1][1]])
			l2 = p2-p1

			pline = np.array(point)-p1
			cp1 = np.cross(l1, l2)
			cp2 = np.cross(l1, pline)	
			if np.dot(cp1, cp2) >=0:
				return True
	return False		



if __name__ == '__main__':
	print "here"
	#init 2D road map as a 40x40 grid
	map = [(0, 0), (0, 40), (40, 0), (40, 40)]	

	start = (random.randint(0, 40), random.randint(0, 40))
	goal = (random.randint(0, 40), random.randint(0, 40))

	polygons = []
	polygon = [(2,2), (4,4), (7,7), (10,5), (7,3)]
	polygons.append(polygon)
	polygon = [(20,7), (19,15), (28,28), (30,10), (25,6)]
	polygons.append(polygon)
	polygon = [(8,17), (2,30), (8,35), (11,30)]
	polygons.append(polygon)
	fig, ax = plt.subplots()
	verts = [p for p in polygons]
	coll = PolyCollection(verts)
	ax.add_collection(coll)
	ax.autoscale_view()
	#plt.show()

	path = []
	path.append(start)

	while cmp(start, goal) != 0:
		#drop 10 random points
		points = []
		num = 0
		while num <10:
			(x, y) = (random.randint(0, 40), random.randint(0, 40))
			if not (x, y) in points:
				points.append((x, y))
				num = num + 1
		
		#plt.plot([x for (x, y) in points], [y for (x, y) in points], 'ro')
		#plt.show()

		while points:
			#pick point with shortest distance from start (start, p)
			point = get_shortest(start, points)
			#check for collision
			insideObst = is_inside(point, polygons)
			if not insideObst:
				path.append(point)
				start = point
				break
			points.remove(point)
		print "iteration done"

	plt.plot([x for (x, y) in path], [y for (x, y) in path], 'ro')
	plt.show()




