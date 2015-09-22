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

nested_dict = lambda: collections.defaultdict(nested_dict)

data = nested_dict()

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
	#t.createListCompleter(find_new(key, d))
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
			print tid.split("-")[1], d[tid]["title"]
		dflt_txt = str(len(d.keys())+1)
		readline.set_startup_hook(lambda: readline.insert_text(dflt_txt))
		task_id = raw_input("Enter task no.")
		try:
			task_id = int(task_id)
		except:
			print "error"
			sys.exit(0)
	return task_id

def add_task(data):
	default =  time.strftime("%Y-%m-%d")
	date = get_input_for("date", default, data)
	(yy, mm, dd) = (str(parser.parse(date).year), str(parser.parse(date).month), 
			str(parser.parse(date).day))
	
	id = get_taskid(data[yy][mm][dd])
	taskid = "task-" + str(id)
	td = data[yy][mm][dd][taskid]
	#task = data[yy][mm][dd][taskid]	
	#sid = get_taskid(task)
	#subtaskid = "subtask-" + str(sid)
	#td = task[subtaskid]
	if id <= len(td.keys()):   ## edit existing data
		td["title"] = get_input_for("title", td["title"], data)
		td["start"] = get_input_for("start", td["start"], data)
		td["end"] = get_input_for("end", td["end"], data)
		td["type"] = get_input_for("type", td["type"], data)
		td["project"] = get_input_for("project", td["project"], data)
		td["link"] = get_input_for("link", td["link"], data)
		td["detail"] = get_input_for("detail", td["detail"], data)
		td["attachment"] = get_input_for("attachment", td["attachment"], data)
		td["status"] = get_input_for("status", td["status"], data)
	else:		
		td["title"] = get_input_for("title", "", data)
		td["start"] = get_input_for("start", "", data)
		td["end"] = get_input_for("end", "", data)
		td["type"] = get_input_for("type", "", data)
		td["project"] = get_input_for("project", "", data)
		td["link"] = get_input_for("link", "", data)
		td["detail"] = get_input_for("detail", "", data)
		td["attachment"] = get_input_for("attachment", "", data)
		td["status"] = get_input_for("status", "open", data)

