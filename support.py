#!/usr/bin/env python

import os
import sys
import readline
import glob

import random
import json
from pprint import pprint
import datetime
import time
from calendar import monthrange
import readline
import dateutil.parser as parser
import collections
from tabulate import tabulate

#nested_dict = lambda: collections.defaultdict(nested_dict)

data = { } 

class tabCompleter(object):
	def pathCompleter(self,text,state):
		line = readline.get_line_buffer().split()
		return [x for x in glob.glob(text+'*')][state]
	def createListCompleter(self,ll):
		def listCompleter(text,state):
			line = readline.get_line_buffer()
			if not line:
				return [c + " " for c in ll][state]
			else:
				return [c + " " for c in ll if c.startswith(line)][state]
		self.listCompleter = listCompleter
def db_init():
	global db_file_name 
	global db_folder
	db_file_name = "data.txt"

def db_name():
	return db_file_name

def file_write(name, d):
	f = open(name,'w')
	f.write(json.dumps(d, indent=4))
	f.close()

def find(key, dictionary): 
	for k, v in dictionary.iteritems():
		if k == key:
			yield v
		elif isinstance(v, dict):
			for result in find(key, v):
				yield result
		elif isinstance(v, list):
			for d in v:
				for result in find(key, d):
					yield result

def find_new(key, d): 
	lst = []
	for yy in d.keys():
		if key == yy:
			lst.append(d[yy])
		for mm in d[yy].keys():
			if key == mm:
				lst.append(d[yy][mm])
			for dd in d[yy][mm].keys():
				if key == dd:
					lst.append(d[yy][mm][dd])
				for tid in d[yy][mm][dd].keys():
					if key == tid:
						lst.append(d[yy][mm][dd][tid])
					for name in d[yy][mm][dd][tid].keys():
						if key == name:
							lst.append(d[yy][mm][dd][tid][name])
	print lst
	return lst

def get_the_date(txt, v):
	dt = datetime.date.today()
	dateflag = True
	while dateflag:
		os.system('clear') 
		yy = str(dt.year)
		mm = str(dt.month)
		dd = str(dt.day)
		readline.set_startup_hook(lambda: readline.insert_text(""))
		print txt
		print "Existing tasks for " +str(dt) + " :"
		display_daily_task_sorted(v, yy, mm, dd)
		days = raw_input("Add days to " + str(dt) + " :")
		
		if not days.strip():
			dateflag = False
		else:
			try:
				dt = dt + datetime.timedelta(days=int(days))
			except:
				pass
	return (yy,mm,dd)

def last_task_end_time(v, yy, mm, dd):
	d = v[yy][mm][dd]
	lt = datetime.datetime(int(yy), int(mm), int(dd), 9, 0)
	for key_task in d.keys():
		for key_subtask in d[key_task].keys():
			try:
				(h, m) = tuple(d[key_task][key_subtask]["end"].split(':'))
        			t = datetime.datetime(int(yy), int(mm), int(dd), int(h), int(m))
				if t > lt:
					lt = t
			except:
				pass
	#t = lt.time()
	return lt   ###str(t.hour) + ":" + str(t.minute)

def new_time(key, v, yy, mm, dd, offset):
	try:
		(h, m) = tuple(v[key].split(':'))
        	t = datetime.datetime(int(yy), int(mm), int(dd), int(h), int(m))
	except:
		t = offset

        timeflag = True
        while timeflag:
                st = str(t.time().hour) + ":" + str(t.time().minute)
                readline.set_startup_hook(lambda: readline.insert_text(""))
		print key + ": " + st
                newt = raw_input("Add minute :")
                if not newt.strip():
                        timeflag = False
                else:
                        try: 
                                t = t + datetime.timedelta(minutes=int(newt))
                        except:
                                continue
                                
                        
        return t


def get_input_for(key, tt, d):
	try:
		st = tt[key]
		readline.set_startup_hook(lambda: readline.insert_text(st))
	except:
		if key == "status":
			readline.set_startup_hook(lambda: readline.insert_text("open"))
		elif key == "flex":
			readline.set_startup_hook(lambda: readline.insert_text("normal"))
		elif key == "type":
			readline.set_startup_hook(lambda: readline.insert_text("work"))
		else:
			readline.set_startup_hook(lambda: readline.insert_text(""))
			
	t = tabCompleter()
	t.createListCompleter(list(set(find(key, d))))
	readline.set_completer_delims('\t')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(t.listCompleter)
	text=key + ": "
	return raw_input(text)

def get_input_for_new(txt, deflt, lst):
	readline.set_startup_hook(lambda: readline.insert_text(deflt))
	t = tabCompleter()
	t.createListCompleter(lst)
	readline.set_completer_delims('\t')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(t.listCompleter)
	strng = "Enter " + txt + ": " 
	return raw_input(strng)

	
def get_taskid(d):
	try:
		id = len(d.keys())
	except:
		return 1
	tbl = []
	lst = []
	print "Add subtask or create new task: "
	for tid in d.keys():
		for stid in d[tid].keys():
			if "subtask-" in stid:
				tbl.append([len(lst), d[tid]["task title"], d[tid]["project"], d[tid][stid]["start"], d[tid][stid]["end"], d[tid][stid]["status"], d[tid]["type"]])
		lst.append(int(tid.split("-")[1]))
	print tabulate(tbl)
	dflt_txt = str(len(d.keys()))
	readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
	task_id = raw_input("Enter task no.")
	try:
		task_id = int(task_id)
	except:
		print "error"
		sys.exit(0)
	if task_id < len(lst):
		task_id = lst[task_id]
	else:
		task_id = len(lst) + 1
	return task_id

def daily_task_sorted(v, y, m, d):
	lst = []
	try:
		t = v[y][m][d]
		start_d = {}
		view = []
		for k,t4d in t.items():
			for sk, st4d in t4d.items():
				if "subtask-" in sk:
					try:
						(hr, minute) = tuple(st4d["start"].split(':'))
						tt = int(hr)*60 + int(minute)
						try:
							start_d[str(tt)] = start_d[str(tt)] + [(k,sk)]
						except:
							start_d[str(tt)] = [(k,sk)]
					except:
						pass
		for start_time in sorted(start_d.keys(), key=int):
			for item in start_d[start_time]:
				lst.append(item)
	except:
		pass
	return lst

def display_daily_task_sorted(v, y, m, d):
	lst = daily_task_sorted(v, y, m, d)
	try:
		view = []
		for (k,sk) in lst:
			tmp = v[y][m][d][k]
			view.append([len(view), tmp[sk]["start"], tmp[sk]["end"], tmp["task title"][:20], tmp[sk]["subtask title"][:20], tmp[sk]["status"], tmp["type"] ])
		print tabulate(view)
	except:
		pass
	return lst

def next_task_id(v):
	for key in v.keys():
		print key.split("-")[1]	

def get_task_subtask_id(v):
	(y, m, d) = get_the_date("New Task :", v)
	os.system('clear') 
	print "New task :"
	print "Existing tasks for " + str(y) + "-" + str(m) +"-" + str(d) + " :"
	
	lst = display_daily_task_sorted(v, y, m, d)
	try:
		dflt_txt = str(len(lst))
		readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
		flag = True
		while flag:
			idd = raw_input("Enter task no.")
			try:
				idd = int(idd)
				flag = False
			except:
				pass
		if idd < len(lst):
			(tk, stk) = lst[idd]
			stk = "subtask-" + str(new_subtaskid(v[y][m][d][tk]))
		else:
			next_task_id(v[y][m][d])
			tk = "task-" + str(len(lst) + 1)
			stk = "subtask-1"
	except:
		tk = "task-1"
		stk = "subtask-1"
	return (tk, stk, y, m, d)


def new_subtaskid(d):
	sid = 1
	try:
		for k in d.keys():
			if "subtask-" in k:
				sid = sid + 1
	except:
		pass
	return sid

def sorted_key_list(data):
	sdata = {}
	lst = []
	types = []
	statuses = []
	projs = []
	title = []
	for yy in sorted(data.keys(), key=int):
		yyd = data[yy]
		for mm in sorted(yyd.keys(), key=int):
			mmd = yyd[mm]
			for dd in sorted(mmd.keys(), key=int):
				ddd = mmd[dd]

				sorted_day = daily_task_sorted(data, yy, mm, dd)

				for (task, subtask) in sorted_day:
					taskd = ddd[task]
					subtaskd = taskd[subtask]
					lst.append((yy,mm,dd, task, subtask))
					statuses.append(subtaskd["status"])
					types.append(taskd["type"])
					projs.append(taskd["project"])
					title.append(taskd["task title"])
	return lst, list(set(types)), list(set(statuses)), list(set(projs)), list(set(title))

def rm_task_kernel(data, tid, stid, yy, mm, dd):
	del data[yy][mm][dd][tid][stid]
	deltask = True
	for k in data[yy][mm][dd][tid].keys():
		if "subtask-" in k:
			deltask = False
	if deltask:
		del data[yy][mm][dd][tid]
	if len(data[yy][mm][dd].keys()) == 0:
		del data[yy][mm][dd]
	if len(data[yy][mm].keys()) == 0:
		del data[yy][mm]
	if len(data[yy].keys()) == 0:
		del data[yy]
	
	file_write(db_name(), data)
#	f = open('data.txt','w')
#	f.write(json.dumps(data, indent=4))
#	f.close()
	


def edit_task_kernel(data, tid, stid, yy, mm, dd):
	yy = str(yy)
	mm = str(mm)
	dd = str(dd)
	taskid =  str(tid)
	subtaskid = str(stid)
	lastend = 9 

	try:
		data[yy]
	except:	
		data[yy] = {}
	try:
		data[yy][mm]
	except:
		data[yy][mm] = {}
	try:
		data[yy][mm][dd]
	except:
		data[yy][mm][dd] = {}
	try:
		task = data[yy][mm][dd][taskid]
	except:
		task = data[yy][mm][dd][taskid]= {}
	try:
		subtask =task[subtaskid]
	except:
		subtask = task[subtaskid] = {}
	startt = last_task_end_time(data, yy, mm, dd)	
	task["project"]= get_input_for("project", task, data).strip()
	task["task title"]= get_input_for("task title", task, data).strip()
	task["type"]= get_input_for("type", task, data).strip()
	subtask["subtask title"] = get_input_for("subtask title", subtask, data).strip()
	startt  = new_time("start", subtask, yy, mm, dd, startt)
	subtask["start"]  = str(startt.time().hour) + ":" + str(startt.time().minute)
	endt = startt + datetime.timedelta(minutes=60)
	endt  = new_time("end", subtask, yy, mm, dd, endt)
	subtask["end"]  = str(endt.time().hour) + ":" + str(endt.time().minute)
	subtask["link"] = get_input_for("link", subtask, data).strip()
	subtask["detail"] = get_input_for("detail", subtask, data).strip()
	if subtask["detail"] == "yes":
		strn="detail/"+yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
		os.system("vim " + strn)	
	subtask["attachment"] = get_input_for("attachment", subtask, data).strip()
	subtask["status"] = get_input_for("status", subtask, data).strip()
	subtask["flex"] = get_input_for("flex", subtask, data).strip()

	file_write(db_name(), data)

