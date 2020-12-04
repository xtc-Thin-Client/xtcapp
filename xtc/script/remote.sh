if (test -e /data/thinclient/remoteon)
then
    /usr/bin/x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /data/thinclient/remote.pass -rfbport 5900 -shared
fi
