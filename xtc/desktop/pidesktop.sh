#!/bin/bash
# get pi hardware 
MODEL=$(cat /proc/cpuinfo |grep "Revision" | cut -d: -f2 | sed 's/^[ \t]*//')
# if Raspberry Pi 3 start driver for pi desktop
if [ "$MODEL" = "a22082" ] || [ "$MODEL" = "a220a0" ] || [ "$MODEL" = "a32082" ] || [ "$MODEL" = "a52082" ] || [ "$MODEL" = "a22083" ] || [ "$MODEL" = "a02100" ] || [ "$MODEL" = "a020d3" ] || [ "$MODEL" = "a2082" ] || [ "$MODEL" = "a20a0" ]
  then
    /usr/bin/python -u /usr/share/pidesktop/python/$1
fi
