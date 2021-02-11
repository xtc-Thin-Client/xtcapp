#!/bin/bash
# get monitor name
# $1 = Monitor number
#
xrandr -q | grep "connect" | cut -d" " -f1 | awk -v LINE=$1 'NR==LINE' 
#xrandr --listmonitors | awk '{print $4}' | awk '!/^$/' | awk -v LINE=$1 'NR==LINE'
