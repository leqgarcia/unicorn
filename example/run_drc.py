#!/bin/env python

_header = {
        'author'           :       'Daniel R. Gowans',
        'initialdate'      :       'March 19, 2003',
        'revisiondate'     :       'April 7, 2003',
        'revision'         :       'v0.9',
        'title'            :       'run_drc',
        'description'      :       '''
        This program is used to automate the task of running the initial_drc report
        on a new job.  It uses a GUI interface to select the job and step.  It must be
        run from within Genesis 2000.  After running the analysis it creates a summary
        of the reslts of the analysis.
        
        The job can be run from the database window, in a job, or in a job and step.  It
        will ask for any information it needs.
        '''
        }

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

# processes the results of attribute files from DRC checklist.  
# out_file is an OPEN file pointer, and NOT a filename
def process_results(in_filename, out_file):
		
	# open the input file
	f = open(in_filename)

	# read in the file's lines
	lines = f.readlines()

	#close the file
	f.close()

	#Set up search patterns
	pat_set = re.compile("set ")
	pat_keep = re.compile('min|typ|num_no_bridge|num_sliver|num_stub|num_miss_via|num_miss_pth')
	pat_root = re.compile('^min|^typ|^num')
	pat_under = re.compile('_')
	pat_equal = re.compile(' *= *')
	pat_notavail = re.compile('N/A')
        
	attribs_main = {}
	layer_list = []
	longest_name = 0

	# go through each line and create the necessary structures
	for line in lines:
	    # Search for the pattern(s) set above, and modify
	    # line accordingly
	    s_res = pat_set.search(line)
	    line = line[s_res.end():]   # keeps everything after the set - set discarded
	    s_res = pat_keep.search(line)
            if (s_res):  # this is taken if it is a layer attribute
	        s_res = pat_root.search(line)  # contains min or typ?
	        if  not (s_res):  # This taken if prepended with a layer name
	            s_res = pat_under.search(line)
	            layer_end = s_res.start()
	            layer_name = line[0:layer_end]
	            layer_end = layer_end + 1
	            if not (layer_list.count(layer_name)):
	                layer_list.append(layer_name)
	        else:   # this is taken if it is a summation (total) from layers (No layer name at beginning)
	            layer_name = "Overall"
	            layer_end = 0
	            
	        s_res = pat_equal.search(line)
	        attr_end = s_res.start()
	        value_start = s_res.end()
	        attr_name = line[layer_end:attr_end]
	        if (len(attr_name) > longest_name):
	            longest_name = len(attr_name)
	        attr_val = line[value_start:].rstrip()
	
	        s_res = pat_notavail.search(attr_val)
	        if not (s_res):
	            if not attribs_main.has_key(attr_name):
	                temp = dict()
	                temp[layer_name] = attr_val
	                attribs_main[attr_name] = temp.copy()
	            else:
	                temp = attribs_main[attr_name].copy()
	                temp[layer_name] = attr_val
	                attribs_main[attr_name] = temp.copy()
	    #end of if, matching min and typ
	# end of for

	#Data structure is now populated, and we traverse through it, writing
	#the information in the way that we like.
	    
	out_file.write("\n")
	padding = '    '
	out_file.write(padding + string.ljust("Attribute",longest_name))
	for layer in layer_list:
	    out_file.write(string.rjust(layer,8))
	out_file.write(string.rjust("Overall",8) + '\n')
	layer_list.append("Overall")
	underlines = "------------------"*20
	out_file.write(padding + underlines[0:longest_name + 8*len(layer_list)] + '\n')
	main_keys = attribs_main.keys()
	main_keys.sort()
	for name in main_keys:
	     out_file.write(padding + string.ljust(name,longest_name))
	     temp_dict = attribs_main[name]
	     for layer in layer_list:
	         if (temp_dict.get(layer)):
	             out_file.write(string.rjust(temp_dict[layer], 8))
	         else:
	             out_file.write(string.rjust("N/A", 8))
	     out_file.write("\n")
        longest_name = 0
	

# Gets the results of the analysis and does the file work
def get_results(guiApp):
        filename_out = '/id/workfile/initial_drc/' + guiApp.jobName + '_summary.doc'
	print filename_out

	file_out = open(filename_out,'w')
	file_out.write('\nSummary of checks for job ' + guiApp.jobName + '\n')

	check_list = {'inner':'Inner Layer','outer':'Outer Layer','pwrgnd':'Power/Ground','smask':'Solder Mask'}
	
	for checks in check_list.keys():
		filename_in = guiApp.job.tmpdir + '/init_drc_' + guiApp.jobName + '_' + checks
		print filename_in
	
		file_out.write('\n\nChecks for ' + check_list[checks] + '\n--------------------------\n')
		process_results(filename_in,file_out)

	file_out.write('\nEnd of checks for job ' + guiApp.jobName + '\n\n')
	file_out.close()

	
####################
# Set up running window/GUI Application class
####################

# Create an extention class to Frame
class SelWin(Frame):
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
                self.wasInJob = 0
                self.wasInStep = 0
                Label(self, text='Running Initial DRC checklist',fg='gray80',bg='darkgreen',).pack(side=TOP)
                self.jobLabel = Label(self,text='Please Select a Job',fg='gray80',bg='darkgreen')
                
                # This is a scrollbar object for the job selection list
                self.scrollList = Scrollbar(self,orient=VERTICAL,bg='blue')
                # This is the list box that will hold jobs/steps to select.
		self.ourListBox = Listbox(self, yscrollcommand=self.scrollList.set, bg='black',fg='gray80')
		self.scrollList.config(command=self.ourListBox.yview)
                self.but1 = Button(self, text='Select Job', command=self.getJob, bg='blue', fg='yellow')
                
                # This statement jumps to the correct procedure based on whether in Job/step or not
                if (self.status.currentJob()):  # if in a job...
                        self.jobName = self.status.currentJob()
                        self.wasInJob = 1
                        if (self.status.currentStep()):  # if in a step...
                                self.stepName = self.status.currentStep()
                                self.job = genClasses.Job(self.jobName)
                                self.beforeAnalysis()
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
                self.beforeAnalysis()
 
        # Prepares to run analysis and allows user to initiate
        def beforeAnalysis(self):
                self.ourListBox.destroy()
                self.scrollList.destroy()
                self.jobLabel.config(text='Ready to run on job ' + self.jobName + ' in step ' + self.stepName)
                self.jobLabel.pack(side=TOP, pady=5)
                self.but1.config(text='Run Analysis',command=self.runAnalysis)
                self.but1.pack(side=BOTTOM, padx=10, pady=5)
        
        # Run's the checklist and calls procedure to process results.
        def runAnalysis(self):
                self.job.COM('chklist_create,chklist=initial_drc')
		self.job.COM('chklist_delete,chklist=initial_drc')
		self.job.COM('chklist_from_lib,chklist=initial_drc')
		self.job.COM('chklist_open,chklist=initial_drc')
		self.job.COM('chklist_run,chklist=initial_drc,nact=S,area=profile')
		self.job.COM('chklist_res_exp,chklist=initial_drc,nact=0,source=attributes,dest=file,fname=init_drc_' + self.jobName + '_inner')
		self.job.COM('chklist_res_exp,chklist=initial_drc,nact=1,source=attributes,dest=file,fname=init_drc_' + self.jobName + '_pwrgnd')
		self.job.COM('chklist_res_exp,chklist=initial_drc,nact=2,source=attributes,dest=file,fname=init_drc_' + self.jobName + '_outer')
		self.job.COM('chklist_res_exp,chklist=initial_drc,nact=3,source=attributes,dest=file,fname=init_drc_' + self.jobName + '_smask')
                get_results(self)
                Button(self, text='Exit Script', bg='blue', fg='white', command=self.quitAll).pack(side=BOTTOM, padx=5, pady=5)
                self.jobLabel.config(text='Checklist run, Initial drc analysis complete')
                Label(self,font=courierFont,text='Results are in: /id/workfile/initial_drc/' + self.jobName + '_summary.doc',fg='orange',bg='darkgreen').pack(side=TOP,padx=5,pady=10)
                self.but1.config(text='Show Checklist Window',command=self.showResults)
                self.but1.pack(side=BOTTOM, padx=5, pady=5)
                
        # Quits (so far)
        def quitAll(self):
                if (self.wasInJob and self.wasInStep):
                	self.job.steps[self.stepName].open(iconic='no')
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
     		self.job.COM('chklist_show,chklist=initial_drc')
                #self.job.COM('info,args=-t check -e daniel3/pcb/initial_drc -d ERF -o action=2,out_file=/tmp/thus2')
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

#root.option_add("*Font", mainFont)
#root.option_add("*Entry*Font",entryFont)
#root.option_add("*Text*Font",entryFont)

selectionWindow=SelWin()

# Configure GUI Name
selectionWindow.master.title('Genesis Script Interface')
selectionWindow.master.config(bg='darkgreen')

# GUI is run
selectionWindow.mainloop()

sys.exit(0)

# We are finished!

