#!/bin/bash
# $1 = output file
# 
INDEX=0

while [ $INDEX -lt 5 ]
do
  if [ -f $1 ]
  then
    RESULT=$(grep -c "Initialization Sequence Completed" $1)
  
    if [ $RESULT -gt 0 ]
    then
      exit 0
    fi
  fi
  
  INDEX=$(expr $INDEX + 1)
  sleep 2
done

exit 1
