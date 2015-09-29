#!/usr/bin/env python

from support import *
from tabulate import tabulate

flag = True
status = "open"
type = "work"
while flag:
	os.system('clear') 
	try:
		json_data=open("data.txt").read()
		data = json.loads(json_data)
	except:
		print "error"
		sys.exit(1)
	lst = sorted_key_list(data)
	tbl = []
	i = 0
	for (yy,mm,dd,task,subtask) in lst:
		task = data[yy][mm][dd][task]
		if type == "all" or task["type"] == type:
			subtask = task[subtask]
			date=yy+"-"+mm+"-"+dd
			if status == "all" or subtask["status"] == status:
				tbl.append([i, subtask["status"], date, subtask["start"], subtask["end"], task["type"], task["project"], task["task title"], subtask["subtask title"]])
				i = i + 1

	print tabulate(tbl, headers=['No.', 'status', 'date', 'start', 'end', 'type', 'project', 'task', 'subtask'])
	inp = raw_input("Enter ")
	if inp == "all":
		if status == "all":
			type = inp
		else:
			status = inp	
	elif inp in ["open", "close", "pending"]:
		status = inp
	elif inp in ["work", "pers"]:
		type = inp
		status = "open"
	elif inp == "new":
		yy = "2015"  ##raw_input("Enter year ")
		mm = "12"      ##raw_input("Enter month ")
		dd = "9"         ##raw_input("Enter day ")
		try:
			tid = get_taskid(data[yy][mm][dd])
		except:
			tid = 1
		tid = "task-" + str(tid)
		try:
			stid = new_subtaskid(data[yy][mm][dd][tid])
		except:
			stid = 1
		stid = "subtask-" + str(stid)
		edit_task_kernel(data, tid, stid, yy, mm, dd)
	elif inp == "quit":
		flag = 0
	
#(yy,mm,dd,task,subtask) = lst[i]
#edit_task_kernel(data, task, subtask, yy, mm, dd)
 
