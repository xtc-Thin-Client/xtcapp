#!/bin/bash
# set sound card
FILE=/data/thinclient/config/soundcard

if [ -s $FILE ]
then
  SOUNDCARD=$(cat $FILE)
  sed "s/^defaults.ctl.card.*$/defaults.ctl.card $SOUNDCARD/" -i /usr/share/alsa/alsa.conf
  sed "s/^defaults.pcm.card.*$/defaults.pcm.card $SOUNDCARD/" -i /usr/share/alsa/alsa.conf
fi

exit 0
