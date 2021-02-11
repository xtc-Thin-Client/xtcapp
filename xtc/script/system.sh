#!/bin/bash
# configure thinclient with paramater file

if [ $# -ne 1 ]
then
 echo "usage: system parameterfile"
 exit 1
fi

/opt/thinclient/bin/system.py $1
