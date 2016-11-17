#!/usr/bin/env python
## move the detail files into the database file

import json
import sys, tempfile
import os

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

def file_write(name, d):
	f = open(name,'w')
	f.write(json.dumps(d, indent=4))
	f.close()

def db_name():
	return db_file_name

def db_path():
	return db_folder

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

        for yy in data:
            for mm in data[yy]:
                for dd in data[yy][mm]:
                    for task in data[yy][mm][dd]:
                        for key in data[yy][mm][dd][task]:
                            if key.startswith("subtask-"):
                                subtask = key
                                file = db_path() + "/detail/" +yy+"-"+mm+"-"+dd+"-"+task+"-"+subtask
                                if os.path.isfile(file):
                                     data[yy][mm][dd][task][subtask]["detail"] = open(file, 'r').read()
                                     os.unlink(file)
        file_write(db_name(), data)

