#!/bin/bash
# get screensaver
# result:
# 0 = screensaver on
# 1 = screensaver off

FILE=/var/thinclient/home/thinclient/.config/openbox/autostart
COMMAND="xset -dpms"

RESULT=$(grep "$COMMAND" $FILE)

if [ "$RESULT" == "" ]
then
  exit 0
fi

exit 1
    
