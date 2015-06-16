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
	time=3600  #how much time the point move in second
	maxDistant=speed*period

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

	return path
	 	




path = createPath(2)
print path



