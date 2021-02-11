#!/bin/bash
RESULT=$(grep "^defaults.ctl.card" /usr/share/alsa/alsa.conf | cut -d" " -f2)
SOUNDCARD=${RESULT##*( )}
echo $SOUNDCARD
exit 0
