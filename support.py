#!/usr/bin/env python

import os
import sys
import subprocess
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

#from time import sleep
import curses
import ctypes
from copy import deepcopy
from operator import itemgetter
import string


ESC = 27
BACKSPACE = 263    #127
TAB = 9

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
startx = 4
screen = curses.initscr()
ymax, xmax = screen.getmaxyx()
# Change this to use different colors when highlighting
curses.start_color() # Lets you use colors when highlighting selected menu option
curses.use_default_colors()
curses.can_change_color() == False
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

data = { } 

def init_screen():
	global h, n, ESC, MENU, COMMAND, EXITMENU, startx, screen, ymax, xmax
	curses.noecho() 
	curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
	screen.keypad(1) # Capture input from keypad
	screen.immedok(True)


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
def db_init(path):
	global db_file_name 
	global db_folder
	if not os.path.exists(path):
    		os.makedirs(path)
		
	db_file_name = str(path) + "/data.txt"

	if not os.path.exists(path):
    		os.makedirs(path)

	if not os.path.isfile(db_file_name):
		f = open(db_file_name, 'w') 
		f.write("{ }")
		f.close()
		
	db_folder = os.path.dirname(os.path.realpath(db_file_name))
	detail = db_folder + "/detail" 
	if not os.path.exists(detail):
    		os.makedirs(detail)

def db_name():
	return db_file_name

def db_path():
	return "'%s'" % db_folder

def file_write(name, d):
	f = open(name,'w')
	f.write(json.dumps(d, indent=4))
	f.close()

def export_gcal(v, y, m, d, tid, sid):	
	cmd = []
	cmd.append("gcalcli")
	cmd.append("--calendar")
	readline.set_startup_hook(lambda: readline.insert_text(""))
	t = tabCompleter()
	t.createListCompleter(["calender", "NSC absences", "NSC shared calender"])
	readline.set_completer_delims('\t')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(t.listCompleter)
	calender = raw_input("Name of calender: ").strip()
	cmd.append(calender)
	cmd.append("--title")
	v[y][m][d][tid][sid]["subtask title"]
	cmd.append(v[y][m][d][tid][sid]["subtask title"])
	cmd.append("--where")
	cmd.append("''")
	cmd.append("--when")
	dt = str(m)+ "/" + str(d) + "/" + str(y) + " " + v[y][m][d][tid][sid]["start"]
	cmd.append(dt)
	cmd.append("--duration")
	(h1, m1) = tuple(v[y][m][d][tid][sid]["start"].split(':'))
	(h2, m2) = tuple(v[y][m][d][tid][sid]["end"].split(':'))
	dur = str((int(h2) - int(h1)) * 60 + (int(m2) -int(m1)))
	cmd.append(dur)
	cmd.append("--description")
	cmd.append("''")
	cmd.append("--reminder")
	cmd.append("0")
	cmd.append("add")
	job = subprocess.Popen(cmd)
	job.wait()
	raw_input("Press enter to continue")

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

def wr_win(win, ypos, xpos, txt, higlight):
	#ym, xm = win.getmaxyx()
	#win.addstr(ypos, xpos, "%s" % (" "*(xm-2)), n) ##write a blank line first
	txt1 = filter(lambda x: x in string.printable, txt)
	win.addstr(ypos, xpos, "%s" % (txt1), higlight)
	win.clrtoeol()
	win.refresh()
	return ypos+1

def get_the_date(wl, txt, v, y):
	dt = datetime.date.today()
	dateflag = True
	while dateflag:
		wl.clear()
		ypos = y
		yy = str(dt.year)
		mm = str(dt.month)
		dd = str(dt.day)
		ypos = wr_win(wl, ypos, 1, txt, n)
		ypos = wr_win(wl, ypos, 1, "Existing tasks for " +str(dt) + " :", n)
		lst, ypos = display_daily_task_sorted(wl, v, yy, mm, dd, ypos+1)
		ypos = wr_win(wl, ypos, 1, "", n)
		days, ypos = curses_raw_input(wl, ypos, 1, "Add days to " + str(dt) + " :")
		if not days.strip():
			dateflag = False
		else:
			try:
				dt = dt + datetime.timedelta(days=int(days))
			except:
				pass
	return (yy,mm,dd), lst, ypos

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
	return str(lt.time().hour) + ":" + str(lt.time().minute) ## lt

def add_time(yy, mm, dd, start, minute):
	(h, m) = tuple(start.split(':'))
        t = datetime.datetime(int(yy), int(mm), int(dd), int(h), int(m))
        t = t + datetime.timedelta(minutes=int(minute))
	return str(t.time().hour) + ":" + str(t.time().minute)

def duration_time(tsk):
	
	FMT = '%H:%M'
	try:
		tdelta = datetime.datetime.strptime(tsk["end"], FMT) - datetime.datetime.strptime(tsk["start"], FMT)
		return int(tdelta.seconds) / 60
	except:
		print "error in duration_time"
		sys.exit(1)

def new_time(wl, key, v, yy, mm, dd, offset, ypos):
	try:
		(h, m) = tuple(v[key].split(':'))
        	t = datetime.datetime(int(yy), int(mm), int(dd), int(h), int(m))
	except:
		(h, m) = tuple(offset.split(':'))
        	t = datetime.datetime(int(yy), int(mm), int(dd), int(h), int(m))

        timeflag = True
	ypos1 = ypos
        while timeflag:
                st = str(t.time().hour) + ":" + str(t.time().minute)
		ypos = wr_win(wl, ypos1, 1, key + ": " + st, n)
		newt, ypos = curses_raw_input(wl, ypos, 1, "Add minute :")
                if not newt.strip():
                        timeflag = False
                else:
                        try: 
                                t = t + datetime.timedelta(minutes=int(newt))
                        except:
                                continue
                                
                        
	return str(t.time().hour) + ":" + str(t.time().minute), ypos


def get_input_for(wl, key, tt, d, ypos):
	try:
		st = tt[key]
	except:
		st = ""
	lst = list(set(find(key, d)))	
	text=key + ": "
	stt, ypos = curses_raw_input(wl, ypos, 1, text, st, lst)
	return stt.strip(), ypos

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

def display_daily_task_sorted(wl, v, y, m, d, ypos):
	lst = daily_task_sorted(v, y, m, d)
	b = "\t"
	try:
		view = []
		for (k,sk) in lst:
			tmp = v[y][m][d][k]
			st = str(len(view)) + b + tmp[sk]["start"] + b + tmp[sk]["end"] + b + tmp["task title"][:20] + b + tmp[sk]["subtask title"][:20] + b + tmp[sk]["status"] + b + tmp["type"]
			ypos = wr_win(wl, ypos, 1, st, n)
			view.append([len(view), tmp[sk]["start"], tmp[sk]["end"], tmp["task title"][:20], tmp[sk]["subtask title"][:20], tmp[sk]["status"], tmp["type"] ])
		#print tabulate(view)
	except:
		pass
	return lst, ypos

def next_task_id(v):
	maxid = 0
	for key in v.keys():
		i = int(key.split("-")[1])
		if i > maxid:
			maxid = i
	return "task-" + str(maxid+1)

def get_task_subtask_id(wl, v, ypos):
	(y, m, d), lst, ypos = get_the_date(wl, "New Task :", v, ypos)
	tk =""
	stk = ""
	try:
		dflt_txt = str(len(lst))
		flag = True
		ypos1 = ypos
		while flag:
			idd, ypos = curses_raw_input(wl, ypos1, 1, "Enter task no. :", dflt_txt)
			try:
				idd = int(idd)
				flag = False
			except:
				pass
		if idd < len(lst):
			(tk, stk) = lst[idd]
			stk = "subtask-" + str(new_subtaskid(v[y][m][d][tk]))
		else:
			tk = next_task_id(v[y][m][d])
			#tk = "task-" + str(len(lst) + 1)
			stk = "subtask-1"
	except:
		tk = "task-1"
		stk = "subtask-1"
		
	return ypos, (tk, stk, y, m, d)


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
	if data[yy][mm][dd][tid][stid]["detail"] == "yes":
		strn = db_path() + "/detail/" +yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
		os.system("rm " + strn)	
		
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
	


def edit_task_kernel(wl, data, tid, stid, yy, mm, dd, ypos):
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
	task["project"], ypos = get_input_for(wl, "project", task, data, ypos)
	task["task title"], ypos = get_input_for(wl, "task title", task, data, ypos)
	task["type"], ypos = get_input_for(wl, "type", task, data, ypos)
	subtask["subtask title"], ypos = get_input_for(wl, "subtask title", subtask, data, ypos)
	subtask["start"], ypos = new_time(wl, "start", subtask, yy, mm, dd, startt, ypos)
	endt = add_time(yy, mm, dd, subtask["start"], 60)
	subtask["end"], ypos = new_time(wl, "end", subtask, yy, mm, dd, endt, ypos)
	subtask["link"], ypos = get_input_for(wl, "link", subtask, data, ypos)
	subtask["detail"], ypos = get_input_for(wl, "detail", subtask, data, ypos)
	if subtask["detail"] == "yes":
		strn = db_path() + "/detail/" +yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
		os.system("gvim " + strn)	
	subtask["attachment"], ypos = get_input_for(wl, "attachment", subtask, data, ypos)
	subtask["status"], ypos = get_input_for(wl, "status", subtask, data, ypos)
	subtask["flex"], ypos = get_input_for(wl, "flex", subtask, data, ypos)

	file_write(db_name(), data)
	return ypos

def copy_task_kernel(wl, data, tid, stid, yy, mm, dd, ntid, nstid, ny, nm, nd, ypos):
	yy = str(yy)
	mm = str(mm)
	dd = str(dd)
	taskid =  str(tid)
	subtaskid = str(stid)

	ny = str(ny)
	nm = str(nm)
	nd = str(nd)
	ntid = str(ntid)
	nstid = str(nstid)

#	lastend = 9 
#
	try:
		data[ny]
	except:	
		data[ny] = {}
	try:
		data[ny][nm]
	except:
		data[ny][nm] = {}
	try:
		data[ny][nm][nd]
	except:
		data[ny][nm][nd] = {}
	try:
		task = data[ny][nm][nd][ntid]
	except:
		task = data[ny][nm][nd][ntid]= {}
		task["project"] = data[yy][mm][dd][taskid]["project"]
		task["task title"] = data[yy][mm][dd][taskid]["task title"]
		task["type"] =  data[yy][mm][dd][taskid]["type"] 
	try:
		subtask = task[nstid]
	except:
		subtask = task[nstid] = {}
		subtask["subtask title"] = data[yy][mm][dd][taskid][subtaskid]["subtask title"]

	ypos = wr_win(wl, ypos, 1, "Project :" + task["project"], n)
	ypos = wr_win(wl, ypos, 1, "Task title :" + task["task title"], n)
	ypos = wr_win(wl, ypos, 1, "Task type :" + task["type"], n)
	ypos = wr_win(wl, ypos, 1, "Subtask title :" + subtask["subtask title"], n)
	dur = duration_time(data[yy][mm][dd][taskid][subtaskid])
	subtask["start"], ypos = new_time(wl, "start", data[yy][mm][dd][taskid][subtaskid], ny, nm, nd, 0, ypos)
	ypos = wr_win(wl, ypos, 1, "start :" + subtask["start"], n)
	endt = add_time(ny, nm, nd, subtask["start"], dur)
	subtask["end"], ypos = new_time(wl, "end", subtask, ny, nm, nd, endt, ypos)
	ypos = wr_win(wl, ypos, 1, "end :" + subtask["end"], n)
	subtask["link"] = data[yy][mm][dd][taskid][subtaskid]["link"]
	subtask["detail"] = data[yy][mm][dd][taskid][subtaskid]["detail"]
	if subtask["detail"] == "yes":
		strold = db_path() + "/detail/" +yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
		strnew = db_path() + "/detail/" +ny+"-"+nm+"-"+nd+"-"+ntid+"-"+nstid
		os.system("cp " + strold + " " + strnew)	
	subtask["attachment"] = data[yy][mm][dd][taskid][subtaskid]["attachment"]
	subtask["status"] = data[yy][mm][dd][taskid][subtaskid]["status"]
	subtask["flex"] = data[yy][mm][dd][taskid][subtaskid]["flex"]
	file_write(db_name(), data)
	check, ypos = curses_raw_input(wl, ypos, 1, "Do you want to quit :")

def curses_del_text(wl, ys, xs, ye, xe):
	for y in range(ys, ye):
		wr_win(wl, y, xs, "", n)
	

def curses_tab_completion(wl, st, key_words):
	yM, xM = wl.getmaxyx()
	h = 6
	ym = yM - h
	xm = xM
	strng = ""
	nmatch = 0
	shift = 0
	stt = st
	curses_del_text(wl, ym, 1, yM, xM)
	
	y = wr_win(wl, ym, 1, "Existing values", n)
	
	for key in key_words:
		if key.startswith(st):
			strng = strng + "," + key
			key_match = key
			nmatch += 1
	num = len(strng) / (xM - 2)
	rem = len(strng) % (xM - 2)
	if (num > h - 2):
		num = h - 2
		last_line="Too many options ... narrow the search"
	else:
		last_line=strng[num*(xM - 2):num*(xM - 2)+rem]
	for i in range(1, num):
		end = i * (xM - 2)
		start = end - (xM - 2)
		y = wr_win(wl, y, 1, strng[start:end], n)
	y = wr_win(wl, y, 1, last_line, n)
	
	if nmatch == 1:
		shift = len(key_match) - len(st)
		stt = key_match
	return stt 
	

def curses_raw_input(wl, ypos, xpos, txt, dfl_inp="", key_words=[]):
	#curses.noecho() 
	loop = True
	st = dfl_inp
	y = wr_win(wl, ypos, 1, txt + st, n)
	while loop:
		c = wl.getch()
		if c == ord("\n"):
			loop = False
		elif c == BACKSPACE:
			st = st[:-1]
		elif c == TAB:
			st = curses_tab_completion(wl, st, key_words)
		else:
			try:
			      #chr(c) in string.printable:
			      st = st + chr(c)
			except:
			      pass
		y = wr_win(wl, ypos, 1, txt + st, n)
	return st, y		

