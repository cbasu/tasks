#!/usr/bin/env python

from support import *



							

try:
	json_data=open("data.txt").read()
	data = json.loads(json_data)

except:
	pass


for i, (yy,mm,dd,task,subtask) in enumerate(sorted_key_list(data)):
	task = data[yy][mm][dd][task]
	subtask = task[subtask]
	print i, yy, mm, dd, subtask["start"], subtask["end"], task["project"], task["task title"], subtask["subtask title"], subtask["status"] 
