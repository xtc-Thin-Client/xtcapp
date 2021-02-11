#!/bin/bash
# get resolution
xrandr --current | grep "*" | awk '{print $1}'
exit 0
