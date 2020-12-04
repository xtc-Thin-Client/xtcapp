#!/bin/bash
# $1 = log file
#
killall openvpn 2> /dev/null
rm $1 2> /dev/null
