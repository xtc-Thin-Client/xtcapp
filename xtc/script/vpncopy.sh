#!/bin/bash
# $1 = source filename
# $2 = target filename
#
TARGET=$2

if [ "$TARGET" = "" ]
then
  TARGET=/data/vpn
fi

cp $1 $TARGET

