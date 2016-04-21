#!/usr/bin/env python

from support import *

copied_task = None



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
	
def main_list(wl, dat, menu, typ, stat, row, act, prj, title):
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

	return  row, true_index[row_index[row]], len(rows)


# This function displays the appropriate menu and returns the option selected
def runmenu(dat, menu, parent):
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
	while x != ord("q") : 
		try:
		      row, t_i, nrow =  main_list(screen, dat, menu, typ, stat, row, act, prj, title)
		except:
		      pass
		msg1 = "commands - d(elete), c(lose), p(aste), y(ank), n(ew), q(uit): "
		wr_win(screen, ymax-4, startx, msg1, n)
		x = screen.getch()
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
			if ind < 0: len(menu[typ]) - 1
			stat = lst[ind]
		elif x == curses.KEY_UP:
			row = row - 1
			if row < 0: row = 0
		elif x == curses.KEY_DOWN:
			row = row + 1
			if row ==  nrow: row = nrow -1
		elif x == ord('\n'):
			(yy,mm,dd,task,subtask) = t_i
			modify_task(screen, dat, yy, mm, dd, task, subtask)
		elif x == ord('d'):
			if confirm(screen, "Do you want to delete this task (y/n): ", ymax-4) == "y":
			      (yy,mm,dd,task,subtask) = t_i
			      rm_task_kernel(dat, task, subtask, yy, mm, dd)
		elif x == ord('y'):
			copied_task = t_i
		elif x == ord('p'):
			try:
			      (yy,mm,dd,task,subtask) = copied_task
			      ypos, (ntid, nstid, ny, nm, nd) = get_task_subtask_id(screen, dat, 1)
			      paste_task_kernel(screen, dat, task, subtask, yy, mm, dd, ntid, nstid, ny, nm, nd, ypos)
			      copied_task = None
			except:
			      pass
		elif x == ord('c'):
			(yy,mm,dd,task,subtask) = t_i
			dat[yy][mm][dd][task][subtask]["status"] = "close"
			file_write(db_name(), dat)
		elif x == ord('n'):
			add_newtask(screen, dat, typ)

# This function calls showmenu and then acts on the selected item
def processmenu(dat, menu, parent=None):
	runmenu(dat, menu, parent)

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

	for typ in ["work", "pers", "all"]:
	      menu[typ] = {}
	      for stat in ["open", "close", "pending", "all"]:
		    menu[typ][stat] = {}

	init_screen()
	processmenu(data, menu)
	os.system('clear')
	curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
