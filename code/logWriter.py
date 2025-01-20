import pandas as pd
from datetime import datetime
import os

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y %H")
logPath = 'LogData/ErrorlogDB'+dt_string+'.log'
logData = 'LogData/StaggingLogDB'+dt_string+'.log'
# Create the log writer
def createIni():
    if not os.path.isfile(logPath):
        f = open(logPath,"x")
        logRecord('Batch code initiated.')
    if not os.path.isfile(logPath):
        f = open(logData,"x")
        logRecord('Batch code initiated.')
    
# Add records to the log wirter    
def logRecord(strs):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y %H:%M:%S")
    f = open(logPath, "a")
    writeData = dt_string+' ---> '+str(strs)+'\n'
    f.write(writeData)
    f.close()

def logBackUpRecord(strs):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y %H:%M:%S")
    f = open(logData, "a")
    writeData = dt_string+' ---> '+str(strs)+'\n'
    f.write(writeData)
    f.close()