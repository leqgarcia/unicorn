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


for step in job.steps:
    pp( job.steps[step].info)
    job.steps[step].open()
    job.steps[step].display_layer('top',1,1)
    job.steps[step].display_layer('bot',2,0)
    job.steps[step].setGenesisAttr('.comment','hello')
    job.PAUSE('hold on')
    job.steps[step].close()


exit(0)

