#!/bin/bash
# get state from argon1 power case
# result:
# 0 = on
# 1 = off

FILE=/tmp/isargon1.txt

rm $FILE 2> /dev/null
systemctl status argononed | grep " active " >> $FILE

if (test -s $FILE)
then
  exit 0
fi

exit 1
