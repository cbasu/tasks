#!/usr/bin/env python

from support import *

status = sys.argv[1]
try:
	json_data=open("data.txt").read()
	data1 = json.loads(json_data)
	for yy in data1.keys():
		for mm in data1[yy].keys():
			for dd in data1[yy][mm].keys():
				for taskid in data1[yy][mm][dd].keys():
					data[yy][mm][dd][taskid] = data1[yy][mm][dd][taskid]
	for yy in data1.keys():
		for mm in data1[yy].keys():
			for dd in data1[yy][mm].keys():
				for taskid in data1[yy][mm][dd].keys():
					pj = data[yy][mm][dd][taskid]["project"]
					ti = data[yy][mm][dd][taskid]["title"]
					be = data[yy][mm][dd][taskid]["start"]
					en = data[yy][mm][dd][taskid]["end"]
					st = data[yy][mm][dd][taskid]["status"]
					if status == "all":
						print pj,":", ti, "(", be,"-", en, ")" 
					elif st == status:
						print pj,":", ti, "(", be,"-", en, ")" 
except:
	pass
#				


