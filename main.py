from io import StringIO
import amc_interview_validator as am
import os
from os.path import exists
import json
import string
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Log:
    id: string = ''
    email: string = ''
    message: string = ''

def getEmailList(logFilePath):
     with open(logFilePath, "r") as jsonFile:
        return json.load(jsonFile)

def writeEmailListToLogFile(logFilePath, emailList):
    with open(logFilePath, "w") as logFile:
        json.dump(emailList, logFile)

def addEmailToTally(email, logFilePath):
    if not exists(logFilePath):
        file = Path(logFilePath)
        file.touch(exist_ok=True)
        with open(logFilePath, "a") as logFile:
            logFile.write("{}")
    else:
        emailList = getEmailList(logFilePath)
        if email not in emailList:
            emailList[email] = 0
        else:
            emailList[email] = emailList[email] + 1
            
        writeEmailListToLogFile(logFilePath, emailList)

def processEmail(email, logFileId):
    if am.is_email(email):
        # Log speicific tally
        logFilePath = f'.\Output\{logFileId}.json'
        addEmailToTally(email, logFilePath)
        # Global tally
        logFilePath = f'.\Output\output.json'
        addEmailToTally(email, logFilePath)

def processLogFile(filePath):
    f = open(filePath)
    data = json.load(f)
    logFileId = data['id']
    for i in data['logs']:
        log = json.loads(json.dumps(i), object_hook=lambda d: Log(**d))
        processEmail(log.email, logFileId)
    f.close()

for dirpath, dirnames, files in os.walk('.'):
    if dirpath == '.\logs\logs':
        for file_name in files:
            print(f'Processing {file_name}...')
            #function to process log file
            processLogFile(f'{dirpath}\{file_name}')

