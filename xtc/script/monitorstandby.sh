#!/bin/bash
# Standby monitor on/off
# $1 = on, off

FILE=/boot/config.txt
COMMAND="hdmi_blanking"
RESULT=$(grep "$COMMAND" $FILE)

if (test -s $FILE)
then
  if [ "$1" = "on" ]
  then
    if [ "$RESULT" == "" ]
    then      
      echo $COMMAND"=1" >> $FILE
    fi
  fi

  if [ "$1" = "off" ]
  then
    if [ "$RESULT" != "" ]
    then
      sed -i "/$COMMAND/d" $FILE    
    fi
  fi
fi

exit 0
