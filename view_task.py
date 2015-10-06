#!/usr/bin/env python


from support import *

def view_task_table(td, subtask):
	view_task = []
	for k in td.keys():
               if "subtask-" not in k: 
			view_task.append([len(view_task), k + " :", td[k]])
        for k in td[subtask].keys():
                view_task.append([len(view_task), k + " :", td[subtask][k]])
	print tabulate(view_task)
	return view_task
			
def modify_task_kernel(view_task, inp2, td, data, subtask):
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
		return True
	except:
		return False

def modify_task(inp, true_index, data):	
	try:
		nmod = int(inp.split()[1])
	except:
		nmod = raw_input("Enter task No. :")
	try:
		nmod = int(nmod)
		if nmod <= len(true_index): 
			(yy,mm,dd,task,subtask) = lst[true_index[nmod]]
			td = data[yy][mm][dd][task]
			view_task = view_task_table(td, subtask)
			readline.set_startup_hook(lambda: readline.insert_text(""))
			inp2 = raw_input("Enter number :")
			return modify_task_kernel(view_task, inp2, td, data, subtask)
	except:
		return False

def view_task_kernel(view_task, inp2, td, data, subtask):
	try:
		index = int(inp2)
		if index in range(len(view_task)):
			print tabulate(view_task[index:index+1])
			if view_task[index][1] == "detail :" and view_task[index][2] == "yes":
				strn="detail/"+yy+"-"+mm+"-"+dd+"-"+task+"-"+subtask
				os.system("less " + strn)
		return True
	except:
		return False

def view_task(inp, true_index, data):	
	try:
		nview = int(inp.split()[1])
	except:
		nview = raw_input("Enter task No. :")
	try:
		nview = int(nview)
		if nview <= len(true_index): 
			(yy,mm,dd,task,subtask) = lst[true_index[nview]]
			td = data[yy][mm][dd][task]
			view_task = view_task_table(td, subtask)
			readline.set_startup_hook(lambda: readline.insert_text(""))
			inp2 = raw_input("Enter number :")
			ret = view_task_kernel(view_task, inp2, td, data, subtask)
			raw_input("Enter to continue :") 
			return ret
	except:
		return False
		

def close_task(inp, true_index, data):	
	try:
		nclose = int(inp.split()[1])
	except:
		nclose = raw_input("Enter task No. :")
	try:
		nclose = int(nclose)
		if nclose <= len(true_index): 
			(yy,mm,dd,task,subtask) = lst[true_index[nclose]]
			td = data[yy][mm][dd][task]
			td[subtask]["status"] = "close"
			f = open('data.txt','w')
			f.write(json.dumps(data, indent=4))
			f.close()
	except:
		pass

def rm_task(inp, true_index, data):	
	try:
		ndel = int(inp.split()[1])
	except:
		ndel = raw_input("Enter task No. :")
	try:
		ndel = int(ndel)
		if ndel <= len(true_index): 
			(yy,mm,dd,task,subtask) = lst[true_index[ndel]]
			td = data[yy][mm][dd][task]
			rm_task_kernel(data, task, subtask, yy, mm, dd)
	except:
		pass

def copy_task(inp, true_index, data):	
	try:
		ncp = int(inp.split()[1])
	except:
		ncp = raw_input("Enter source task No. :")
	try:
		ncp = int(ncp)
		if ncp <= len(true_index): 
			(yy,mm,dd,task,subtask) = lst[true_index[ncp]]
			td = data[yy][mm][dd][task]
	except:
		return
	dt = datetime.date.today()
        dateflag = True
        while dateflag:
		readline.set_startup_hook(lambda: readline.insert_text(""))
		days = raw_input("Enter target date ("+str(dt)+") :")
		if not days.strip():
			dateflag = False
		else:
			try: 
				dt = dt + datetime.timedelta(days=int(days)) 
			except: 
				pass
	print inp, dt
	new_yy = str(dt.year)
	new_mm = str(dt.month)
	new_dd = str(dt.day)
	try:
		data[new_yy]
	except:
		data[new_yy] = {}
	try:
		data[new_yy][new_mm]
	except:
		data[new_yy][new_mm]= {}
	try:
		data[new_yy][new_mm][new_dd]
	except:
		data[new_yy][new_mm][new_dd] =  {}
	try:
		data[new_yy][new_mm][new_dd][task]
		xx = raw_input("Task Exists. Do you want to overwrite :")
		if xx == "y":
			data[new_yy][new_mm][new_dd][task] = td
	except:
		data[new_yy][new_mm][new_dd][task] =  td

	if td[subtask]["detail"] == "yes":
	 	strold="detail/"+yy+"-"+mm+"-"+dd+"-"+task+"-"+subtask	
	 	strnew="detail/"+new_yy+"-"+new_mm+"-"+new_dd+"-"+task+"-"+subtask	
		os.system("cp " +  strold + " " + strnew)
	f = open('data.txt','w')
	f.write(json.dumps(data, indent=4))
	f.close()

def index_for_start_end_print(end, win, leng):
	if end > leng:
		end = leng
	elif end < 0 :
		end = 0
	start = end - win
	if start < 0:
		start = 0
	return (start, end)
	

flag = True
status = "open"
typ1 = "work"
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
		if typ1 == "all" or td["type"] == typ1:
			std = td[subtask]
			ldate=yy+"-"+mm+"-"+dd
			if status == "all" or std["status"] == status:
				l = len(true_index)
				tbl.append([l, ldate, std["start"], std["end"], td["project"], td["task title"][:20], std["subtask title"][:20]])
				true_index.append(index)
				try:
					end_index
				except:
					if new_dt > ref_dt: 
						(start_index, end_index) = index_for_start_end_print(l, 10, len(true_index))
	prstr = "Showing " + '"'+ typ1 + '"' + " tasks with " + '"' + status + '"' + " statuses"  			
	print prstr
	print tabulate(tbl[start_index:end_index], headers=['No.', 'date', 'start', 'end', 'project', 'task', 'subtask'], tablefmt="fancy_grid")
	readline.set_startup_hook(lambda: readline.insert_text(""))
	inp = raw_input("Enter ")

	
	
	try:
		x1 = inp.split()[0]
	except:
		continue	
	
	try:
		nd = int(x1)
		(start_index, end_index) = index_for_start_end_print(end_index + nd, 10, len(true_index))
		

	except:
		if x1 == "search":
			if inp.split()[1] == "all":
				status = "all"
				typ1 = "all"
			elif inp.split()[1] in statuses:
				status = inp.split()[1]
			elif inp.split()[1] in types:
				typ1 = inp.split()[1]
		elif x1 == "view":
			viewflag = True
			while viewflag:
				os.system('clear') 
				print "Task details"
				print "============"
				viewflag = view_task(inp, true_index, data)
		elif x1 == "modify":
			modflag = True
			while modflag:
				os.system('clear') 
				print "Task details"
				print "============"
				modflag = modify_task(inp, true_index, data)
		elif x1 == "close":
			close_task(inp, true_index, data)	
		elif x1 == "delete":
			rm_task(inp, true_index, data)	
		elif x1 == "copy":
			copy_task(inp, true_index, data)	
		elif x1 == "new":
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
 
