#!/bin/bash
# get Multi Monitor
# result:
# 0 = on
# 1 = off

FILE=/boot/config.txt
COMMAND="dtoverlay=vc4-fkms-v3d"

if (test -s $FILE)
then
  RESULT=$(grep "^$COMMAND" $FILE)

  if [ "$RESULT" == "" ]
  then
    exit 1
  fi
else
  exit 1
fi

exit 0
