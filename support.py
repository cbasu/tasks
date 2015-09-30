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
	print "Add subtask or create new task: "
	for tid in d.keys():
		print tid.split("-")[1], d[tid]["task title"], '-', d[tid]["project"]
	dflt_txt = str(len(d.keys())+1)
	readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
	task_id = raw_input("Enter task no.")
	try:
		task_id = int(task_id)
	except:
		print "error"
		sys.exit(0)
	return task_id

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
	return lst, list(set(types)), list(set(statuses))

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
	#default =  time.strftime("%Y-%m-%d")
	#date = get_input_for("date", default, data)
	#(yy, mm, dd) = (str(parser.parse(date).year), str(parser.parse(date).month), 
	#		str(parser.parse(date).day))
	
	#id = get_taskid(data[yy][mm][dd])
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
		for key_task in data[yy][mm][dd].keys():
			for key_subtask in data[yy][mm][dd][key_task].keys():
				try:
					if lastend < int(data[yy][mm][dd][key_task][key_subtask]["end"]):
						lastend = int(data[yy][mm][dd][key_task][key_subtask]["end"])
				except:
					pass
	except:
		data[yy][mm][dd] = {}
	try:
		data[yy][mm][dd][taskid]
		title = data[yy][mm][dd][taskid]["task title"]
		project = data[yy][mm][dd][taskid]["project"]
		type = data[yy][mm][dd][taskid]["type"]
	except:
		data[yy][mm][dd][taskid]= {}
		title = ""
		project = ""
		type = ""
	task = data[yy][mm][dd][taskid]
	task["project"]= get_input_for("project", project, data)
	task["task title"]= get_input_for("task title", title, data)
	task["type"]= get_input_for("type", type, data)
	try:
		subtask =task[subtaskid]
		title = subtask["subtask title"]
		start = subtask["start"]
		end = subtask["end"]
		link = subtask["link"]
		detail = subtask["detail"]
		attachment = subtask["attachment"]
		status = subtask["status"]
	except:
		subtask = task[subtaskid] = {}
		title = ""
		start = str(lastend)
		end = str(lastend+1)
		link = ""
		detail = "no"
		attachment = ""
		status = "open"
	subtask["subtask title"] = get_input_for("subtask title", title, data)
	subtask["start"] = get_input_for("start", start, data)
	subtask["end"] = get_input_for("end", end, data)
	subtask["link"] = get_input_for("link", link, data)
	subtask["detail"] = get_input_for("detail", detail, data)
	if subtask["detail"] == "yes":
		strn="detail/"+yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
		os.system("vim " + strn)	
	subtask["attachment"] = get_input_for("attachment", attachment, data)
	subtask["status"] = get_input_for("status", status, data)
	f = open('data.txt','w')
	f.write(json.dumps(data, indent=4))
	f.close()

