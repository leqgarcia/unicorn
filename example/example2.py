#!/bin/env python

_header = {
	'author'        :       'Mike J. Hopkins',
        'date'          :       '10/30/2002',
        'revision'      :       '1.1.6',
        'title'         :       'example2',
        'description'   :       '''
        This is another example Python script using the genClasses.py
	interface module.
        '''
        }

# Import standard Python modules
import os, sys, string

sys.path.append('/external/MasterDevelTree/src/Genesis/Merix/pylib')

# Import local resources
import genClasses

print genClasses._header
print genClasses.__file__

# Check for job and step ...
if 'JOB' and 'STEP' not in os.environ.keys():
	gen = genClasses.Genesis()
	gen.PAUSE('Need to run this from within a job and step...')
	sys.exit()
	
# instantiate the Job object.
job = genClasses.Job(os.environ['JOB'])

# get the current step
step = job.steps[os.environ['STEP']]

# open step, and clear all layers.
step.open('yes')
step.clearAll()

# dynamically get the value of the step's system attribute: comment
print 'value of this steps comment attribute:',
print step.comment

# Check out the output polarity of all the layers
pat = '%s	%s'
print pat % ('Layer', 'Polarity')
for lay in step.layers.keys():
	print pat % (step.layers[lay].name, step.layers[lay].out_polarity)


# List out some profile info
STR = '%f x %f' % (step.profile.xsize,step.profile.ysize )
print 'Step Size::',STR

# Access step and repeat table
STR = 'N:%f S:%f E:%f W:%f' % (step.sr.nBorder,step.sr.sBorder,step.sr.eBorder,step.sr.wBorder)
print 'borders::',STR


print "STEP - REPEAT TABLE....... (This doesn't work yet"
print '------------------------------'
pat = '%-12.12s %5f %5f %5f %5f %5f %5f %i %-3.3s'
for row in step.sr.table:
	STR = pat % (row.step, row.xanchor, row.yanchor, row.xdist, row.ydist, row.xnum, row.ynum, row.angle, row.mirror)
	print STR



