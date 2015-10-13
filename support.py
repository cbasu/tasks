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

def last_task_end_time(d, yy, mm, dd):
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
	t = lt.time()
	return str(t.hour) + ":" + str(t.minute)

def new_time(txt, d, yy, mm, dd, addt):
        try:
                (h, m) = tuple(d.split(':'))
        except:
                (h, m) = (9,0)

        t = datetime.datetime(int(yy), int(mm), int(dd), int(h), int(m))
	t = t + datetime.timedelta(minutes=addt)
            
        timeflag = True
        while timeflag:
                st = str(t.time().hour) + ":" + str(t.time().minute)
                readline.set_startup_hook(lambda: readline.insert_text(""))
		print txt + st
                newt = raw_input("Add minute :")
                if not newt.strip():
                        timeflag = False
                else:
                        try: 
                                t = t + datetime.timedelta(minutes=int(newt))
                        except:
                                continue
                                
                        
        return st


def get_input_for(key, dflt_txt, d):
	readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
	t = tabCompleter()
	t.createListCompleter(list(set(find(key, d))))
	readline.set_completer_delims('\t')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(t.listCompleter)
	text=key + ": "
	return raw_input(text)

	
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

def get_task_subtask_id(v, y, m, d):
	try:
		t = v[y][m][d]
		start_d = {}
		view = []
		lst = []
		for k,t4d in t.items():
			for sk, st4d in t4d.items():
				if "subtask-" in sk:
					try:
						(hr, minute) = tuple(st4d["start"].split(':'))
						tt = int(hr)*60 + int(minute)
						start_d[str(tt)] = (k,sk)
					except:
						pass
		for start_time in sorted(start_d.keys(), key=int):
			lst.append(start_d[start_time])
		for (k,sk) in lst:
			tmp = v[y][m][d][k]
			view.append([len(view), tmp[sk]["start"], tmp[sk]["end"], tmp["task title"][:20], tmp[sk]["subtask title"][:20], tmp[sk]["status"], tmp["type"] ])
		print tabulate(view)

	except:
		print "No data exists"
	dflt_txt = str(len(lst))
	readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
	task_id = raw_input("Enter task no.")
#	try:
#		task_id = int(task_id)
#	except:
#		print "error"
#		sys.exit(0)
#	return task_id

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
	for yy in sorted(data.keys(), key=int):
		yyd = data[yy]
		for mm in sorted(yyd.keys(), key=int):
			mmd = yyd[mm]
			for dd in sorted(mmd.keys(), key=int):
				ddd = mmd[dd]
				for task in sorted(ddd.keys()):
					taskd = ddd[task]
					for key in sorted(taskd.keys()):
						if "subtask-" in key:
							subtask = key 
							subtaskd = taskd[subtask]
							lst.append((yy,mm,dd,task,subtask))
							try:
								statuses.append(subtaskd["status"])
							except:
								pass
						elif key == "type":
							types.append(taskd[key])
						elif key == "project":
							projs.append(taskd[key])
	return lst, list(set(types)), list(set(statuses)), list(set(projs))

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
	f = open('data.txt','w')
	f.write(json.dumps(data, indent=4))
	f.close()
	


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
		print "project: ", task["project"]
		print "task title: ", task["task title"]
		print "type: ", task["type"]
	except:
		task = data[yy][mm][dd][taskid]= {}
		title = ""
		project = ""
		type = ""
		task["project"]= get_input_for("project", project, data).strip()
		task["task title"]= get_input_for("task title", title, data).strip()
		task["type"]= get_input_for("type", type, data).strip()
	try:
		subtask =task[subtaskid]
		title = subtask["subtask title"]
		start = subtask["start"]
		end = subtask["end"]
		link = subtask["link"]
		detail = subtask["detail"]
		attachment = subtask["attachment"]
		status = subtask["status"]
		try:
			flex = subtask["flex"]
		except:
			pass
	except:
		subtask = task[subtaskid] = {}
		title = ""
		start = last_task_end_time(data[yy][mm][dd], yy, mm, dd)
		link = ""
		detail = "no"
		attachment = ""
		status = "open"
		flex = "normal"	
	subtask["subtask title"] = get_input_for("subtask title", title, data).strip()
	subtask["start"]  = new_time("Start ", start, yy, mm, dd, 0)
	subtask["end"]  = new_time("End ", subtask["start"], yy, mm, dd, 60)
	subtask["link"] = get_input_for("link", link, data).strip()
	subtask["detail"] = get_input_for("detail", detail, data).strip()
	if subtask["detail"] == "yes":
		strn="detail/"+yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
		os.system("vim " + strn)	
	subtask["attachment"] = get_input_for("attachment", attachment, data).strip()
	subtask["status"] = get_input_for("status", status, data).strip()
	try:
		subtask["flex"] = get_input_for("flex", flex, data).strip()
	except:
		pass
	
	f = open('data.txt','w')
	f.write(json.dumps(data, indent=4))
	f.close()

