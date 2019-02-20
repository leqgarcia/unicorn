#!/Python25/python.exe
import os
from genClasses import Job
from pprint import pprint as pp


print "XaaS Automation PyCAM  v0.0.1"
if "JOB" in os.environ.keys():
	print "Job is: " + os.environ["JOB"]
	job = Job(os.environ["JOB"])
else:
	print "No job is open"
	job = Job("82444")	
	job.open(False)
	#exit(0)

panel = job.steps['panel']

def xa_rqd_steps_extremes(step, rqd_steps):
	xmin = min( [sr.xmin for sr in panel.sr.table if sr.step in rqd_steps] )
	ymin = min( [sr.ymin for sr in panel.sr.table if sr.step in rqd_steps] )
	xmax = max( [sr.xmax for sr in panel.sr.table if sr.step in rqd_steps] )
	ymax = max( [sr.ymax for sr in panel.sr.table if sr.step in rqd_steps] )

	return xmin, ymin, xmax, ymax

xmin, ymin, xmax, ymax = xa_rqd_steps_extremes(panel, ['array','tdfsr'])

print xmin, ymin, xmax, ymax


panel.open()
