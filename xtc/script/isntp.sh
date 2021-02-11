#!/bin/bash
# check if ntp service active
NTP=$(timedatectl | grep "NTP service:")

if (timedatectl | grep "NTP service: active" > /dev/null)
then
  exit 0
fi
exit 1 
