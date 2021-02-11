#!/bin/bash
# get ntp server
grep "^NTP=" /etc/systemd/timesyncd.conf | cut -d= -f2
exit 0
