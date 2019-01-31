#!/bin/env python

_header = {
        'author'           :       'Daniel R. Gowans',
        'initialdate'      :       'September 10, 2003',
        'revisiondate'     :       'Sept 12, 2003',
        'revision'         :       'v1.0',
        'title'            :       'create_outline',
        'checklists'       :       '',
        'forms'            :       '',
        'other_resources'  :       '',
        'description'      :       '''
        This program is used to generate an outline of the board.  This will be used for thieving, 
	board checks, drill stuff, and a variety of other utilities.  This will be maintained over
	the outline portion of the thieving script, which will be obsoleted (however it is left in
	the thieving script)
	- Added prompt for v_cut, which then bumps selected lines by 50 mil.
        '''
        }

#Import Standard Modules
import os, string, sys, re, time

#Import Genesis specific resources
#sys.path.append('/genesis/e81/all/python')
#sys.path.append('/genesis/sys/scripts/python/modules')
sys.path.append('/genesis/sys/scripts/python/dev/testmods')
import genClasses

#Import the GUI specific classes
import Tkinter, tkFont
from Tkinter import *

###############################################
# Set up running window/GUI Application class
###############################################

# Create an extention class to Frame
class SelWin(Frame):
        # This is run when the class is instantiated
        def __init__(self,parent=None):
                Frame.__init__(self,parent)
                self.config(bg='darkgreen')		# change window background to dark green
                self.pack(padx=20,pady=20)		# put 20 pixel border on frame
                self.jobName=''				# init job name var
                self.stepName=''			# init step name var
                self.status = genClasses.Top()		# gather database status from genesis
                self.getInfo()          		# run the getInfo method below
          
        # The initial portion of the script.  This opens the GUI and configures
        # it, depending on whether the user starts it in a job/step, or neither.        
        def getInfo(self):
                
                self.wasInJob = 0		# Tells if script was started from within a job
                self.wasInStep = 0		# Tells if script was started from withing a step
                
                self.CustOutlineLayer = 'fabulous'  	# fab,dr  The layer with the fab drawing of the board profile - set to something we'd never have, so it would always prompt
                self.outlineLayer = 'outline'   # name of layer showing board edge/outline
                
                self.workLayer = 't_work'       # name of working layer for thieving stuff
                
                # Add two labels to GUI
                Label(self, font=boldFont,text='Running Outline Creation Operation',fg='yellow',bg='darkgreen',).pack(side=TOP)
                self.jobLabel = Label(self,text='Please Select a Job',fg='gray80',bg='darkgreen')
                
                # This is a scrollbar object for the job selection list
                self.scrollList = Scrollbar(self,orient=VERTICAL,bg='blue')
                # This is the list box that will hold jobs/steps to select.
		self.ourListBox = Listbox(self, yscrollcommand=self.scrollList.set, bg='black',fg='gray80')
                #attach scroll bar to list box
		self.scrollList.config(command=self.ourListBox.yview)
                #add button to use for job selection
                self.but1 = Button(self, font=buttonFont, text='Select Job', command=self.getJob, bg='blue', fg='yellow')
                
                # This statement jumps to the correct procedure based on whether in Job/step or not
                if (self.status.currentJob()):  # if in a job...
                        self.jobName = self.status.currentJob()		# This is like $JOB var is csh
                        self.wasInJob = 1				# This variable tells us if we were in a job when started
                        if (self.status.currentStep()):  # if in a step...
                                self.stepName = self.status.currentStep()	# This is like $STEP in csh
                                self.job = genClasses.Job(self.jobName)		# create Genesis-python job class
                                self.beforeAction()				# run beforeAction method - skip job and step selection
                                self.wasInStep = 1
                        else:
                                self.makeStepChoice()  				# if in a job, just choose step
                else:
                        self.makeJobChoice()					# if not in job or step, go to choose job
                
        # This is run if the user isn't in a job, and needs to select one.
        def makeJobChoice(self):
                self.jobLabel.pack(side=TOP,pady=5)
		self.allJobs=self.status.listJobs()			# this gets list of all the jobs in the database
                # populate the listbox with the job names in the database
		for jobName in self.allJobs:
		        self.ourListBox.insert(END, jobName)
                # put GUI components on screen (in frame)
		self.ourListBox.pack(side=LEFT, fill=BOTH, expand=1)
		self.scrollList.pack(side=LEFT, fill=Y)
                self.but1.pack(side=RIGHT, padx=10, pady=5)
                
        # This retrieves the job selected in the makeJobChoice method
	def getJob(self):
                jobIndex = self.ourListBox.curselection()	# get value selected in list box
                self.ourListBox.delete(0, END)			# delete all the entries in list box
        	jobNumber = int(jobIndex[0])			# get index of selected entry
        	self.jobName = str(self.allJobs[jobNumber])	# Retrieve job name from list using index
                self.makeStepChoice()				# go to method to choose step
        
        # This is run if a step needs to be chosen
        def makeStepChoice(self):
                self.jobLabel.config(font=largerFont,text='Running on job: ' + self.jobName)
                self.jobLabel.pack(side=TOP,pady=5)
		self.job = genClasses.Job(self.jobName)		# create the python-genesis job class instance
                self.job.open(1)				# Open the job - 1 means check out
                self.allSteps=self.job.steps.keys()		# save a list of the steps
                
                # Checks to see if there are any steps.  Errors if no steps on which to run
                if len(self.allSteps) < 1:
                        self.errorEvent()
                
                # Gets step names for list box
                for stepName in self.allSteps:
                        self.ourListBox.insert(END, stepName)
                # pack in those GUI components!
                self.ourListBox.pack(side=LEFT, fill=BOTH, expand=1)
		self.scrollList.pack(side=LEFT, fill=Y)
                self.but1.config(text='Select Step',command=self.getStep)
                self.but1.pack(side=RIGHT, padx=10, pady=5)
                                              
        # Gets the step chosen - same as in getJob method
        def getStep(self):
                stepIndex = self.ourListBox.curselection()
                stepNumber = int(stepIndex[0])
                self.stepName = str(self.allSteps[stepNumber])
                self.job.steps[self.stepName].open(iconic='yes')
                self.beforeAction()
 		
        # Prepares to run configuration and allows user to initiate, get bearings
        def beforeAction(self):
                #get rid of objects used to select job/step
                self.ourListBox.destroy()
                self.scrollList.destroy()
                
		# Change label on screen
                self.jobLabel.config(font=buttonFont,text='Ready to generate outline in job ' + self.jobName + ', step ' + self.stepName)
                self.jobLabel.pack(side=TOP, pady=5)
                
                # Put in an exit button
                self.exitbut = Button(self, font=buttonFont1, text='Exit Program', command=self.quitAll, bg='grey80', fg='grey10')
                self.exitbut.pack(side=BOTTOM, padx=10, pady=10)

                # Change bottom button to lead to next step
		self.but1.destroy()
		self.but1 = Button(self, font=buttonFont, bg='blue', fg='yellow')
                self.but1.config(text='Create Board Edge/Outline',command=self.verifyProfileExists)
                self.but1.pack(side=BOTTOM)
        
        # Get profile information
        def verifyProfileExists(self):
                prof = self.job.steps[self.stepName].profile   # retrieve profile coordinates
                print "Profile Area " + str(prof.xmin) + ',' + str(prof.ymin) + ' by ' + str (prof.xmax) + ',' + str(prof.ymax)
                # Check to see if the profile is tiny (meaning it was never drawn)
                if (abs(prof.xmax - prof.xmin) < 0.01):
                        self.job.COM('zoom_home')
	                self.job.COM('filter_reset,filter_name=popup')
        	        self.job.steps[self.stepName].open(iconic='no')
                	self.job.PAUSE("Draw a profile for this step.  Stay as close to board edge as possible.")                            
                	self.job.steps[self.stepName].open(iconic='yes')
                self.selectOutlineLayer()
        
        # NOW should be the profile stuff
        # Select fab layer
        def selectOutlineLayer(self):
		self.taskLabel = Label(self, text='Finding layer that has a board edge outline...', fg='gray80',bg='darkgreen')
		self.taskLabel.pack(side=TOP)
                self.jobLabel.config(font=buttonFont,text='Working on job ' + self.jobName + ', step ' + self.stepName)
                # if outline layer exists, then it is unlikely the program needs to find the edge again
		if self.job.steps[self.stepName].isLayer(self.outlineLayer):
			self.CustOutlineLayer = self.outlineLayer
			self.but1.pack_forget()
			self.verifyOutline()		
                # if no edge layer, but there is a fab drawing, then generate edge from that
                elif self.job.steps[self.stepName].isLayer(self.CustOutlineLayer):
                        self.genProf()
                # if neither, user must select a layer that could be used to extrapolate an edge
                else:
                        self.getLayerChoice()
       
        # If fab doesn't exist, list layers and have user select which layer to use
        def getLayerChoice(self):
		# This is a scrollbar object for the job selection list
	        self.scrollList = Scrollbar(self,orient=VERTICAL,bg='blue')
        	# This is the list box that will hold jobs/steps to select.
		self.ourListBox = Listbox(self, yscrollcommand=self.scrollList.set, bg='black',fg='gray80')
                #attach scroll bar to list box
		self.scrollList.config(command=self.ourListBox.yview)
                #add button to use for job selection
		self.but1.config(text='Select Layer with Board Edge Outline',command=self.getLayer)
                self.allLayers = self.job.steps[self.stepName].layers.keys()
		self.allLayers.sort()
                for layerName in self.allLayers:
		        self.ourListBox.insert(END, layerName)
		self.ourListBox.pack(side=LEFT, fill=BOTH, expand=1)
		self.scrollList.pack(side=LEFT, fill=Y)
		self.job.steps[self.stepName].open(iconic='no')
                self.job.PAUSE('Please find a layer with a board edge outline drawn (often a fab sheet)')
		self.job.steps[self.stepName].open(iconic='yes')
        
	# grabs user choice from the list box
        def getLayer(self):
        	layerIndex = self.ourListBox.curselection()
                self.ourListBox.delete(0, END)
        	layerNumber = int(layerIndex[0])
        	self.CustOutlineLayer = str(self.allLayers[layerNumber])
		self.scrollList.destroy()
                self.ourListBox.destroy()
		self.but1.pack_forget()
		self.taskLabel.config(text="Working on extracting board edge...")
		self.genProf()                
        
        # Generate board edge layer.  This uses a funky algorithm that finds the longest line on the 
        # layer and then traces all the lines connected to its edges, in a long chain.
	def genProf(self):
		
		self.job.steps[self.stepName].clearAll()                
                self.job.steps[self.stepName].layers[self.CustOutlineLayer].display(1)
                
                #self.job.COM('disp_off')
                
                # Selected longest feature(s)
	        # put it in a dictionary - have list of longest lines inside profile here.
                self.job.COM('sel_clear_feat')
                self.job.COM('filter_reset,filter_name=popup')
                self.job.COM('filter_set,filter_name=popup,update_popup=no,profile=in,feat_types=line')
                self.job.COM('filter_area_strt')
	        # Selects only lines from 100 mil to 50 inches long
		self.job.COM('filter_area_end,layer=,filter_name=popup,operation=select,area_type=none,lines_only=yes,min_len=0.1,max_len=50,min_angle=0,max_angle=360')
		
                features_dict = self.job.steps[self.stepName].layers[self.CustOutlineLayer].featSelOut()
		
		# For DEBUG
		#features_dict_2 = self.job.steps[self.stepName].layers[self.CustOutlineLayer].featOut(fileName = '/tmp/dantest1')
		#self.job.printFeatureDict(features_dict)
		#self.job.printFeatureDict(features_dict_2)
                
                size = 10.0	# This is size (in microns) of the imaginary rectangle drawn around the start
                		# and end points of each line.  Anything intersecting this rectangle is then selected
                length = 0.0	# sets up length variable, which will hold the length of a line in some parts
                index = 0	# sets up line list index
		
                # Check the features dictionary.  We should have selected some lines already and created a feature dictionary
		if (len(features_dict['lines']) < 1):
			self.job.PAUSE('There are no lines in that layer.  Please at least select a layer with some lines.')
			self.CustOutlineLayer = 'nothing'
			self.selectOutlineLayer()
			return

		# Create a profile layer.  If it exists, delete it and recreate
                if self.job.steps[self.stepName].isLayer(self.outlineLayer):
                        self.job.matrix.deleteRow(self.outlineLayer)
                self.job.steps[self.stepName].createLayer(self.outlineLayer)                
                
		# Go through the feature list and grab the longest line
                for x in range(len(features_dict['lines'])):
                        l = features_dict['lines'][x].len
                        if  l > length:
                                index = x
                                length = l
               
                # These lists hold the rectangles that are used to select chains
                # We append the rectangles around start and end points of longest lines
                # rectList holds all the unique rectangles we have found.  new_rects
                # holds new rectangles from each iteration of the algorithm
                rectList = []
                rectList.append(self.getLineStartRect(features_dict['lines'][index],size))
                rectList.append(self.getLineEndRect(features_dict['lines'][index],size))
                
                new_rects = []
                new_rects.append(self.getLineStartRect(features_dict['lines'][index],size))
                new_rects.append(self.getLineEndRect(features_dict['lines'][index],size))
                #self.job.printFeatureDict(features_dict)
                
                # Now let's select everything that intersects these rectangles
                self.job.COM('sel_clear_feat')
                self.job.COM('filter_set,filter_name=popup,update_popup=no,profile=in,feat_types=line;arc')
		self.update()
		self.master.lift()
                          
                # Run until the break is executed, i.e. no new rectangles are found.
		while (1):
			# Select all lines or arcs intersecting new rectangles around end points
                        y = range(len(new_rects))
                        for x in y:
                                each_rect = new_rects[x]
                                self.job.COM('filter_area_strt')
	                        self.job.COM('filter_area_xy,x='+str(each_rect.x1)+',y='+str(each_rect.y1))
                                self.job.COM('filter_area_xy,x='+str(each_rect.x2)+',y='+str(each_rect.y2))
				self.job.COM('filter_area_end,layer=,filter_name=popup,operation=select,area_type=rectangle,inside_area=yes,intersect_area=yes,lines_only=no,ovals_only=no')
			# Output new selected features to dictionary
			features_dict = self.job.steps[self.stepName].layers[self.CustOutlineLayer].featSelOut()
                     	new_rects = []		# clear out the new rects list
                        
                        # This loop goes through the selected features and adds them to the rectangles lists
	                for each_line in features_dict['lines']:
        	                                
                	        # Put all endpoint rectangles in list
                                rect_s = self.getLineStartRect(each_line,size)
                                rect_e = self.getLineEndRect(each_line,size)
                                
                                same_s = 0
                                same_e = 0
                                for x in range(len(rectList)):
                                        same_s = same_s + self.compareRect(rect_s,rectList[x])
                                        same_e = same_e + self.compareRect(rect_e,rectList[x])
				if same_s == 0:
                                        rectList.append(rect_s)
                                        new_rects.append(rect_s)
                                if same_e == 0:
                                        rectList.append(rect_e)
                                        new_rects.append(rect_e)
                                                                 
                        # Same for any arcs
                        for each_arc in features_dict['arcs']:
                                
                                # Put all endpoint rectangles in list
                                rect_s = self.getLineStartRect(each_arc,size)
                                rect_e = self.getLineEndRect(each_arc,size)
                                
                                same_s = 0
                                same_e = 0
                                for x in range(len(rectList)):
                                        same_s = same_s + self.compareRect(rect_s,rectList[x])
                                        same_e = same_e + self.compareRect(rect_e,rectList[x])
                                               
				if same_s == 0:
                                        rectList.append(rect_s)
                                        new_rects.append(rect_s)
                                if same_e == 0:
                                        rectList.append(rect_e)
                                        new_rects.append(rect_e)

			# When no new rectangles are found, then the algorithm is complete
                        if len(new_rects) == 0:
                                break;
                        
                        #self.job.COM('sel_clear_feat')        
                #self.job.COM('disp_on')
                # Copy the information to a new layer
		self.update()
		self.master.lift()
                self.job.COM('sel_copy_other,dest=layer_name,target_layer=' + self.outlineLayer + ',invert=no,dx=0,dy=0,size=0')
                self.verifyOutline()
 
        # get an object with a rectangle of size 2*mils centered on line start
        def getLineStartRect(self, line, mils):
                rect = genClasses.Empty()
                rect.x1 = float(line.xs)-(mils/1000)
                rect.x2 = float(line.xs)+(mils/1000)
                rect.y1 = float(line.ys)-(mils/1000)
                rect.y2 = float(line.ys)+(mils/1000)
                return rect
                
        def getLineEndRect(self, line, mils):
                rect = genClasses.Empty()
                rect.x1 = float(line.xe)-(mils/1000)
                rect.x2 = float(line.xe)+(mils/1000)
                rect.y1 = float(line.ye)-(mils/1000)
                rect.y2 = float(line.ye)+(mils/1000)
                return rect
 
 	# Returns a 1 if rectangles are same within 0.002 inch
 	def compareRect(self, rect1, rect2):
                result = 0
                if (abs(rect1.x1-rect2.x1) > 0.002):
                	return result
                
                if (abs(rect1.y1-rect2.y1) > 0.002):
                        return result
 		result = 1
                return result                                

        
        # Switch to profile layer and have user verify
        def verifyOutline(self):
		self.taskLabel.config(text="Verifying new outline")
		self.update()
		self.master.lift()
		self.job.steps[self.stepName].clearAll()                
                self.job.steps[self.stepName].layers[self.outlineLayer].display(1)
        	
                self.job.COM('zoom_home')
                self.job.COM('filter_reset,filter_name=popup')
                self.job.steps[self.stepName].open(iconic='no')
                self.job.PAUSE('Please check that this layer contains the board edge/outline.  If not, repair or add it in.')                               
                self.job.steps[self.stepName].open(iconic='yes')
                self.addVcut()


	def addVcut(self):
		self.taskLabel.config(text="Widening v-cut areas")
		self.update()
		self.master.lift()
		self.job.steps[self.stepName].clearAll()
		self.job.steps[self.stepName].layers[self.outlineLayer].display(1)
		
		self.job.COM('zoom_home')
		self.job.COM('filter_reset,filter_name=popup')
                self.job.steps[self.stepName].open(iconic='no')
		self.job.PAUSE('Select all lines that will be V-CUT (cut with the rout v-bit)') 
		self.job.steps[self.stepName].open(iconic='yes')
		# If something was selected, bump it by 56 mil.
		if self.job.steps[self.stepName].featureSelected() > 0:
			self.job.COM('sel_resize,size=56,corner_ctl=no')
		self.updateTimeRecord()

	def updateTimeRecord(self):		
		# Update Time Record in User Files
		#-----------operation time record ---------
		self.job.VOF()
		now_str = time.asctime()
		self.job.COM('get_user_name')
		username = self.job.COMANS
		filename = self.job.dbpath + '/user/time_check'
		STR = 'Outline Creation completed at ' + now_str + ' by user ' + username
		self.job.VON()
		#Write it to the file
		file_out = open(filename,'a')
		file_out.write(STR + '\n')
		file_out.close()
		self.taskLabel.config(text="Outline creation complete!")
		self.update()
		self.master.lift()
                
        # Quits (takes back to where you were when you started)
        def quitAll(self):
                if (self.wasInJob and self.wasInStep):
                	self.job.steps[self.stepName].open(iconic='no')
                        self.quit()
                elif self.wasInJob:
                        self.job.steps[self.stepName].close()
                        self.quit()
                else:
                        #self.job.close(1)
                        self.quit()
            
        # Run if no steps found in job, or other errors
        def errorEvent(self,message='Error, must exit'):
                self.destroy()
                parent=None
                Frame.__init__(self,parent)
                self.config(bg='darkgreen')
                self.pack(padx=20,pady=20)
                Label(self, font=boldFont,text=message,fg='gray80',bg='darkgreen',).pack(side=TOP)
                Button(self,font=buttonFont,text='EXIT',command=self.quitAll,bg='blue', fg='white').pack(side=BOTTOM, padx=5, pady=5)
# END SelWin class
        	
        
##  MAIN ROUTINE
#  This is where execution begins.  The gui is run.  It takes care of running everything else.

# GUI is instantiated
root = Tkinter.Tk()

# Font selections are made
mainFontDesc = Tkinter.Button()['font']
entryFontDesc = Tkinter.Entry()['font']

# Fonts are setup
courierFont = tkFont.Font(family='Courier', size = 16)
boldFont = tkFont.Font(family='Arial',size = 15, weight = tkFont.BOLD)
buttonFont = tkFont.Font(family='Arial',size=14)
buttonFont1 = tkFont.Font(family='Arial',size=10)
largerFont = tkFont.Font(family='Arial',size=14)

# This is the GUI class
selectionWindow=SelWin()

# Configure GUI Name
selectionWindow.master.title('Genesis Python Script')
selectionWindow.master.config(bg='darkgreen')

# GUI is run
selectionWindow.mainloop()

sys.exit(0)

# END of MAIN
# END of PROGRAM
