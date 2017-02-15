#!/usr/bin/env python
#-*- coding: utf-8 -*-

from support import *

copied_task = None



def make_show_list(dat, typ, prj, title, stat):
	lst, types, stats, projs, titles = sorted_key_list(dat)
	tbl = []
	table_index = []
	l = 0
	b = " "
	for index, (yy,mm,dd,task, subtask) in enumerate(lst):
		td = dat[yy][mm][dd][task]
		new_dt = datetime.date(int(yy),int(mm),int(dd))
		if td["type"] == typ or typ == "all":
			std = td[subtask]
			if td["project"] == prj or prj == "all":
				if td["task title"] == title or title == "all":
					if std["status"] == stat or stat == "all":
						l = len(table_index)
						tbl.append(one_line(l, yy, mm, dd, td, std))
						table_index.append(index)
	dt = datetime.date.today()
	yy_today = dt.year
	mm_today = dt.month
	dd_today = dt.day
	for row, val in enumerate(tbl):
	      (yy,mm,dd,task,subtask) = lst[table_index[row]]
	      if int(yy) >= yy_today and int(mm) >= mm_today and int(dd) >= dd_today:
		    break
	return (tbl, table_index, lst, row)

def make_report(f, dat, typ, prj, title, stat):
	lst, types, stats, projs, titles = sorted_key_list(dat)
	tbl = []
	table_index = []
	l = 0
	b = " "
        c = "="
        h = "-"
        n = "\n"
#        f = open("/tmp/tmp12341",'w')
        f.write("*"*10 + b + "Report" + b + "*"*10 + n)
        for index, (yy,mm,dd,task, subtask) in enumerate(lst):
                td = dat[yy][mm][dd][task]
                new_dt = datetime.date(int(yy),int(mm),int(dd))
                if td["type"] == typ or typ == "all":
                        std = td[subtask]
                        if td["project"] == prj or prj == "all":
                                if td["task title"] == title or title == "all":
                                        if std["status"] == stat or stat == "all":
                                                l = len(table_index)
                                                strn = yy + h + mm + h + dd + n
                                                f.write(c*len(strn)+n)
                                                f.write("No.: " + str(l).zfill(3)+n)
                                                f.write("Date: " + strn)
                                                f.write("Start: " + std["start"].encode(koden) + n)
                                                f.write("End: " + std["end"].encode(koden) + n)
                                                f.write("Project: " + td["project"].encode(koden) + n)
                                                f.write("Task: " + td["task title"].encode(koden) + n)
                                                f.write("Sub Task: " + std["subtask title"].encode(koden) + n)
                                                f.write("Detail: " + n + std["detail"].encode(koden) + n )
                                                f.write("Link: " + std["link"].encode(koden) + n)
                                                f.write("Attachment: " + std["attachment"].encode(koden) + n)
#                                                filename = db_path() + "/detail/" +yy+"-"+mm+"-"+dd+"-"+task+"-"+subtask
#                                                try:
#                                                    fl = open(filename)
#                                                    f.write("Description:" + n)
#                                                    f.write(fl.read())
#                                                    fl.close()
#                                                except:
#                                                    pass
#                                                f.write(n)
#
                                                tbl.append(one_line(l, yy, mm, dd, td, std))
                                                table_index.append(index)
        #f.close()
        f.flush()
	return 
def list_range(r, l):
	w = 10
	f = r / w
	s = f * w
	e = (f+1) * w
	if e > l: e = l
	return range(s, e)	


	
def main_list(wl, dat, menu, typ, stat, row, rows):
	wl.clear()
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
		for line in list_range(row, len(rows[0])):
			textstyle = n
			if row == line:
				textstyle = h
			wr_win(screen, menu3y, menu3x, rows[0][line], textstyle)
			menu3y = menu3y  + 1
	except:
		pass
	menu4x = startx
	menu4y = ymax-4


# This function displays the appropriate menu and returns the option selected
def runmenu(dat, menu, parent):
	new = {}
	
	if parent is None:
		lastoption = "Exit"
	else:
		lastoption = "Return to %s menu" % parent['title']

	typ = "work"
	stat = "open"
	act = "new"
	prj = "all"
	title = "all"
        filt = 0
	row_arr = make_show_list(dat, typ, prj, title, stat)
	nrow = rows_len(row_arr)
	row = row_arr[3] #row_for_today(row_arr)

	x = None 
	msg1 = "commands - d(elete), c(lose), p(aste), y(ank), n(ew), q(uit): "
	while x != ord("q") : 
		try:
		      main_list(screen, dat, menu, typ, stat, row, row_arr)
		except:
		      pass
		wr_win(screen, ymax-4, startx, msg1, n)
		x = screen.getch()
		if x == ord('\t'):
			stat = "open"
			row = 0
                        filt = 0
			act = "new"
	                prj = "all"
                        title = "all"
			lst = menu.keys()
			ind = lst.index(typ) + 1
			if ind == len(menu): ind = 0
			typ = lst[ind]
			row_arr = make_show_list(dat, typ, prj, title, stat)
			#row = row_for_today(row_arr)
	                row = row_arr[3] #row_for_today(row_arr)
			nrow = rows_len(row_arr)
		elif x == curses.KEY_BTAB:
			stat = "open"
			row = 0
			act = "new"
	                prj = "all"
                        title = "all"
                        filt = 0
			lst = menu.keys()
			ind = lst.index(typ) - 1
			if ind < 0 : ind = len(menu) - 1
			typ = lst[ind]
			row_arr = make_show_list(dat, typ, prj, title, stat)
			#row = row_for_today(row_arr)
	                row = row_arr[3] #row_for_today(row_arr)
			nrow = rows_len(row_arr)
		elif x == curses.KEY_RIGHT:
			row = 0
			act = "new"
			lst = menu[typ].keys()
			ind = lst.index(stat) + 1
			if ind > len(menu[typ])-1: ind = 0
			stat = lst[ind]
			row_arr = make_show_list(dat, typ, prj, title, stat)
			#row = row_for_today(row_arr)
	                row = row_arr[3] #row_for_today(row_arr)
			nrow = rows_len(row_arr)
		elif x == curses.KEY_LEFT:
			row = 0
			act = "new"
			lst = menu[typ].keys()
			ind = lst.index(stat) - 1
			if ind < 0: len(menu[typ]) - 1
			stat = lst[ind]
			row_arr = make_show_list(dat, typ, prj, title, stat)
			#row = row_for_today(row_arr)
	                row = row_arr[3] #row_for_today(row_arr)
			nrow = rows_len(row_arr)
		elif x == curses.KEY_UP:
			row = row - 1
			if row < 0: row = 0
		elif x == curses.KEY_DOWN:
			row = row + 1
			if row ==  nrow: row = nrow -1
		elif x == ord('\n'):
			(yy,mm,dd,task,subtask) = get_keys(row, row_arr)
			past = past_task(yy,mm,dd, dat[yy][mm][dd][task][subtask]["end"]) 
			if past :
				view_task(screen, dat, yy, mm, dd, task, subtask)
                        else:
				modify_task(screen, dat, yy, mm, dd, task, subtask)
			row_arr = make_show_list(dat, typ, prj, title, stat)
			nrow = rows_len(row_arr)
		elif x == ord('r'):
                        with tempfile.NamedTemporaryFile(suffix=".tmp") as f:
                            make_report(f, dat, typ, prj, title, stat)
                            p = subprocess.Popen("gvim " + f.name, stdout=subprocess.PIPE, shell=True)

                            (output, err) = p.communicate()  
                            p.wait()

		elif x == ord('d'):
			if confirm(screen, "Do you want to delete this task (y/n): ", ymax-4) == "y":
			      (yy,mm,dd,task,subtask) = get_keys(row, row_arr)
			      rm_task_kernel(dat, task, subtask, yy, mm, dd)
			row_arr = make_show_list(dat, typ, prj, title, stat)
			nrow = rows_len(row_arr)
                elif x == ord('+'):
			(yy,mm,dd,task,subtask) = get_keys(row, row_arr)
                        if filt == 0:
                            prj = dat[yy][mm][dd][task]["project"]
                            filt = filt + 1
                        elif filt == 1:
                            title = dat[yy][mm][dd][task]["task title"]
                            filt = filt + 1
                        
			row_arr = make_show_list(dat, typ, prj, title, stat)
			#row = row_for_today(row_arr)
	                row = row_arr[3] #row_for_today(row_arr)
			nrow = rows_len(row_arr)
                elif x == ord('-'):
			(yy,mm,dd,task,subtask) = get_keys(row, row_arr)
                        if filt == 2:
                            title = "all"
                            filt = filt - 1
                        elif filt == 1:
                            prj = "all"
                            filt = filt - 1
                        
			row_arr = make_show_list(dat, typ, prj, title, stat)
			#row = row_for_today(row_arr)
	                row = row_arr[3] #row_for_today(row_arr)
			nrow = rows_len(row_arr)
		elif x == ord('y'):
			copied_task = get_keys(row, row_arr)
			row_arr = make_show_list(dat, typ, prj, title, stat)
			nrow = rows_len(row_arr)
		elif x == ord('p'):
			(yy,mm,dd,task,subtask) = get_keys(row, row_arr)
                        nday = datetime.date(int(yy), int(mm), int(dd))
			ypos, (ntid, nstid, ny, nm, nd) = get_task_subtask_id(screen, dat, 1, nday)
			try:
			      (oyy,omm,odd,otask,osubtask) = copied_task
			      paste_task_kernel(screen, dat, otask, osubtask, oyy, omm, odd, ntid, nstid, ny, nm, nd, ypos)
			      #copied_task = None
			except:
			      pass
			row_arr = make_show_list(dat, typ, prj, title, stat)
			nrow = rows_len(row_arr)
		elif x == ord('c'):
			(yy,mm,dd,task,subtask) = get_keys(row, row_arr)
			dat[yy][mm][dd][task][subtask]["status"] = "close"
			file_write(db_name(), dat)
			row_arr = make_show_list(dat, typ, prj, title, stat)
			nrow = rows_len(row_arr)
		elif x == ord('n'):
			(yy,mm,dd,task,subtask) = get_keys(row, row_arr)
                        nday = datetime.date(int(yy), int(mm), int(dd))

			add_newtask(screen, dat, typ, nday)
			row_arr = make_show_list(dat, typ, prj, title, stat)
			nrow = rows_len(row_arr)

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
