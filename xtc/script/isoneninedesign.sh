#!/bin/bash
# get state from oneninedesign power case
# result:
# 0 = on
# 1 = off

FILE=/boot/config.txt
COMMAND="dtoverlay=gpio-poweroff"

if (test -s $FILE)
then
  RESULT=$(grep "^$COMMAND" $FILE)

  if [ "$RESULT" != "" ]
  then
    exit 0
  fi
fi

exit 1
