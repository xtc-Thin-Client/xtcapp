#!/bin/bash
pkill timeaction.py

while getopts k opt
do 
  case $opt in
    k) exit 0
       ;;
  esac
done

/opt/thinclient/bin/timeaction.py &
exit 0
