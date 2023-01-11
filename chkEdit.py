#!/usr/bin/python

#This script contains a function to check when the last edit of a file was, and interpret when it should have last been edited
#This function is intended as a method of ensuring that MTA archive files are being accessed and edited as often as they are supposed to be.

import os
import time
from datetime import timedelta
import re
#---------------------------------------------------
#--chkEdit: alerts if archive file no longer updates
#---------------------------------------------------

#ArchivePeriod file to be stored in mcf package location
locArcPer = os.path.dirname(__file__)
locArcPer = locArcPer + '/archivePeriod'

def chkEdit(archive,notify=[]):
    """
    alerts if archive file no longer updates
    input: archive  --- file path to archive file
           notify   --- list of emails to notify in case of failure
           read from --- 
    output: /tmp/mta/warnArchive-{archiveTail}.out
            mail to mtadude + notify
    """    
    if isinstance(notify,str):
        notify = notify.split()
    elif not isinstance(notify,list):
        raise TypeError("Notify arguement should be list or space-separated string of notifiers")
     
    sendTo = ['william.aaron@cfa.harvard.edu'] + notify 
#    sendTo = ['mtadude@cfa.harvard.edu'] + notify
    warndir = "/tmp/mta"

    if (not os.path.exists(warndir)):
        os.system(f'mkdir {warndir}')
    
    archiveTail = os.path.basename(os.path.normpath(archive))
    warnfile = warndir + f"/warnArchive-{archiveTail}.out"
    
    #Read in targeted Archive File's maximum period before alerting
    data = []
    with open(locArcPer,'r') as f:
        for line in f.readlines():
            if line[0] != "#":
                data.append(line.strip())
        
    
    for ent in data:
        atemp = re.split(':', ent)
        print(atemp)
        fileName = atemp[0].strip()
        per = atemp[1].strip()
        if fileName == archiveTail:
            period = int(per)
            break
    #TODO add error handling for period not being assigned, meaing archive file name doesn't match anything in archivePeriod    

    lastEdit = os.path.getmtime(archive)
    currTime = time.time()
    diff = currTime - lastEdit

    lastEdit = time.localtime(lastEdit)
    currTime = time.localtime(currTime)

    #If it has been too long, record tmp file and send alert.
    if diff > period:
        if (os.path.exists(warnfile)):
            os.system(f'date >> {warnfile}')
        else:
            warnhandle = open(warnfile,"w+")
            warnhandle.write(f'Archive file: {archive} not updating.\n')
            warnhandle.write(f'Last Edit: {time.strftime("%Y-%m-%d %H:%M:%S",lastEdit)}\n')
            warnhandle.write(f'currTime: {time.strftime("%Y-%m-%d %H:%M:%S",currTime)}\n')
            warnhandle.write(f"Diff: {timedelta(seconds = diff)}\n")
            warnhandle.write(f"Max Period: {timedelta(seconds = period)}\n")
            warnhandle.close()
            cmd = f'cat {warnfile} | mailx -s "Archive File: {archiveTail} Not Updating" '
            cmd = cmd + ' '.join(sendTo)
            os.system(cmd)


if __name__ == "__main__":
    chkEdit("/home/waaron/git/mta_comm_func/test.test", 'waaron')
