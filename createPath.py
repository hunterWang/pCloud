#encoding:utf-8

import random
import sys


#---------------------parameter -------------
times=300 #how many path you want to produce 
width=30 #boundry
speed=1  
period=15 #time have one point 
time=600  #how much time the point move in second
maxDistant=speed*period
radius=5 #equvilant to accurancy for track
std = 2  #stander deviation to produce mapP 


def createPath ():
	#---------------------explain -------------
	'''create many fake path inside a width*width 2Dbox
	times means how many path you need,
	will return a list contain fakePath and realPath''' 
	#---------------------parameter -------------

	#---------------------cotroller -------------
	fakePointOn = 1

	#---------------------start------------------
	realPath=[]
	fakePath=[]
	for j in range(0,times):		
		realPath.append([])
		fakePath.append([])
		realPath[j].append([random.randint(0,width),random.randint(0,width)]) #r0
		fakePath[j].append([0,0])
		# print path[j][0]	
		# print path[j][0][1]	
		for i in range(0,int(time/period)):
			gate=0
			while gate==0:
				x = realPath[j][i][0] + random.randint(-maxDistant,maxDistant)
				y = realPath[j][i][1] + random.randint(-maxDistant,maxDistant)
				if 0<x<width and 0<y<width:
					gate=1

			realPath[j].append([x,y])
			fakePath[j].append([0,0])

		if fakePointOn:
			for i in range(0,int(time/period)):
				fakePath[j][i]=fakePoint(realPath[j][i])

	path=[realPath,fakePath]
	return path

def fakePoint (point):
	#---------------------explain -------------
	'''
	point should be [x.y] and will rutnrn a point which 
	distant from point in radius you want and inside the box with width  
	'''

	#---------------------parameter -------------
	# radius = 5 #equvilant to accurancy for track
	


	#---------------------start------------------
	gate = 0
	while gate == 0:
		x = point[0] + random.randint(-radius,radius)
		y = point[1] + random.randint(-radius,radius)
		if 0<x<width and 0<y<width:
			gate=1
	return [x,y]


def createPCloud(path):
	#---------------------explain -------------
	'''
	input is path[0~n] n stand for how many path 
	each path has certain point like path[0][0]=[x,y],path[0][1]=[x,y].....means every second have a position
	output will be map[0~n] n will map to path n below
	each map will like map[0][1][x][y]=0.5 means when time=1 path[0]'s possibility map at (x,y)=0.5    	
	'''
	from math import exp,sqrt,pi
	#---------------------parameter -------------
	

	#---------------------start------------------
	map=[]
	for n in range(0,times):
		map.append([])
		for t in range(0,int(time/period)):
			map[n].append([])
			for i in range(0,width):
				map[n][t].append([])
				x=path[n][t][0]
				y=path[n][t][1]
				for j in range(0,width):
					rSruare = (x-i)*(x-i)+(y-j)*(y-j)
					map[n][t][i].append(1/(sqrt(2*pi)*std)*exp(-1*rSruare/(2*std*std)))
			map[n][t]=normalizeMap(map[n][t])


	return map

def normalizeMap(mapP):
	#---------------------explain -------------
	'''
	input is mapP[0][0] to mapP[n][n]
	and output will let it sum up to 1     	
	'''
	#---------------------start ------------

	sum=0
	for i in range(0,len(mapP)):
		for j in range(0,len(mapP[i])):
			sum += mapP[i][j]
	factor=1/sum
	for i in range(0,len(mapP)):
		for j in range(0,len(mapP[i])):
			mapP[i][j]=mapP[i][j]*factor
	return mapP






path = createPath()
mapP = createPCloud(path[1]) #create mapP by fakePath


# sum=0
# for i in range(0,len(mapP[0][0])):
# 	for j in range(0,len(mapP[0][0][i])):
# 		# print "%.3f," %mapP[0][0][i][j],	
# 		sum+=mapP[0][0][i][j]

# print sum




