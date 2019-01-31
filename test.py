#!/bin/env python

import sys

print "XaaS Scripting"

'''
COM check_inout,mode=out,type=job,job=22172apct
COM clipb_open_job,job=22172apct,update_clipboard=view_job
COM open_job,job=22172apct
'''


cmd = '@%#%@'+ 'COM check_inout,mode=out,type=job,job=22172apct' + '\n'
sys.stdout.write(cmd)
sys.stdout.flush()



cmd = '@%#%@'+ 'COM clipb_open_job,job=22172apct,update_clipboard=view_job' + '\n'
sys.stdout.write(cmd)
sys.stdout.flush()

exit(0)

cmd = '@%#%@'+ 'COM check_inout,mode=out,type=job,job=22172apct' + '\n'
sys.stdout.write(cmd)
sys.stdout.flush()


