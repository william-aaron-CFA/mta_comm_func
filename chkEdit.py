#!/usr/bin/python

#This script contains a function to check when the last edit of a file was, and interpret when it should have last been edited
#This function is intended as a method of ensuring that MTA archive files are being accessed and edited as often as they are supposed to be.

import os
import time
from datetime import timedelta

#---------------------------------------------------
#--chkEdit: alerts if archive file no longer updates
#---------------------------------------------------

def chkEdit(archive,notify=[]):
    """
    alerts if archive file no longer updates
    input: archive  --- file path to archive file
           notify   --- list of emails to notify in case of failure
           read from --- 
    output: /tmp/mta/warnArchive-{archiveTail}.out
            mail to mtadude + notify
    """    
 

    warndir = "/tmp/mta"

    if (not os.path.exists(warndir)):
        os.system(f'mkdir {warndir}')
    
    archiveTail = os.path.basename(os.path.normpath(archive))
    warnfile = warndir + f"/warnArchive-{archiveTail}.out"



    lastEdit = os.path.getmtime(archive)
    currTime = time.time()
    diff = currTime - lastEdit

    lastEdit = time.localtime(lastEdit)
    currTime = time.localtime(currTime)

    period = 60

    if diff > period:
        period = period + 100000000
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
            os.system(f'cat {warnfile} | mailx -s "Archive File: {archiveTail} Not Updating" waaron')


if __name__ == "__main__":
    chkEdit("/home/waaron/git/mta_comm_func/test.test")
