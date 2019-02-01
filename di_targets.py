#!/bin/env python

import genClasses
import os
from genClasses import g
from pprint import pprint as pp



class di_interface(object):
    def __init__(self):
        if os.environ.has_key('JOB'):
            self.job = genClasses.Job(os.environ['JOB'])
        else:
            g.PAUSE('You need to open a job first')
            print g.STATUS
            exit(0)
    def layer_list(self):
        
        matrix = self.job.matrix.info 

        gROWcontext = matrix['gROWcontext']
        gROWlayer_type = matrix['gROWlayer_type']
        gROWname = matrix['gROWname']

        work_list = []
        reqd_types = ['drill',
                    'solder_mask',
                    'mixed', 'power_ground', 'signal']

        for i in range(len(gROWname)):
            if gROWcontext[i] == 'board':
                if gROWlayer_type[i] in reqd_types:
                    color = self.job.colors['hex'][gROWlayer_type[i]]
                    work_list.append(
                    [ gROWname[i]   , 
                    gROWlayer_type[i],
                    color  ] 
                    )
        return work_list



    