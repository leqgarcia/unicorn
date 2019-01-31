#!/usr/local/bin/python

_header = {
	'author'        :       'Mike J. Hopkins',
        'date'          :       '10/30/2002',
        'revision'      :       '1.1.6',
        'title'         :       'example',
        'description'   :       '''
        This is an example Python script using the genClasses.py
	interface module.
        '''
        }

# Import standard Python modules
import os, sys, string

# Import local resources
sys.path.append('/genesis/e81/all/python')
import genClasses

# See if we've got Tkinter installed
try:
	from Tkinter import *
	myInter = 'Tk'
except:
	myInter = 'GUI'

# Interface using GUI
def guiInterface(label):
	print 'Executing GUI interface...'
	# Initialize a Genesis object, for paths, etc.
	gen = genClasses.Genesis()
	gui = os.path.join(gen.edir, 'all', 'gui')
	
	# Run the GUI
	fo = open(gen.tmpfile, 'w')
	fo.write('WIN 200 200\nTEXT result '+label+'\nEND\n')
	fo.close()
	fd = os.popen(gui+' '+gen.tmpfile)
	for line in fd.readlines():
		print line
		line = line[4:]
		exec(line)
	return result
	
# Interface using Tkinter
def tkInterface(label):
	print 'Executing Tk dialog...'
	dbox = SimpleDialog(label, label)
	return dbox.result.get()
	
# Simple Tk class defining a dialog-box
class SimpleDialog(Frame):
	def __init__(self, title, label):
		Frame.__init__(self)
		self.label = label
		self.master.title(title)
		self.result = StringVar()
		self.pack(expand=1, fill=BOTH)
		
		self.buildGui()
		
		# Make modal
		self.grab_set()
		self.focus_set()
		self.wait_window()

	def buildGui(self):
		self.frame = Frame(self)
		self.lab = Label(self.frame, text=self.label)
		self.ent = Entry(self.frame, textvariable=self.result)
		self.ent.bind('<Return>', self.ok_cb)
		self.lab.pack(side=LEFT)
		self.ent.pack(side=LEFT)
		self.ok = Button(self, text='OK', command=self.ok_cb)

		self.frame.pack(side=TOP, expand=1, fill=BOTH)
		self.ok.pack(side=TOP, expand=0, fill=X)

	def ok_cb(self, *e):
		self.destroy()

# Main routine...
if __name__ == '__main__':
	
	# Check to see which interface is available
	if myInter == 'Tk':
		myInter = tkInterface
	else:
		myInter = guiInterface

	# Run the interface, get the job name
	jobName = myInter('Enter Job Name')
	print 'My Job Name is::'+jobName
	
	# Instantiate the job object, open it without checkout
	job = genClasses.Job(jobName)
	
	job.open(1)
	
	# Run the interface to get a step name, Create a new step
	newStep = myInter('New step name to create')
	if newStep in job.steps.keys():
		job.PAUSE('Step '+newStep+' exists...create '+newStep+'-mjh ?')
		newStep = newStep+'-mjh'
	job.addStep(newStep)
	
	# open the new step
	job.steps[newStep].open()
	
	# Create a profile, zoom home, display the first layer
	newLayer = myInter('New layer name to create')
	if newLayer in job.steps[newStep].layers:
	        job.PAUSE('Layer'+newLayer+' exists...create '+newLayer+'-drg ?')
		newLayer = newLayer + '-drg'
	job.steps[newStep].cmd.createLayer(newLayer)
	lay = job.matrix.info['gROWname'][0]
	job.COM('profile_rect,x1=0,y1=0,x2=5,y2=5')
	job.COM('zoom_home')
	job.COM('display_layer,name='+lay+',display=yes,number=1')
	job.COM('work_layer,name='+lay)
	
	# Add a pad at the coordinate specified by MOUSE
	job.MOUSE('Select a point to add a pad')
	x,y = string.split(job.MOUSEANS)
	job.COM('add_pad,attributes=no,x='+x+',y='+y+',symbol=r100,polarity=positive')
	
	# Pause, then remove step and close up shop
	job.PAUSE('All done.')
	job.steps[newStep].close()
	job.removeStep(newStep)
	job.close(1)
	
	sys.exit(0)
	
