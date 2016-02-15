#!/usr/bin/env python

from support import *

def add_newtask(wl, d):
	var = 1
	curses.echo()
	ypos, (tid, stid, yy, mm, dd) = get_task_subtask_id(wl, d, 1) 
	ypos = edit_task_kernel(wl, data, tid, stid, yy, mm, dd, ypos)
	while var == 1:
		y = wr_win(wl, ypos, 1, 'Do you want to close the window: ', n)
		key = wl.getch()
		if key == ord("y"):
			var = 0
	curses.noecho() 


def modify_task_new(wl, d, yy, mm, dd, tid, stid):
	wl.clear()
	wl.refresh()
	title = "view/modify task"
	c = None
	t = d[yy][mm][dd][tid]
	st = t[stid]
	strn = db_path() + "/detail/"+yy+"-"+mm+"-"+dd+"-"+tid+"-"+stid
	
	key = []
	tmp_t = []
	key.append("project")
	key.append("type")
	key.append("task title")
	key.append("subtask title")
	key.append("status")
	key.append("flex")
	key.append("start")
	key.append("end")
	key.append("link")
	key.append("detail")
	key.append("attachment")
	tmp_t.append(t["project"])
	tmp_t.append(t["type"])
	tmp_t.append(t["task title"])
	tmp_t.append(st["subtask title"])
	tmp_t.append(st["status"])
	tmp_t.append(st["flex"])
	tmp_t.append(st["start"])
	tmp_t.append(st["end"])
	tmp_t.append(st["link"])
	tmp_t.append(st["detail"])
	tmp_t.append(st["attachment"])

	row = 0
	y1 = wr_win(wl, 2, xmax/2 - len(title)/2, title, curses.A_STANDOUT) ## Title
	while c != ord('q') :
		y = y1+2
		for i, opt in enumerate(key):
		      stn = key[i]+":"
		      stn = stn.ljust(17) + tmp_t[i]
		      if i  == row:
			  y = wr_win(wl, y, 1, stn, h)
			  (yh, xh) = wl.getyx()
		      else:
			  y = wr_win(wl, y, 1, stn, n)

		y = wr_win(wl, ymax-4, 2, "save and quit (x), quit (q): ", n)
		c = wl.getch()
		if c == curses.KEY_DOWN:
			l = len(key)
			if row < l-1:
			      row = row + 1
			else:
			      row = l - 1
		elif c == curses.KEY_UP:
			if row > 0:
			      row = row - 1
			else:
			    row = 0
		elif c == ord('\n'):
			curses.echo() 
			wl.move(yh, 1)
			stn = key[row]+":"
			stn = stn.ljust(17)
			tmp_t[row],y = curses_raw_input(wl, yh, 1, stn, tmp_t[row])
			if key[row] == "detail" and tmp_t[row] == "yes":
			      os.system("gvim " +  strn)
			curses.noecho()
		elif c == ord('x'):
			for i,k in enumerate(key):
			      if k in ["project", "type", "task title"]:
				    t[k] = tmp_t[i]
			      else:
				    st[k] = tmp_t[i] 
			      if k == "detail" and tmp_t[i] == "no":
				    os.system("rm -f " + strn)
			file_write(db_name(), d)
			
			if os.path.isfile(strn+".tmp"):
			      os.system("mv " + strn+".tmp" + " " + strn)
			break



def action(wl, x, y, comm, ind, d):
	msg = ""
	textstyle = n
	msg = "select the task to " + comm + " and type y: "
	wr_win(wl, ymax-6, startx, msg, textstyle)
	if comm == "new":				
		msg = "for new task type y : "
		wr_win(wl, ymax-6, startx, msg, textstyle)
	elif comm == "search":
		msg = "not yet implemented "
		wr_win(wl, ymax-6, startx, msg, textstyle)
	elif comm == "move":
		msg = "not yet implemented "
		wr_win(wl, ymax-6, startx, msg, textstyle)
	
	inp = screen.getch()
	if inp == ord("y"):
		(yy,mm,dd,task,subtask) = ind
		t = d[yy][mm][dd][task]
		wl.addstr(y,len(msg)+x, "%s" % ('y'), n)
		if comm == "new":
			add_newtask(wl, d)

	return inp

def one_line(i, yy, mm, dd, t, st):
	b = " "
	s = str(i) + b + yy + "-"
	if int(mm) < 10:
	  s1 = "0" + mm + "-"
	else:
	  s1 = mm + "-"
	if int(dd) < 10:
	  s1 = s1 + "0" + dd
	else:
	  s1 = s1 + dd
	s = s + s1 + b 
	tarr = st["start"].split(":")
	if int(tarr[0]) < 10:
	  s1 = "0" + tarr[0] + ":"
	else:
	  s1 = tarr[0] + ":"
	if int(tarr[1]) < 10:
	  s1 = s1 + "0" + tarr[1]
	else:
	  s1 = s1 + tarr[1]
	s = s + s1 + b
	tarr = st["end"].split(":")
	if int(tarr[0]) < 10:
	  s1 = "0" + tarr[0] + ":"
	else:
	  s1 = tarr[0] + ":"
	if int(tarr[1]) < 10:
	  s1 = s1 + "0" + tarr[1]
	else:
	  s1 = s1 + tarr[1]
	s = s + s1 + b
	
	s = s + t["project"].ljust(10)
	s = s + b + filter(lambda x: x in string.printable, t["task title"][:15]).ljust(15)
	s = s + b + filter(lambda x: x in string.printable, st["subtask title"][:20])

	return s

def show_list(dat, typ, prj, title, stat):
	lst, types, stats, projs, titles = sorted_key_list(data)
	tbl = []
	table_index = []
	l = 0
	b = " "
	for index, (yy,mm,dd,task, subtask) in enumerate(lst):
		td = data[yy][mm][dd][task]
		new_dt = datetime.date(int(yy),int(mm),int(dd))
		if td["type"] == typ or typ == "all":
			std = td[subtask]
			if td["project"] == prj or prj == "all":
				if td["task title"] == title or title == "all":
					if std["status"] == stat or stat == "all":
						l = len(table_index)
						tbl.append(one_line(l, yy, mm, dd, td, std))
						table_index.append(index)
	return tbl, table_index, lst

def list_range(r, l):
	w = 10
	f = r / w
	s = f * w
	e = (f+1) * w
	if e > l: e = l
	return range(s, e)	
	
def main_list(wl, dat, menu, menu_command, typ, stat, row, act, prj, title):
	wl.clear()
	rows, row_index, true_index = show_list(dat, typ, prj, title, stat)
	wl.border(0)
	wr_win(wl, 2, startx, "Title", curses.A_STANDOUT) ## Title
	count1 = len(menu)
	ycurser, xcurser = wl.getyx()
	menu1y = ymax-2
	menu1x = startx
	try:
		for key in menu:
			textstyle = n
			if typ == key:
				textstyle = h
			wr_win(screen, menu1y, menu1x, key, textstyle)
			menu1x = menu1x + len(key) + 2
	except:
		pass
	menu2x = startx
	menu2y = 5
	try:
		for key1 in menu[typ]:
			textstyle = n
			if stat == key1:
				textstyle = h
			wr_win(screen, menu2y, menu2x, key1, textstyle)
			menu2x = menu2x + len(key1) + 2
	except:
		pass			
	menu3x = startx
	menu3y = 7
	try:
		for line in list_range(row, len(rows)):
			textstyle = n
			if row == line:
				textstyle = h
			wr_win(screen, menu3y, menu3x, rows[line], textstyle)
			menu3y = menu3y  + 1
	except:
		pass
	menu4x = startx
	menu4y = ymax-4
	try:
		#for key3 in menu_action:
		for key3 in menu_command:
			textstyle = n
			if act == key3:
				textstyle = h
			wr_win(screen, menu4y, menu4x, key3, textstyle)
			menu4x = menu4x  + len(key3) + 2 
	except:
		pass
	return  row, true_index[row_index[row]], len(rows)


# This function displays the appropriate menu and returns the option selected
def runmenu(dat, menu, menu_command, parent):
	new = {}
	
	if parent is None:
		lastoption = "Exit"
	else:
		lastoption = "Return to %s menu" % parent['title']

	typ = "work"
	stat = "open"
	row = 0
	act = "new"
	prj = "all"
	title = "all"

	x = None 
	while x != ESC :   ## escape = 27
		row, t_i, nrow =  main_list(screen, dat, menu, menu_command, typ, stat, row, act, prj, title)
		x = action(screen, startx, ymax-6, act, t_i, dat)
		if x == ord('\t'):
			stat = "open"
			row = 0
			act = "new"
			lst = menu.keys()
			ind = lst.index(typ) + 1
			if ind == len(menu): ind = 0
			typ = lst[ind]
		elif x == curses.KEY_BTAB:
			stat = "open"
			row = 0
			act = "new"
			lst = menu.keys()
			ind = lst.index(typ) - 1
			if ind < 0 : ind = len(menu) - 1
			typ = lst[ind]
		elif x == curses.KEY_RIGHT:
			row = 0
			act = "new"
			lst = menu[typ].keys()
			ind = lst.index(stat) + 1
			if ind > len(menu[typ])-1: ind = 0
			stat = lst[ind]
		elif x == curses.KEY_LEFT:
			row = 0
			act = "new"
			lst = menu[typ].keys()
			ind = lst.index(stat) - 1
			if ind < 0: ind = 0  #len(menu[typ]) - 1
			stat = lst[ind]
		elif x == curses.KEY_UP:
			row = row - 1
			if row < 0: row = 0
		elif x == curses.KEY_DOWN:
			row = row + 1
			if row ==  nrow: row = nrow -1
		elif x == curses.KEY_SRIGHT:
			lst = menu_command
			ind = lst.index(act) + 1
			if ind ==  len(menu_command): ind = 0
			act = lst[ind]
		elif x == curses.KEY_SLEFT:
			lst = menu_command
			ind = lst.index(act) - 1
			if ind < 0: ind = len(menu_command) - 1
			act = lst[ind]
		elif x == ord('\n'):
			(yy,mm,dd,task,subtask) = t_i
			modify_task_new(screen, dat, yy, mm, dd, task, subtask)
		elif x == ord('d'):
			(yy,mm,dd,task,subtask) = t_i
			if dat[yy][mm][dd][task][subtask]["status"] == "deleted":
			      rm_task_kernel(dat, task, subtask, yy, mm, dd)
			else:
			      dat[yy][mm][dd][task][subtask]["status"] = "deleted"
			file_write(db_name(), dat)
		elif x == ord('s'):
			(yy,mm,dd,task,subtask) = t_i
			ypos, (ntid, nstid, ny, nm, nd) = get_task_subtask_id(screen, dat, 1)
			copy_task_kernel(screen, dat, task, subtask, yy, mm, dd, ntid, nstid, ny, nm, nd, ypos)
		elif x == ord('c'):
			(yy,mm,dd,task,subtask) = t_i
			dat[yy][mm][dd][task][subtask]["status"] = "close"
			file_write(db_name(), dat)
		

# This function calls showmenu and then acts on the selected item
def processmenu(dat, menu, menu_command, parent=None):
	runmenu(dat, menu, menu_command, parent)

if __name__ == '__main__':
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

	# Main program
	menu = {}
	menu_action = {}

	for typ in ["work", "pers", "all"]:
	      menu[typ] = {}
	      for stat in ["open", "close", "pending", "all"]:
		    menu[typ][stat] = {}
	
	menu_command = ["new", "move", "search"]

	menu_action["new"] = {}
	menu_action["move"] = {}
	menu_action["search"] = {}

	init_screen()
	processmenu(data, menu, menu_command)
	os.system('clear')
	curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
