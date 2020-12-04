#!/bin/bash
# screensaver on/off
# $1 = on = switch screensaver on, off = switch screensaver off

FILE=/var/thinclient/home/thinclient/.config/openbox/autostart
COMMAND="xset -dpms"
RESULT=$(grep "$COMMAND" $FILE)

if [ "$1" = "off" ]
then
  if [ "$RESULT" = "" ]
  then
    echo $COMMAND "s off" >> $FILE
  fi
fi

if [ "$1" = "on" ]
then
  if [ "$RESULT" != "" ]
  then
    sed -i "/$COMMAND/d" $FILE    
  fi
fi

exit 0
