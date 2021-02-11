#!/bin/bash
# get time zone
TIMEZONE=$(timedatectl | grep "Time zone:" | cut -d: -f2 | cut -d"(" -f1)
echo $TIMEZONE
exit 0
