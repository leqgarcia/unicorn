#!/bin/env python

_header = {
        'author'           :       'Daniel R. Gowans',
        'initialdate'      :       'June 30, 2003',
        'revisiondate'     :       'September 15, 2003',
        'revision'         :       'v1.1',
        'title'            :       'conv_pos_planes',
        'description'      :       '''
        This program/routine is used to automate the task of some steps of the conversion of 
	positive plane layer data to negative data.  It uses a GUI interface to select the job and step.  
	It must be run from within Genesis 2000. 
        
        The job can be run from the database window, in a job, or in a job and step.  It
        will ask for any information it needs.
	
	July 18 - now runs only on positive p/g planes
	July 18 - user can select if program runs removal of Non-Functional Pads on converted layers.
	September 15 - Need to still be able to run non-functional pad removal even if drill layers are ld1, ld2, etc.
        '''
        }

	# Error codes
	# 1 - contourization of old failed
	# 2 - Features overlap between positive and negative layer
	# 3 - Features overlap and contourization of old failed
	# 4 - Underlap of features
	# 5 - Underlap and original countourization of old failed
	# 6 - Underlap and overlap
	# 7 - Underlap, overlap, and original contourization failed oooh, nasty!


#Import Standard Modules
import os, string, sys, re

#Import Genesis specific resources
#sys.path.append('/genesis/e81/all/python')
#sys.path.append('/genesis/sys/scripts/python/modules')
sys.path.append('/genesis/sys/scripts/python/dev/testmods')

import genClasses

#Import the GUI specific classes
import Tkinter, tkFont

from Tkinter import *

####################
# Set up running window/GUI Application class
####################

# Create an extention class to Frame
class Pos_Plane_Conv(Frame):
        # This is run when the class is instantiated (I Think)
        def __init__(self,parent=None):
                Frame.__init__(self,parent)
                self.config(bg='darkgreen')
                self.pack(padx=20,pady=20)
                self.jobName=''
                self.stepName=''
                self.status = genClasses.Top()
                self.getInfo()          
                
        # The initial portion of the script.  This opens the GUI and configures
        # it, depending on whether the user starts it in a job/step, or neither.        
        def getInfo(self):

		#Other parameters setup
		self.workLayer = ''
		self.pwrLayers = []
		self.runList=[]         # Layers that conversion will be run on
		self.failedDict={}      # Holds failed layers
		self.remNFP=0           # Remove nonfunctional pads (default not to)
		self.drillLayer=0       # Change to one if there is a drill layer 'ld'
		
                self.wasInJob = 0
                self.wasInStep = 0
                Label(self, font=largerFont, text='Running Positive Plane Conversion Step',fg='yellow',bg='darkgreen',).pack(side=TOP)
                self.jobLabel = Label(self,text='Please Select a Job',fg='gray80',bg='darkgreen')
                
                # This is a scrollbar object for the job selection list
                self.scrollList = Scrollbar(self,orient=VERTICAL,bg='blue')
		
                # This is the list box that will hold jobs/steps to select.
		self.ourListBox = Listbox(self, yscrollcommand=self.scrollList.set, bg='black',fg='gray80')
		self.scrollList.config(command=self.ourListBox.yview)
                self.but1 = Button(self, text='Select Job', command=self.getJob, bg='blue', fg='white')
                
                # This statement jumps to the correct procedure based on whether in Job/step or not
                if (self.status.currentJob()):  # if in a job...
                        self.jobName = self.status.currentJob()
                        self.wasInJob = 1
                        if (self.status.currentStep()):  # if in a step...
                                self.stepName = self.status.currentStep()
                                self.job = genClasses.Job(self.jobName)
                                self.verifyProfileExists()
                                self.wasInStep = 1
                        else:
                                self.makeStepChoice()  
                else:
                        self.makeJobChoice()
                
        # This is run if the user isn't in a job, and needs to select one.
        def makeJobChoice(self):
                self.jobLabel.pack(side=TOP,pady=5)
		self.allJobs=self.status.listJobs()
                # populate the listbox with the job names in the database
		for jobName in self.allJobs:
		        self.ourListBox.insert(END, jobName)
		self.ourListBox.pack(side=LEFT, fill=BOTH, expand=1)
		self.scrollList.pack(side=LEFT, fill=Y)
                self.but1.pack(side=RIGHT, padx=10, pady=5)
                
        # This retrieves the job selected in the makeJobChoice method
	def getJob(self):
        	jobIndex = self.ourListBox.curselection()
                self.ourListBox.delete(0, END)
        	jobNumber = int(jobIndex[0])
        	self.jobName = str(self.allJobs[jobNumber])
                self.makeStepChoice()
        
        # This is run if a step needs to be chosen
        def makeStepChoice(self):
                self.jobLabel.config(text='Running on job: ' + self.jobName)
                self.jobLabel.pack(side=TOP,pady=5)
		self.job = genClasses.Job(self.jobName)
                self.job.open(1)
                self.allSteps=self.job.steps.keys()
                
                # Checks to see if there are any steps.  Errors if no steps to run on
                if len(self.allSteps) < 1:
                        self.errorEvent()
                
                # Gets step names for list box
                for stepName in self.allSteps:
                        self.ourListBox.insert(END, stepName)
                self.ourListBox.pack(side=LEFT, fill=BOTH, expand=1)
		self.scrollList.pack(side=LEFT, fill=Y)
                self.but1.config(text='Select Step',command=self.getStep)
                self.but1.pack(side=RIGHT, padx=10, pady=5)
                                              
        # Gets the step chosen  
        def getStep(self):
                stepIndex = self.ourListBox.curselection()
                print stepIndex
                stepNumber = int(stepIndex[0])
                print stepNumber
                self.stepName = str(self.allSteps[stepNumber])
                self.job.steps[self.stepName].open(iconic='yes')
		self.ourListBox.destroy()
                self.scrollList.destroy()
                self.verifyProfileExists()  # Change this if necessary
 
 
 	# THE STEPS BEFORE THIS ARE COMMON TO MOST OF THE SCRIPTS
         # Prepares to process the board
	 
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
                self.beforeConversion() 
	 
	def beforeConversion(self):      	
		#Get list of all the layer names that are board power/ground layers
		# Go through all the rows in the matrix.
                for row in range(1,len(self.job.matrix.info['gROWname'])):
                	row_info = self.job.matrix.getRowInfo(row)
			# Get pwr/gnd layers
                	if (row_info['type'] == 'power_ground') and (row_info['context'] == 'board') and (row_info['polarity'] == 'positive'):
                                self.pwrLayers.append(row_info['name'])
	               	row = int(row) + 1
                        	
		if (self.pwrLayers == ''):
                	self.errorEvent(message="Couldn't find any power/ground layers that were positive!") 
                
		self.jobLabel.config(text='Ready to run on job ' + self.jobName + ' in step ' + self.stepName)
                self.jobLabel.pack(side=TOP, pady=5)
                self.but1.config(text='Run on ALL positive Power/Ground Planes',command=self.runAll)
                self.but1.pack(side=BOTTOM, padx=10, pady=5)	
		
		self.but2 = Button(self, text='Choose from positive P/G Layers', command=self.setupConversion, bg='blue',fg='white')
		self.but2.pack(side=BOTTOM, pady=5)
		
	# Sets up the conversion, mostly just by allowing the user to select which power/ground layers need to be
	# converted.	
	def setupConversion(self):	
		self.but2.pack_forget()
	      	# These are the scrollbar objects for the layer selection lists
                self.scrollListSource = Scrollbar(self,orient=VERTICAL,bg='blue')
		self.scrollListDest = Scrollbar(self,orient=VERTICAL,bg='blue')
		
                # These are the list boxes that will hold layers to select/selected layers.
		self.layerListBoxSource = Listbox(self, yscrollcommand=self.scrollListSource.set, bg='black',fg='gray80')
		self.layerListBoxDest = Listbox(self, yscrollcommand=self.scrollListDest.set, bg='black',fg='gray80')
		
		# Attach the scroll bars to their lists
		self.scrollListSource.config(command=self.layerListBoxSource.yview)
		self.scrollListDest.config(command=self.layerListBoxDest.yview)
		
		# Put layers in source box
		for layer in self.pwrLayers:
		        self.layerListBoxSource.insert(END, layer)
		
		# Configure graphical elements
		self.buttonFrame = Frame(self,bg='darkGreen')
		self.addBut = Button(self.buttonFrame, text='Add ->', command=self.addLayer, bg='blue',fg='white')
		self.resetBut = Button(self.buttonFrame, text='Reset', command=self.resetLayerList, bg='blue', fg='yellow')
		self.checkBut = Button(self.buttonFrame, text='Check', command=self.checkGenesis,bg='blue',fg='yellow')
		self.but1.config(text='Run Conversion on Selected Power/Ground Layers',command=self.runSelected)
		
		# Put them in the frame
		self.layerListBoxSource.pack(side=LEFT, fill=BOTH, expand=1)
		self.scrollListSource.pack(side=LEFT, fill=Y)
		self.scrollListDest.pack(side=RIGHT, fill = Y)
		self.layerListBoxDest.pack(side=RIGHT, fill=BOTH, expand=1)
		self.addBut.pack(side=TOP, pady=10)
		self.resetBut.pack(side=TOP,pady=10)
		self.checkBut.pack(side=BOTTOM,pady=10)
		self.buttonFrame.pack(side=LEFT)
		
	def addLayer(self):
		layerIndex = self.layerListBoxSource.curselection()
		layerNumber = int(layerIndex[0])
		layerName = str(self.layerListBoxSource.get(layerNumber))
                self.layerListBoxSource.delete(layerIndex)
		self.layerListBoxDest.insert(END, layerName)
		
	def resetLayerList(self):
		self.layerListBoxSource.delete(0,END)
		self.layerListBoxDest.delete(0,END)
		# Put layers in source box
		for layer in self.pwrLayers:
		        self.layerListBoxSource.insert(END, layer)
			
	def checkGenesis(self):
		self.job.steps[self.stepName].open(iconic='no')
		self.job.PAUSE('Click "Continue Script" when ready...')
		self.job.steps[self.stepName].open(iconic='yes')
		self.master.lift()
		self.update()
			
	def runAll(self):
		self.but2.pack_forget()
		self.runList = self.pwrLayers
		self.chooseRemoveNFP()
	
	def runSelected(self):
		# Get list of layers on which to run
		self.runList = self.layerListBoxDest.get(0,END)
		
		# Remove all unnecessary elements.
		self.buttonFrame.destroy()
		self.addBut.destroy()
		self.resetBut.destroy()
		self.checkBut.destroy()
		self.scrollListSource.destroy()
		self.scrollListDest.destroy()
		self.layerListBoxSource.destroy()
		self.layerListBoxDest.destroy()
		self.chooseRemoveNFP()
		
	def chooseRemoveNFP(self):
		self.jobStatLabel = Label(self,text='Remove Non-Functional Pads Before Converting?',font=largerFont,fg='gray80',bg='darkgreen')
		self.jobStatLabel.pack(side=TOP,pady=5)
		self.but1.config(text='NO',command=self.dontRemoveNFP)
		self.but1.pack(side=BOTTOM)
		self.but2.config(text='YES',command=self.removeNFP)
		self.but2.pack(side=BOTTOM)
		
		
	def dontRemoveNFP(self):
		self.remNFP = 0
		self.runConversionLoop()
	
	def removeNFP(self):
		self.remNFP = 1
		self.runConversionLoop()
		
	# Runs the conversion procedure on all the layers in board
	def runConversionLoop(self):
		
		# Setup some GUI stuff
		self.jobLabel.config(text='Running on job ' + self.jobName + ' in step ' + self.stepName)
		self.but2.pack_forget()

		# Change drill layers to type drill and context board
		if self.remNFP:
			drill_layer_names = ['ld','ld1','ld2','ld3','ld4','ld5','drill']
			for drill_name in drill_layer_names:
				self.drillLayerExists = self.job.steps[self.stepName].isLayer(layer_name=drill_name)
				if self.drillLayerExists:
					self.job.matrix.modifyRow(drill_name,type='drill',context='misc')
					self.drillLayer = self.drillLayer + 1
					#self.job.PAUSE('Check that Drill is right')
			if not self.drillLayer:
				self.job.PAUSE("There is no known layer to use for drill (Need ld, ld1, ld2, ld3, ld4, ld5 or drill).  Not removing non-functional pads")

		STR = "Running on layer(s): "
		count = 1
		length = len(self.runList)
		for layerName in self.runList:
			if (count >= length):
				STR = STR + layerName
			else:
				STR = STR + layerName + ', '
			count = count + 1

		self.jobStatLabel.config(text=STR)
		self.statusLabel = Label(self,font=largerFont,text='',fg='gray80',bg='darkgreen')
		self.statusLabel.pack(side=TOP)
		self.but1.pack_forget()
		self.job.steps[self.stepName].open(iconic='yes')
		#Run the selected power/ground layers
		for layer in self.runList:
			self.workLayer = layer
			exist = int(self.job.matrix.getRow(self.workLayer))
			if (exist > 0):
				#self.job.PAUSE('Working on Layer ' + self.workLayer)
				self.statusLabel.config(text='Converting layer: ' + self.workLayer,fg='yellow')
				self.master.lift()
				self.update()
				self.runConversion()
			else:
				self.job.PAUSE('Error!  Layer ' + self.workLayer + ' not found!  Skipping...')
				print "Skipping missing layer " + self.workLayer
			
		self.job.steps[self.stepName].clearAll()
		
		keyList = self.failedDict.keys()
		keyList.sort()
		
		for key in keyList:
			self.job.PAUSE(self.failedDict[key])
		self.statusLabel.destroy()
		
		self.jobLabel.config(text='Job ' + self.jobName + ' in step ' + self.stepName + ' complete.')
                self.jobStatLabel.config(text='Conversion complete')
                self.but1.config(text='Exit Script',command=self.showResults)
                self.but1.pack(side=BOTTOM, padx=5, pady=5)
		self.master.lift()
		self.update()
	        #self.job.steps[self.stepName].open(iconic='no')
        
        # Begin the conversion process. This runs on all the board signal and power layers.
        def runConversion(self):
	
		self.job.steps[self.stepName].open(iconic='yes')
	
		# Then layer is renamed because now we are making modifications, and we don't want user to think, if
		# the script aborts early, that the layer is unchanged.
		sourceLayer=self.workLayer+'_src'
		destLayer=self.workLayer+'_new'
		compareLayer1=self.workLayer+'_cmp1'
		compareLayer2=self.workLayer+'_cmp2'
		compareLayer3=self.workLayer+'_cmp3'
		oldLayer=self.workLayer+'_old'
		destTestLayer=self.workLayer+'_dtst'
		testLayer='test_tmp'
		
		# By request, clean non functional pads very first
		if self.drillLayer and self.remNFP:
			self.statusLabel.config(text='Removing Non-functional Pads from ' + self.workLayer)
			self.master.lift()
			self.update()				
			self.job.COM('chklist_single,action=valor_dfm_nfpr,show=no')
			self.job.COM('chklist_erf,chklist=valor_dfm_nfpr,nact=1,erf=Isolated Pads')
			self.job.COM('chklist_cupd,chklist=valor_dfm_nfpr,nact=1,params=((pp_layer=' + self.workLayer + ')(pp_delete=Isolated;Duplicate)(pp_work=Features)(pp_drill=PTH;Via)(pp_non_drilled=Yes)(pp_in_selected=All)(pp_remove_mark=Remove)),mode=regular')
			self.job.COM('chklist_run,chklist=valor_dfm_nfpr,nact=1,area=profile')
			self.job.COM('chklist_close,chklist=valor_dfm_nfpr,mode=hide')
							
		# Initially, we need to copy the layer with _old to preserve it
		self.job.matrix.copyRow(self.workLayer,oldLayer,overwrite=1)
		
		# Create a blank layer with _dest where the new negative plane will be.
		sourceRow = int(self.job.matrix.getRow(self.workLayer))
		self.job.matrix.addLayer(destLayer,sourceRow,type='power_ground',polarity='negative')
				
		# Change some of the original layer's properties - change it to source layer
		newRow = int(self.job.matrix.getRow(oldLayer))
		self.job.matrix.modifyRow(self.workLayer,row=newRow,name=sourceLayer,context='misc')
						
		self.statusLabel.config(text='Converting layer: ' + self.workLayer)
		self.master.lift()
		self.update()			
				
		# Fill the profile of the new layer
		self.job.steps[self.stepName].clearAll()
		self.job.steps[self.stepName].layers[destLayer].display(1)
              	self.job.steps[self.stepName].layers[destLayer].work()
		self.job.COM('sr_fill,polarity=positive,step_margin_x=0,step_margin_y=0,step_max_dist_x=100,step_max_dist_y=100,sr_margin_x=0,sr_margin_y=0,sr_max_dist_x=0,sr_max_dist_y=0,nest_sr=yes,consider_feat=no,feat_margin=0,consider_drill=no,drill_margin=0,consider_rout=no,dest=affected_layers,layer=gnd2_new,attributes=no')
		
		# Copy the old layer to the new, inverting
		self.job.steps[self.stepName].clearAll()
		self.job.steps[self.stepName].layers[sourceLayer].display(1)
              	self.job.steps[self.stepName].layers[sourceLayer].work()
		self.job.COM('sel_copy_other,dest=layer_name,target_layer=' + destLayer + ',invert=yes,dx=0,dy=0,size=0')
		self.master.lift()
		self.update()
		
		# contourize the destination layer
		self.job.steps[self.stepName].clearAll()
		self.job.steps[self.stepName].layers[destLayer].display(1)
              	self.job.steps[self.stepName].layers[destLayer].work()
		# Make sure nothing is selected
		self.job.steps[self.stepName].clearSel()
		if self.job.steps[self.stepName].featureSelected() <= 0:
			self.job.COM('sel_contourize,accuracy=0.25,break_to_islands=yes,clean_hole_size=3,clean_hole_mode=x_and_y')
			
		self.master.lift()
		self.update()
		# do contour to pads
		self.job.steps[self.stepName].clearSel()
		self.job.COM('sel_cont2pad,match_tol=0.25,restriction=Symmetric,min_size=5,max_size=300,suffix=+++')
		
		#self.job.PAUSE('Mess it up')
		# Now we need to check to see if anything has been messed up.  We need to check for overlap between the old and new
		# layer, and also for "underlap"
		comparisonFailed = 0
		self.statusLabel.config(text='Comparing layers: ' + oldLayer + ' and ' + sourceLayer)
		self.master.lift()
		self.update()
		# contourize source layer
		self.job.steps[self.stepName].clearAll()
		self.job.steps[self.stepName].layers[sourceLayer].display(1)
		self.job.steps[self.stepName].layers[sourceLayer].work()
		# Make sure nothing is selected
		self.job.steps[self.stepName].clearSel()
		if self.job.steps[self.stepName].featureSelected() <= 0:
			self.job.COM('sel_contourize,accuracy=0.25,break_to_islands=yes,clean_hole_size=3,clean_hole_mode=x_and_y')
		self.master.lift()
		self.update()
		# Do graphical comparison between old and source layer to verify they are the same.  We 
		# Then have a basis to compare source layer to destination layer
		
		#COMMMENT this stuff out to not bother comparing contourized source with original
		STR = 'compare_layers,layer1=' + sourceLayer + ',job2=' + self.jobName + ',step2=' + self.stepName
		STR = STR + ',layer2=' + oldLayer + ',layer2_ext=,tol=0.4,area=profile,ignore_attr=,map_layer='
		STR = STR + compareLayer1 + ',map_layer_res=200'
		self.job.COM(STR)
		
		# if anything found, set user alert for visual compare and leave old layer.
		result = int(self.job.COMANS)
		if (result > 0):
			comparisonFailed = 1
		else:
			self.job.matrix.deleteRow(compareLayer1)
		self.job.matrix.deleteRow( sourceLayer + '+++')
		#STOP COMMENTING OUT HERE
		
		# Now we run a second compare.  This looks for overlapping features between source and destination
		# If they are true opposites (positive and negative) nothing will overlap - and nothing will get selected
		if (comparisonFailed < 8):
			self.statusLabel.config(text='Comparing layers: ' + sourceLayer + ' and ' + destLayer + ' for overlap')
			self.master.lift()
			self.update()
			# Do a reference selection for covering features between source layer and destination layer.
			# Copy destination to new layer
			self.job.matrix.copyRow(destLayer,destTestLayer,overwrite=1)
			# reduce destination by 2 mils
			self.job.steps[self.stepName].clearAll()
			self.job.steps[self.stepName].layers[destTestLayer].display(1)
	              	self.job.steps[self.stepName].layers[destTestLayer].work()
			self.job.steps[self.stepName].clearSel()
			self.job.COM('sel_resize,size=-2,corner_ctl=no')
			# ref selection covered compared to source layer
			self.job.steps[self.stepName].clearSel()
			STR = 'sel_ref_feat,layers=' + sourceLayer
			STR = STR + ',use=filter,mode=touch,f_types=line\;pad\;surface\;arc\;text,polarity='
			STR = STR + 'positive\;negative,include_syms=,exclude_syms='
			self.job.COM(STR)		
			# Fail if anything selected
			if self.job.steps[self.stepName].featureSelected() > 0:
				#create compare layer
				self.job.matrix.addLayer(compareLayer2,newRow,context='misc',type='document')
				self.job.steps[self.stepName].copySel(compareLayer2)
				comparisonFailed = comparisonFailed + 2
			self.job.matrix.deleteRow( destTestLayer )
	
		# The third test merges the layers together.  If there are gaps, then there are errors in the 
		# conversion.  This is done by comparing the merged layers with a rectangle filling the profile
		if (comparisonFailed < 8):
			self.statusLabel.config(text='Comparing layers: ' + sourceLayer + ' and ' + destLayer + ' for gaps')
			self.master.lift()
			self.update()
			#create test layer
			self.job.matrix.addLayer(testLayer,newRow,context='misc',type='document')
			#fill test layer with rectangle
			self.job.steps[self.stepName].clearAll()
			self.job.steps[self.stepName].layers[testLayer].display(1)
	              	self.job.steps[self.stepName].layers[testLayer].work()
			self.job.COM('sr_fill,polarity=positive,step_margin_x=0,step_margin_y=0,step_max_dist_x=100,step_max_dist_y=100,sr_margin_x=0,sr_margin_y=0,sr_max_dist_x=0,sr_max_dist_y=0,nest_sr=yes,consider_feat=no,feat_margin=0,consider_drill=no,drill_margin=0,consider_rout=no,dest=affected_layers,layer=gnd2_new,attributes=no')
				
			#Copy merge destination layer with source layer
			self.job.COM('merge_layers,source_layer=' + destLayer + ',dest_layer=' + sourceLayer + ',invert=no')
			self.update()
			#Do graphical compare between test layer and source layer
			STR = 'compare_layers,layer1=' + sourceLayer + ',job2=' + self.jobName + ',step2=' + self.stepName
			STR = STR + ',layer2=' + testLayer + ',layer2_ext=,tol=0.4,area=profile,ignore_attr=,map_layer='
			STR = STR + compareLayer3 + ',map_layer_res=200'
			self.job.COM(STR)
			#See if fails
			result = int(self.job.COMANS)
			if (result > 0):
				#self.job.PAUSE('There were at least ' + str(result) + ' differences between ' + sourceLayer + ' and ' + testLayer + '.  Leaving these layers and compare(' + compareLayer2 + ') layer.')
				comparisonFailed = comparisonFailed + 4
				self.job.matrix.deleteRow(testLayer)
			else:
				self.job.matrix.deleteRow(compareLayer3)
				self.job.matrix.deleteRow(testLayer)
			self.job.matrix.deleteRow( sourceLayer + '+++')
				
		self.statusLabel.config(text='Layer ' + self.workLayer + ' Complete')
		self.update()	
		#If failures, leave old and destination layer, plus cmp layers
		self.job.matrix.deleteRow(destLayer + '+++')
		self.job.matrix.deleteRow(sourceLayer)
		if (comparisonFailed > 0):
			self.job.steps[self.stepName].open(iconic='no')
			self.failedDict[self.workLayer] = 'Compare failed between ' + oldLayer + ' and ' + destLayer + '. Please verify manually.  Use ' + self.workLayer + '_cmp# layers. Status:' + str(comparisonFailed)
			#self.job.PAUSE('Compare failed between ' + oldLayer + ' and ' + destLayer + '. Please verify manually.  Use ' + self.workLayer + '_cmp# layers. Status:' + str(comparisonFailed))
			# 1 - contourization of old failed
			# 2 - Features overlap between positive and negative layer
			# 3 - Features overlap and contourization of old failed
			# 4 - Underlap of features
			# 5 - Underlap and original countourization of old failed
			# 6 - Underlap and overlap
			# 7 - Underlap, overlap, and original contourization failed oooh, nasty!
		#If success, rename destination to original root, delete everything else.
		else:
			self.job.matrix.modifyRow(destLayer,name=self.workLayer)
			self.job.matrix.deleteRow(oldLayer)
		#Exit Section
                
        # Quits (so far)
        def quitAll(self):
                if (self.wasInJob and self.wasInStep):
                	self.job.steps[self.stepName].open(iconic='yes')
                        self.quit()
                elif self.wasInJob:
                        self.job.steps[self.stepName].close()
                        self.quit()
                else:
                        self.job.close(1)
                        self.quit()

                     
        # Run if user clicks the 'Show Checklist Window' Button
	def showResults(self):
                self.job.steps[self.stepName].open(iconic='no')
                self.quit()           

        # Run if no steps found in job.
        def errorEvent(self):
                self.ourListBox.destroy()
                self.scrollList.destroy()
                self.but1.destroy()
                self.jobLabel.config(text='There are no steps in this job!')
                self.job.close(1)
                Button(self,text='EXIT',command=self.quit,bg='blue', fg='white').pack(side=BOTTOM, padx=5, pady=5)
# END SelWin class
        	
        
##  MAIN ROUTINE
#  This is where execution begins.  The gui is run.  It takes care of running everything else.

# GUI is instantiated
root = Tkinter.Tk()

mainFontDesc = Tkinter.Button()['font']
entryFontDesc = Tkinter.Entry()['font']

courierFont = tkFont.Font(family='Courier', size = 16)
largerFont = tkFont.Font(family='Arial',size=14)


plane_convert=Pos_Plane_Conv()

# Configure GUI Name
plane_convert.master.title('Genesis Script Interface')
plane_convert.master.config(bg='darkgreen')

# GUI is run
plane_convert.mainloop()

sys.exit(0)

# We are finished!
