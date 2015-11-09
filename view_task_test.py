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
			
def modify_task_kernel(vt, inp2, td, data, y,m,d,tsk,stsk):
	try:
		index = int(inp2)
		xx = vt[index][1].split(":")[0].strip()
		if index in range(len(vt)):
			if xx in td.keys():
				td[xx] = get_input_for(xx, td, data).strip()
			elif xx in td[stsk].keys():
				if xx == "start" :
					td[stsk][xx] = new_time("start", td[stsk], y, m, d, 0)
				elif xx == "end" :
					td[stsk][xx] = new_time("end", td[stsk], y, m, d, 0)
				elif xx == "detail" and td[stsk][xx] == "yes":
					strn = db_path() + "/detail/"+y+"-"+m+"-"+d+"-"+tsk+"-"+stsk
					os.system("vi " + strn)
				else:
					td[stsk][xx] = get_input_for(xx, td[stsk], data).strip()
		file_write(db_name(), data)
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
			return modify_task_kernel(view_task, inp2, td, data, yy,mm,dd,task,subtask)
	except:
		return False

def view_task_kernel(vt, inp2, td, data, y,m,d,tsk, subtsk):
	try:
		index = int(inp2)
		if index in range(len(vt)):
			print tabulate(vt[index:index+1])
			if vt[index][1] == "detail :" and vt[index][2] == "yes":
				strn = db_path() + "/detail/"+y+"-"+m+"-"+d+"-"+tsk+"-"+subtsk
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
			ret = view_task_kernel(view_task, inp2, td, data, yy,mm,dd,task, subtask)
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
			file_write(db_name(), data)

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
			std = data[yy][mm][dd][task][subtask]
	except:
		return

	(ntid, nstid, ny, nm, nd) = get_task_subtask_id(data)
	copy_task_kernel(data, task, subtask, yy, mm, dd, ntid, nstid, ny, nm, nd)

def display(data, incr):
	tbl = []
	true_index = []
	l = 0
	ref_dt = datetime.date.today()
	lst, types, stats, projs, titles = sorted_key_list(data)
	typ1 = get_input_for_new("type", "work", types + ["all"]).strip()
	stat1 = get_input_for_new("status", "open", stats + ["all"]).strip()
	proj1 = get_input_for_new("project", "all", projs + ["all"]).strip()
	title1 = get_input_for_new("task title", "all", titles + ["all"]).strip()
	for index, (yy,mm,dd,task, subtask) in enumerate(lst):
		td = data[yy][mm][dd][task]
		new_dt = datetime.date(int(yy),int(mm),int(dd))
		if td["type"] == typ1 or typ1 == "all":
			std = td[subtask]
			ldate=yy+"-"+mm+"-"+dd
			if td["project"] == proj1 or proj1 == "all":
				if td["task title"] == title1 or title1 == "all":
					if std["status"] == stat1 or stat1 == "all":
						l = len(true_index)
						tbl.append([l, ldate, std["start"], std["end"], td["project"], td["task title"][:20], std["subtask title"][:20]])
						true_index.append(index)
						if new_dt > ref_dt:
							(start, end) = index_for_start_end_print(l, 10, len(true_index))
							
	prstr = "Showing " + '"'+ typ1 + '"' + " tasks with " + '"' + stat1 + '"' + " statuses"  			
	print prstr
	print tabulate(tbl[start+incr:end+incr+1], headers=['No.', 'date', 'start', 'end', 'project', 'task', 'subtask'], tablefmt="fancy_grid")

def index_for_start_end_print(end, win, leng):
	if end > leng:
		end = leng
	elif end < 0 :
		end = 0
	start = end - win
	if start < 0:
		start = 0
	return (start, end)

try:
	db_init(sys.argv[1])	
except:
	print "Error: pass the database name"	
	sys.exit()

flag = True
try:
	json_data=open(db_name()).read()
	data = json.loads(json_data)
except:
	print "error"
	sys.exit(1)
lst, types, stats, projs, titles = sorted_key_list(data)
types.append("all")
readline.set_startup_hook(lambda: readline.insert_text(""))
t = tabCompleter()
t.createListCompleter(types)
readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
readline.set_completer(t.listCompleter)
typ1 = raw_input("Enter task type: ").strip()

stat1 = "open"
#typ1 = "work"
proj1 = "all"
title1 = "all" 
ref_dt = datetime.date.today()
command = "show"
while flag:
	os.system('clear') 
	try:
		json_data=open(db_name()).read()
		data = json.loads(json_data)
	except:
		print "error"
		sys.exit(1)
	lst, types, stats, projs, titles = sorted_key_list(data)
	if command == "show":
		display_flag = True
		incr = 0
		while display_flag:
			display(data, incr)
			try:
				incr = incr + int(raw_input("Enter subcommand :").strip())
			except:
				display_flag = False	
			
	command = raw_input("Enter command :").strip()
#	for index, (yy,mm,dd,task, subtask) in enumerate(lst):
#		td = data[yy][mm][dd][task]
#		new_dt = datetime.date(int(yy),int(mm),int(dd))
#		if td["type"] == typ1 or typ1 == "all":
#			std = td[subtask]
#			ldate=yy+"-"+mm+"-"+dd
#			if td["project"] == proj1 or proj1 == "all":
#				if td["task title"] == title1 or title1 == "all":
#					if std["status"] == stat1 or stat1 == "all":
#						l = len(true_index)
#						tbl.append([l, ldate, std["start"], std["end"], td["project"], td["task title"][:20], std["subtask title"][:20]])
#						true_index.append(index)
#						try:
#							end_index
#						except:
#							if new_dt > ref_dt and l > 10:
#								(start_index, end_index) = index_for_start_end_print(l, 10, len(true_index))
#	try:
#		end_index
#	except:
#		(start_index, end_index) = index_for_start_end_print(l, 10, len(true_index))
#	prstr = "Showing " + '"'+ typ1 + '"' + " tasks with " + '"' + stat1 + '"' + " statuses"  			
#	print prstr
#	print tabulate(tbl[start_index:end_index], headers=['No.', 'date', 'start', 'end', 'project', 'task', 'subtask'], tablefmt="fancy_grid")
#	readline.set_startup_hook(lambda: readline.insert_text(""))
#	t = tabCompleter()
#	t.createListCompleter(["show", "view", "modify", "delete", "close", "copy", "report", "quit", "new", ])
#	readline.set_completer_delims('\t')
#	readline.parse_and_bind("tab: complete")
#	readline.set_completer(t.listCompleter)
#	inp = raw_input("Enter command :").strip()
#
#	
#	try:
#		x1 = inp.split()[0]
#	except:
#		continue	
#	
#	try:
#		nd = int(x1)
#		(start_index, end_index) = index_for_start_end_print(end_index + nd, 10, len(true_index))
#	except:
#		try:
#			del end_index
#			del start_index
#		except:
#			pass
#		if x1 == "report":
#			readline.set_startup_hook(lambda: readline.insert_text(""))
#			t = tabCompleter()
#			t.createListCompleter(projs)
#			readline.set_completer_delims('\t')
#			readline.parse_and_bind("tab: complete")
#			readline.set_completer(t.listCompleter)
#			prj = raw_input("Enter project name :").strip()
#			line1 = "Report for project " + prj
#			line2 = ""
#			for i in range(len(line1)):
#				line2 = line2 + "="
#			print line1
#			print line2  
#			for y,yv in data.items():
#				for m,mv in yv.items():
#					for d,dv in mv.items():
#						for t,tv in dv.items():
#							if tv["project"] == prj:
#								rdate=y+"-"+m+"-"+d
#								print rdate
#								print "Task title :", tv["task title"]
#								for s,sv in tv.items():
#									if "subtask-" in s:
#										print "Subtask title :", sv["subtask title"]
#										print "Start time :", sv["start"]
#										print "End time :", sv["end"]
#										print "Status :", sv["status"]
#										print "Detail :", sv["detail"]
#										if sv["detail"] == "yes":
#	 										rstr = db_path() + "/detail/"+y+"-"+m+"-"+d+"-"+t+"-"+s
#											fp = open(rstr, "r")	
#											print fp.readline()
#											fp.close()
#											
#										
#								print ""
#			raw_input()
#			
#		
#		if x1 == "show":
#			typ1 = get_input_for_new("type", typ1, types + ["all"]).strip()
#			stat1 = get_input_for_new("status", stat1, stats + ["all"]).strip()
#			proj1 = get_input_for_new("project", proj1, projs + ["all"]).strip()
#			title1 = get_input_for_new("task title", title1, titles + ["all"]).strip()
#		elif x1 == "view":
#			viewflag = True
#			while viewflag:
#				os.system('clear') 
#				print "Task details"
#				print "============"
#				viewflag = view_task(inp, true_index, data)
#		elif x1 == "modify":
#			modflag = True
#			while modflag:
#				os.system('clear') 
#				print "Task details"
#				print "============"
#				modflag = modify_task(inp, true_index, data)
#		elif x1 == "close":
#			close_task(inp, true_index, data)	
#		elif x1 == "delete":
#			rm_task(inp, true_index, data)	
#		elif x1 == "copy":
#			copy_task(inp, true_index, data)	
#		elif x1 == "new":
#			prj = get_input_for("project", task, data).strip()
#			task_title = get_input_for("task title", task, data).strip()
#			(tid, stid, yy, mm, dd) = get_task_subtask_id(data)
#			edit_task_kernel(data, tid, stid, yy, mm, dd)
#			readline.set_startup_hook(lambda: readline.insert_text("no"))
#			read = raw_input("Do you want to export to google calender: ")
#			if read == "yes":
#				export_gcal(data, yy, mm, dd, tid, stid)
#		elif inp == "quit":
#			flag = 0
	
 
