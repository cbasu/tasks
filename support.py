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
	id = len(d.keys())
	if id == 0:
		task_id = 1
	else:
		print "Existing tasks: "
		for tid in d.keys():
			print tid.split("-")[1], d[tid]["task title"]
		dflt_txt = str(len(d.keys())+1)
		readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
		task_id = raw_input("Enter task no.")
		try:
			task_id = int(task_id)
		except:
			print "error"
			sys.exit(0)
	return task_id

def sorted_key_list(data):
	sdata = {}
	lst = []
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
	return lst

def edit_task_kernel(data, tid, stid, yy, mm, dd):
	#default =  time.strftime("%Y-%m-%d")
	#date = get_input_for("date", default, data)
	#(yy, mm, dd) = (str(parser.parse(date).year), str(parser.parse(date).month), 
	#		str(parser.parse(date).day))
	
	#id = get_taskid(data[yy][mm][dd])
	yy = str(yy)
	mm = str(mm)
	dd = str(dd)
	taskid = "task-" + str(tid)
	subtaskid = "subtask-" + str(stid)

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
		data[yy][mm][dd][taskid]
		title = data[yy][mm][dd][taskid]["task title"]
		project = data[yy][mm][dd][taskid]["project"]
	except:
		data[yy][mm][dd][taskid]= {}
		title = ""
		project = ""
	task = data[yy][mm][dd][taskid]
	task["project"]= get_input_for("project", project, data)
	task["task title"]= get_input_for("task title", title, data)
	try:
		subtask =task[subtaskid]
		title = subtask["subtask title"]
		start = subtask["start"]
		end = subtask["end"]
		type = subtask["type"]
		link = subtask["link"]
		detail = subtask["detail"]
		attachment = subtask["attachment"]
		status = subtask["status"]
	except:
		subtask = task[subtaskid] = {}
		title = ""
		start = ""
		end = ""
		type = ""
		link = ""
		detail = ""
		attachment = ""
		status = ""
	subtask["subtask title"] = get_input_for("subtask title", title, data)
	subtask["start"] = get_input_for("start", start, data)
	subtask["end"] = get_input_for("end", end, data)
	subtask["type"] = get_input_for("type", type, data)
	subtask["link"] = get_input_for("link", link, data)
	subtask["detail"] = get_input_for("detail", detail, data)
	subtask["attachment"] = get_input_for("attachment", attachment, data)
	subtask["status"] = get_input_for("status", status, data)

