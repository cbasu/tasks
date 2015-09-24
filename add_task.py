#!/usr/bin/env python

from support import *

try:
	json_data=open("data.txt").read()
	data1 = json.loads(json_data)
	#data = data1
	for yy in data1.keys():
		data[yy] = data1[yy]
except:
	pass
#				

print(json.dumps(data, indent=4))
#
#print "add task"
#
#add_task(data)
add_task(data, 1, 1, 2015, 9, 22)
add_task(data, 1, 1, 2015, 9, 23)
print(json.dumps(data, indent=4))
#
f = open('data.txt','w')
f.write(json.dumps(data, indent=4))
f.close()


