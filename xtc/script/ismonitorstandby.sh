#!/bin/bash
# get Standby monitor
# result:
# 0 = on
# 1 = off

FILE=/boot/config.txt
COMMAND="hdmi_blanking"

if (test -s $FILE)
then
  RESULT=$(grep "^$COMMAND" $FILE)

  if [ "$RESULT" == "" ]
  then
    exit 1
  fi
fi

exit 0
