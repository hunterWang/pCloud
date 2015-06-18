#encoding:utf-8
import random
import sys
#---------------------parameter -------------
times=1000 #how many path you want to produce 
width=30 #boundry
border=5 #width=border+zoneInside
speed=1  
period=25 #time have one point 
time=1000  #how much time the point move in second
maxDistant=speed*period
radius=12 #equvilant to accurancy for track
std = 5  #stander deviation to produce mapP 

#---------------------cotroller -------------
heatmapOn = 0
peopleInOutOn = 1

def main():


	#----------------------start-----------------

	path = createPath()
	mapPFake = createPCloud(path[1]) #create mapP by fakePath
	# mapPReal = createPCloud(path[0]) #create mapP by realPath
	if heatmapOn:
		heatMapReal = getHeatmapByPath(path[0])  #realone
		heatMapFakeByPath = getHeatmapByPath(path[1])  #fakeone
		heatMapFakeByPMap = getHeatmapByMapP(mapPFake) #fakeoneByPmap
		print "compareHeatMapByPath : compareHeatMapByMap"
		print compareHeatMap(heatMapFakeByPath,heatMapReal),compareHeatMap(heatMapFakeByPMap,heatMapReal)

	if peopleInOutOn:
		print "accurancy byPath,byMap"
		print comparePeopleByPP(path[0],path[1]),comparePeopleByPM(path[0],mapPFake)

		# print "real path"
		# realpath = getPeopleInsideByPath(path[0])
		# print realpath  #print sumIn,sunOut,total
		# print "fakeBypath"
		# fakepath=getPeopleInsideByPath(path[1])
		# print fakepath
		# print "fakeByMap"
		# fakemap=getPeopleInsideByMapP(mapPFake)
		# print fakemap
		# print "accurancy for ByPath"
		# print abs(fakepath[0]-realpath[0])+abs(fakepath[1]-realpath[1])
		# print "accurancy for ByMap"
		# print abs(fakemap[0]-realpath[0])+abs(fakemap[1]-realpath[1])


def createPath ():
	#---------------------explain -------------
	'''create many fake path inside a width*width 2Dbox
	times means how many path you need,
	will return a list contain fakePath(path[1]) and realPath(path[0])
	path will like path[n][t][(x.y)]''' 
	#---------------------parameter -------------

	#---------------------cotroller -------------
	fakePointOn = 1

	#---------------------start------------------
	realPath=[]
	fakePath=[]
	for n in range(0,times):		
		realPath.append([])
		fakePath.append([])
		# realPath[n].append([random.randint(border+1,width-1-border),random.randint(border+1,width-1-border)]) #r0
		realPath[n].append([random.randint(0,width-1),random.randint(0,width-1)]) #r0
		fakePath[n].append([0,0])
		# print path[j][0]	
		# print path[j][0][1]	
		for t in range(0,int(time/period)):
			gate=0
			while gate==0:
				x = realPath[n][t][0] + random.randint(-maxDistant,maxDistant)
				y = realPath[n][t][1] + random.randint(-maxDistant,maxDistant)
				# if border+1<x<width-1-border and border+1<y<width-border-1:
				if 0<x<width and 0<y<width:
					gate=1

			realPath[n].append([x,y])
			fakePath[n].append([0,0])

		if fakePointOn:
			for t in range(0,int(time/period)):
				fakePath[n][t]=fakePoint(realPath[n][t])

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
		for t in range(0,int(time/period)+1):			
			map[n].append([])
			for i in range(0,width):
				map[n][t].append([])
				x=path[n][t][0]
				y=path[n][t][1]
				for j in range(0,width):
					rSruare = (x-i)*(x-i)+(y-j)*(y-j)
					map[n][t][i].append(1/(sqrt(2*pi)*std)*exp(-1*rSruare/(2*std*std)))
			map[n][t]=normalizeMap(map[n][t])

	# print "createPCloud"
	# print int(time/period),len(map[n])		


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



def getHeatmapByMapP(mapP):
	#---------------------explain -------------
	'''input seris of possibility map(map[n][t]) to get heatmap of each time
	   output heatMap[t][x][y]=8 means at time t there is 8 person at (x,y) '''

	#---------------------start -------------
	heatMap=[]
	for x in range(0,width):
		for y in range(0,width):
			for t in range(0,len(mapP[0])):
				if (y == 0 and x==0):
					heatMap.append([])				
				sump=0
				for n in range(0,len(mapP)):
					sump += mapP[n][t][x][y]
				heatMap[t].append([])
				heatMap[t][x].append([])
				heatMap[t][x][y]=sump


	return heatMap

def getHeatmapByPath(path):
	#---------------------explain -------------
	'''input seris of path(path[n][t][x,y]) to get heatmap of each time
	   output heatMap[t][x][y]=8 means at time t there is 8 person at (x,y) '''

	#---------------------start -------------
	heatMap=[]
	for x in range(0,width):
		for y in range(0,width):	
			for t in range(0,len(path[0])):
				if (y == 0 and x==0):
					heatMap.append([])				
				heatMap[t].append([])
				heatMap[t][x].append([])
				heatMap[t][x][y]=0

	for t in range(0,len(path[0])):
		for n in range(0,len(path)):
			x=path[n][t][0]
			y=path[n][t][1]			
			heatMap[t][x][y] += 1

	
	return heatMap

def compareHeatMap(fakeMap,realMap):
	#---------------------explain -------------
	'''input two heatMap[t][x][y]=8 and will get accurancy of people been put to wrong zone  '''
	#zoneNumber = 5 # if set 2 means 4 zone ,2*2 and so on
	range1=[0,int(width/2)]
	range2=[int(width/2),width]
	diff,sumR,sumF=0,0,0


	for t in range(0,int(time/period)):
		for x in range(0,width/2):
			for y in range(0,width/2):
				sumF += fakeMap[t][x][y]
				sumR += realMap[t][x][y]
		diff += abs(sumF-sumR)
		sumR,sumF=0,0
		for x in range(0,width/2):
			for y in range(width/2,width):
				sumF += fakeMap[t][x][y]
				sumR += realMap[t][x][y]
		diff += abs(sumF-sumR)
		sumR,sumF=0,0
		for x in range(width/2,width):
			for y in range(0,width/2):
				sumF += fakeMap[t][x][y]
				sumR += realMap[t][x][y]
		diff += abs(sumF-sumR)
		sumR,sumF=0,0
		for x in range(width/2,width):
			for y in range(width/2,width):
				sumF += fakeMap[t][x][y]
				sumR += realMap[t][x][y]
		diff += abs(sumF-sumR)

	diff = diff*1.0/(2*times*int(time/period))
	return diff

def comparePeopleByPP(realPath,fakePath):
	rnumIn,rnumOut=0,0
	fnumIn,fnumOut=0,0
	diff=0
	for t in range(0,len(realPath[0])):
		for n in range(0,len(realPath)):
			rx=realPath[n][t][0]
			fx=fakePath[n][t][0]
			ry=realPath[n][t][1]
			fy=fakePath[n][t][1]
			if((rx<=border or rx>=(width-border)) and (ry<=border or ry>=(width-border)) ):
				rnumOut +=1

			if((fx<=border or fx>=(width-border)) and (fy<=border or fy>=(width-border)) ):
				fnumOut +=1
		diff += abs(rnumOut-fnumOut)
	diff = diff/(len(realPath)*len(realPath[0]))
	return diff

def comparePeopleByPM(realPath,fakeMap):
	fnumIn,fnumOut=0,0

	for t in range(0,len(fakeMap[0])):	
		for x in range(0,width):
			for y in range(0,width):						
					for n in range(0,len(fakeMap)):
						if((x<=border or x>=(width-border)) and (y<=border or y>=(width-border)) ):
							fnumOut += fakeMap[n][t][x][y]
		for n in range(0,len(realPath)):
			rx=realPath[n][t][0]
			ry=realPath[n][t][1]
			if((rx<=border or rx>=(width-border)) and (ry<=border or ry>=(width-border)) ):
				rnumOut +=1		
		diff += abs(rnumOut-fnumOut)
		
	diff = diff/(len(realPath)*len(realPath[0]))
	return diff

def getPeopleInsideByPath(path):
	numIn,numOut=0,0

	for t in range(0,len(path[0])):
		for n in range(0,len(path)):
			x=path[n][t][0]
			y=path[n][t][1]
			if((x<=border or x>=(width-border)) and (y<=border or y>=(width-border)) ):
				numOut += 1
			else:
				numIn += 1
	numIn=numIn*1.0/(times*(1+time/period))
	numOut=numOut*1.0/(times*(1+time/period))
	num=[numIn,numOut,numIn+numOut]
	return num 

def getPeopleInsideByMapP(mapP):
	numIn,numOut=0,0

	for x in range(0,width):
		for y in range(0,width):
			for t in range(0,len(mapP[0])):				
				for n in range(0,len(mapP)):
					if((x<=border or x>=(width-border)) and (y<=border or y>=(width-border)) ):
						numOut += mapP[n][t][x][y]
					else:
						numIn += mapP[n][t][x][y]
	numIn=numIn/(times*(1+time/period))
	numOut=numOut/(times*(1+time/period))
	num=[numIn,numOut,numIn+numOut]
	return num
					
				


main()







# sum=0
# for i in range(0,len(mapP[0][0])):
# 	for j in range(0,len(mapP[0][0][i])):
# 		# print "%.3f," %mapP[0][0][i][j],	
# 		sum+=mapP[0][0][i][j]

# print sum




