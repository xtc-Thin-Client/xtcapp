#!/usr/bin/python3

import sys
import os
from datetime import datetime, timedelta
import time
import logging
import common

def timeaction(connectionname):
    configfile = common.ressourcefile
    loggingfilename = common.getRessourceByName(configfile, "loggingTimeAction")
    debugfile = common.getRessourceByName(configfile, "debugSwitch")
    debug = False
    if os.path.isfile(debugfile):
        debug = True
    common.loggingStart(loggingfilename, debug)
    logging.info("timeaction")
    
    # get action time from file
    values = common.readTime()
    if "execute" in values:
        logging.info("execute: " + values["execute"])
        if values["execute"] == "no":
            print("no action. Terminated")
            logging.info("no action. Terminated")
            sys.exit(0)
    else:
        sys.exit(0)
    
    actiontime = values["execat"]
    logging.info(actiontime)
    action = values["action"]
    logging.info(action)
    
    if actiontime.startswith("+"):
        splitline = actiontime.split("+")
        text = splitline[1]
        splitline = text.split(":")
        text = splitline[0]
        hours = int(text)
        text = splitline[1]
        minutes = int(text)
        actionat = datetime.now() + timedelta(hours=hours, minutes=minutes)
    else:
        actionat = datetime.strptime(actiontime, "%Y-%m-%d %H:%M")
        
    logging.info("current time: " + str(datetime.now()))
    logging.info("action at " + str(actionat))
    print("current time: " + str(datetime.now()))
    print("action at " + str(actionat))
    print("action: " + action)
    
    run = True
    while run:
        if datetime.now() >= actionat:
            break
        # wait 10 sec. before new check
        time.sleep(10)

    # write last action to file
    values["last"] = str(datetime.now())
    logging.info(values["last"])
    if "repeat" in values:
        logging.info("repeat " + values["repeat"])
        if values["repeat"] == "no":
            values["execute"] = "no"
    else:
        values["execute"] = "no"
    common.writeTime(values)
    logging.info("execute at: " + str(datetime.now()))
    
    # execute action
    if action == "shutdown": 
        common.runProgram(common.getRessource("commandShutdown"))
    if action == "reboot": 
        common.runProgram(common.getRessource("commandreboot"))
    if action == "test":
        print("execute action test")
        logging.info("execute action test")
        sys.exit(0)
    
if __name__ == "__main__":
    timeaction(sys.argv)
