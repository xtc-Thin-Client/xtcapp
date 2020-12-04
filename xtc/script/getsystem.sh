#!/bin/bash
# get system
# result:
# U = Ubuntu
# PI3 = Raspberry Pi 3
# PI4 = Raspberry Pi 4

RESULT="U"
if (cat /etc/issue | grep -i "RASPBIAN" > /dev/null)
then
  RESULT="R"
fi

# detect pi hardware 
if [ $RESULT = "R" ]
then
  MODEL=$(cat /proc/cpuinfo |grep "Revision" | cut -d: -f2 | sed 's/^[ \t]*//')
  if [ "$MODEL" = "a22082" ] || [ "$MODEL" = "a220a0" ] || [ "$MODEL" = "a32082" ] || [ "$MODEL" = "a52082" ] || [ "$MODEL" = "a22083" ] || [ "$MODEL" = "a02100" ] || [ "$MODEL" = "a020d3" ] || [ "$MODEL" = "a2082" ] || [ "$MODEL" = "a20a0" ]
  then
    RESULT="PI3"
  else
    RESULT="PI4"
  fi
fi

echo $RESULT
