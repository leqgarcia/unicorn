#!/bin/env python
import os
from pprint import pprint as pp
from genClasses import g, Job



if os.environ.has_key('JOB'):
   job = Job(os.environ['JOB'])
else:
    g.PAUSE('You need to open a job first')
    print g.STATUS
    exit(0)


# for itm in job.steps['panel'].sr.__dict__.items():
#     pp(itm)

#for itm in job.steps:
#    print itm
#    print type(job.steps[itm])
#


for itm in job.steps:
    job.steps[itm].setGenesisAttr('.comment','')


for itm in job.steps:
    print job.steps[itm].etm_adapter_h



or_step = job.steps['orig']

or_step.open()

if 'graph' in or_step.layers:
    or_step.removeLayer('graph')

or_step.createLayer('graph','misc','signal')

or_step.display_layer('graph',1)



for x in range(10):
    if x%2:
        dir = 'CW'
    else:
        dir = 'CCW'
    or_step.addArc(0,0,x,x,x/2.0,x/2.0,'r10',dir)


#or_step.addArc(0.0,0.0,1,0,.5,-.5,'r10','CW')
#or_step.addArc(0.0,0.0,1,0,.5,-.5,'r10','CCW')


# if os.environ.has_key('STEP'):
job.PAUSE('STEP found ' + os.environ['STEP'])



or_step.removeLayer('graph')
exit(0)




for step in job.steps:
    pp( job.steps[step].info)
    job.steps[step].open()
    job.steps[step].display_layer('top',1,1)
    job.steps[step].display_layer('bot',2,0)
    job.steps[step].setGenesisAttr('.comment','hello')
    job.PAUSE('hold on')
    job.steps[step].close()



