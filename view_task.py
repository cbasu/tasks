#!/usr/bin/env python

from support import *

flag = True
status = "open"
type = "work"
ref_dt = datetime.date.today()
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
		new_dt = datetime.date(int(yy),int(mm),int(dd))
		if type == "all" or td["type"] == type:
			std = td[subtask]
			ldate=yy+"-"+mm+"-"+dd
			if status == "all" or std["status"] == status:
				l = len(true_index)
				if abs(ref_dt - new_dt).days < 2:
					tbl.append([l, std["status"], ldate, std["start"], std["end"], td["type"], td["project"], td["task title"][:20], std["subtask title"][:20]])
				true_index.append(index)
				

	print tabulate(tbl, headers=['No.', 'status', 'date', 'start', 'end', 'type', 'project', 'task', 'subtask'], tablefmt="fancy_grid")
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
				for k in td.keys():
					if "subtask-" not in k:
						view_task.append([len(view_task), k + " :", td[k]])
				for k in td[subtask].keys():
					view_task.append([len(view_task), k + " :", td[subtask][k]])

				print tabulate(view_task)
				readline.set_startup_hook(lambda: readline.insert_text(""))
				inner_flag2 = True
				while inner_flag2:
					inp1 = raw_input("Enter ")
					try:
						index = int(inp1)
						if index in range(len(view_task)):
							print tabulate(view_task[index:index+1])
							if view_task[index][1] == "detail :" and view_task[index][2] == "yes":
								strn="detail/"+yy+"-"+mm+"-"+dd+"-"+task+"-"+subtask
								os.system("less " + strn)
					except:
						if inp1 == "delete":
							rm_task_kernel(data, task, subtask, yy, mm, dd)
							inner_flag = False
							inner_flag2 = False
						elif inp1 == "close":
							td[subtask]["status"] = "close"
							f = open('data.txt','w')
							f.write(json.dumps(data, indent=4))
							f.close()
							inner_flag = False
							inner_flag2 = False
						elif inp1 == "modify":
							readline.set_startup_hook(lambda: readline.insert_text(""))
							inp2 = raw_input("Enter number :")
							try:
								index = int(inp2)
								xx = view_task[index][1].split(":")[0].strip()
								if index in range(len(view_task)):
									if xx in td.keys():
										td[xx] = get_input_for(xx, td[xx], data)
									elif xx in td[subtask].keys():
										td[subtask][xx] = get_input_for(xx, td[subtask][xx], data)
										if xx == "detail" and td[subtask][xx] == "yes":
											strn="detail/"+yy+"-"+mm+"-"+dd+"-"+task+"-"+subtask
											os.system("vi " + strn)
									f = open('data.txt','w')
									f.write(json.dumps(data, indent=4))
									f.close()
									inner_flag2 = False
							except:
								pass
									
						elif inp1 == "back":
							inner_flag = False
							inner_flag2 = False
			

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
 
