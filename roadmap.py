import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import networkx as nx

# Graph creation
gr = nx.path_graph(0)

class Node:
	def __init__(self, id, location):
		self.id = id
		self.location = location
        



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

def num_intersect(point, polygon):
	p1 = np.array([polygon[0][0], polygon[0][1], 0])
	p2 = np.array([polygon[2][0], polygon[2][1], 0])
	N = np.cross(p1, p2)
	print N
	print np.linalg.norm(N)
	if np.linalg.norm(N) != 0.0:
		N = N/np.linalg.norm(N)
	return N


def inside_poly(point, poly):
	size = len(poly)
	for i in range(0, size):
		p1 = np.array([poly[i][0], poly[i][1], 0]) # (x1, y1) in line l1
		p2 = np.array([poly[(i+1)%size][0], poly[(i+1)%size][1], 0]) # (x2, y2) in line l2
		l1 = p2-p1
		pline = np.array(point)-p1

		if i-1 <= 0:
			p2 = np.array([poly[size-1][0], poly[size-1][1], 0])
		else:
			p2 = np.array([poly[i-1][0], poly[i-1][1], 0])
		l2 = p2-p1
			
		cp1 = np.cross(l1, l2)
		cp2 = np.cross(l1, pline)

		if np.dot(cp1, cp2) < 0:
			return False

	return True

def is_inside(point, polygons):
	""" References:
		http://www.blackpawn.com/texts/pointinpoly/
	"""
	for poly in polygons:
		if inside_poly(point, poly):
			return True

	return False



def pnpoly(xp, yp, x, y):
	""" References: 
		http://erich.realtimerendering.com/ptinpoly/
		http://www.faqs.org/faqs/graphics/algorithms-faq/
	"""

	j = 1
	c = 0
	print c
	for i in range(len(polygons)):
		if (((yp[i]<=y) and (y<yp[j])) or \
			(yp[j]<=y) and (y<yp[i])) and \
			(x<(xp[j]-xp[i])*(y-yp[i])/(yp[j]-yp[i]) + xp[i]):
			c = not c
			print c
		j = i

	return c 

if __name__ == '__main__':
	#init 2D road map as a 40x40 grid
	map = [(0, 0), (0, 40), (40, 0), (40, 40)]	

	start = (1, 1)
	goal = (39, 39)

	polygons = []
	polygon = [(2,2), (4,4), (7,7), (10,5), (7,3), (2,2)]
	polygons.append(polygon)
	polygon = [(20,7), (19,15), (28,28), (30,10), (25,6), (20,7)]
	polygons.append(polygon)
	polygon = [(8,17), (2,30), (8,35), (11,30), (8,17)]
	polygons.append(polygon)
	fig, ax = plt.subplots()
	verts = [p for p in polygons]
	coll = PolyCollection(verts)
	ax.add_collection(coll)
	ax.autoscale_view()
	#plt.show()

	path = []
	path.append(start)
	#xp = [p[0] for p in polygons[0]]
	#yp = [p[1] for p in polygons[0]]
	#print pnpoly(xp, yp, 30, 5)
	#print is_inside([35, 5, 0], polygons)

	#Sampling
	num = 0
	points = []
	dict = {}
	while num <50:
		(x, y) = (random.randint(0, 40), random.randint(0, 40))
		if not (x, y) in points:
			if not is_inside([x, y, 0], polygons):
				points.append([x, y])
				dict[num] = [x, y]
				gr.add_node(num)
				num = num + 1


	plt.plot([x for (x, y) in points], [y for (x, y) in points], 'go')
	plt.plot([start[0], goal[0]], [start[1], goal[1]], 'ro')
	plt.show()
	print gr.nodes()


	#connect points to every other point
	for node in gr.nodes():
		for node2 in gr.nodes():
			if node != node2:
				gr.add_edge(node, node2, weight=get_dist(points[node], points[node2]))

	start_node = len(points)

	points.append(start)
	goal_node = len(points)
	
	points.append(goal)

	for node in gr.nodes():
		gr.add_edge(start_node, node, weight=get_dist(points[start_node], points[node]))
		gr.add_edge(node, goal_node, weight=get_dist(points[node], points[goal_node]))
	#search for shortest path
	print points[len(points)-2]
	print points[len(points)-1]
	path = nx.astar_path(gr, start_node, goal_node)
	print path
	print [points[p] for p in path]

	#plot path
	fig, ax = plt.subplots()
	verts = [p for p in polygons]
	coll = PolyCollection(verts)
	ax.add_collection(coll)
	ax.autoscale_view()
	plt.plot([points[n][0] for n in path], [points[n][1] for n in path], 'ro', linewidth=2.0, linestyle='--')
	other_p = [points[n] for n in gr.nodes() if n not in path]
	plt.plot([x for (x, y) in other_p], [y for (x, y) in other_p], 'go')
	
	plt.show()
	sys.exit(0)
