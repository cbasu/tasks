#!/usr/bin/env python

from support import *

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
	lst, types, statuses = sorted_key_list(data)
	tbl = []
	true_index = []
	for index, (yy,mm,dd,task,subtask) in enumerate(lst):
		td = data[yy][mm][dd][task]
		if type == "all" or td["type"] == type:
			std = td[subtask]
			ldate=yy+"-"+mm+"-"+dd
			if status == "all" or std["status"] == status:
				l = len(true_index)
				tbl.append([l, std["status"], ldate, std["start"], std["end"], td["type"], td["project"], td["task title"], std["subtask title"]])
				true_index.append(index)
				

	print tabulate(tbl, headers=['No.', 'status', 'date', 'start', 'end', 'type', 'project', 'task', 'subtask'])
	readline.set_startup_hook(lambda: readline.insert_text(""))
	inp = raw_input("Enter ")
	try:
		i = int(inp)
		if i <= len(true_index): 
			inner_flag = True
			while inner_flag:
				view_task = []
				(yy,mm,dd,task,subtask) = lst[true_index[i]]
				td = data[yy][mm][dd][task]
				view_task.append([len(view_task), "Task :", td["task title"]])
				view_task.append([len(view_task), "Project :", td["project"]])
				view_task.append([len(view_task), "Type :", td["type"]])
				try:
					view_task.append([len(view_task), "Flex :", td[subtask]["flex"]])
				except:
					pass
				view_task.append([len(view_task), "Sub task :", td[subtask]["subtask title"]])
				view_task.append([len(view_task), "Date :", yy+"-"+mm+"-"+dd])	
				view_task.append([len(view_task), "Start :", td[subtask]["start"]])
				view_task.append([len(view_task), "End :", td[subtask]["end"]])
				view_task.append([len(view_task), "status :", td[subtask]["status"]])
				view_task.append([len(view_task), "Links :", td[subtask]["link"]])
				view_task.append([len(view_task), "Attachment :", td[subtask]["attachment"]])
				view_task.append([len(view_task), "Description :", td[subtask]["detail"]])
				print tabulate(view_task)
				readline.set_startup_hook(lambda: readline.insert_text(""))
				inp1 = raw_input("Enter ")
				if inp1 == "delete":
					rm_task_kernel(data, task, subtask, yy, mm, dd)
					inner_flag = False
				elif inp1 == "close":
					td[subtask]["status"] = "close"
					f = open('data.txt','w')
					f.write(json.dumps(data, indent=4))
					f.close()
					inner_flag = False
				elif inp1 == "modify":
					readline.set_startup_hook(lambda: readline.insert_text(""))
					inp2 = raw_input("Enter number :")
				elif inp1 == "back":
					inner_flag = False
			

	except:
		if inp == "all":
			status = "all"
			type = "all"
		elif inp in statuses:
			status = inp
		elif inp in types:
			type = inp
		elif inp == "new":
			default =  time.strftime("%Y-%m-%d")
			dt = datetime.date.today()
			dateflag = True
			while dateflag:
				readline.set_startup_hook(lambda: readline.insert_text(""))
				days = raw_input("Enter Date ("+str(dt)+") :")
				
				if not days.strip():
					dateflag = False
				else:
					try:
						dt = dt + datetime.timedelta(days=int(days))
					except:
						pass
			yy = str(dt.year)
			mm = str(dt.month)
			dd = str(dt.day)

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
 
