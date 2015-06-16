#encoding:utf-8

import random

def createPath (times):
	#---------------------explain -------------
	# create many fake path inside a width*width 2Dbox
	# times means how many path you need,
	# will return a list contain fake path 
	#---------------------parameter -------------
	width=20 #boundry
	speed=1  
	period=15 #time have one point 
	time=60  #how much time the point move in second
	maxDistant=speed*period

	radius=5 #equvilant to accurancy for track

	#---------------------cotroller -------------
	fakePointOn = 1

	#---------------------start------------------
	path=[]
	for j in range(0,times):		
		path.append([])
		path[j].append([random.randint(0,width),random.randint(0,width)]) #r0
		# print path[j][0]	
		# print path[j][0][1]	
		for i in range(0,int(time/period)):
			gate=0
			while gate==0:
				x = path[j][i][0] + random.randint(-maxDistant,maxDistant)
				y = path[j][i][1] + random.randint(-maxDistant,maxDistant)
				if 0<x<width and 0<y<width:
					gate=1

			path[j].append([x,y])

		if fakePointOn:
			for i in range(0,int(time/period)):
				path[j][i]=fakePoint(path[j][i],width,radius)



	return path

def fakePoint (point,width,radius):
	#---------------------explain -------------
	#point should be [x.y] and will rutnrn a point which 
	#distant from point in radius you want and inside the box with width  
	

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




print createPath(1)
# print fakePoint([3,4])



