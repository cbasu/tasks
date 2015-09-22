#!/usr/bin/env python

from support import *

try:
	json_data=open("data.txt").read()
	data1 = json.loads(json_data)
	for yy in data1.keys():
		for mm in data1[yy].keys():
			for dd in data1[yy][mm].keys():
				for taskid in data1[yy][mm][dd].keys():
					data[yy][mm][dd][taskid] = data1[yy][mm][dd][taskid]
except:
	pass
#				
##print(json.dumps(data, indent=4))
#
#print "add task"
#
add_task(data)
#
f = open('data.txt','w')
f.write(json.dumps(data, indent=4))
f.close()


