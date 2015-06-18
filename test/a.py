#encoding: utf-8

import sys

file_in =file('db.txt','r')
file_out = file('copy.txt','w')

for line in file_in:
	for i in range(0,len(line)):
		if line[i] != "\n":
			print str(i) + ","
			sys.stdout.write(line[i] + "-" )
		else:
			sys.stdout.write(line[i])
			
		file_out.write(line[i])


sys.stdout.write("\n")
file_in.close()
file_out.close()


for t in range(0,10):
	print t 