Implement builder and reader classs for packet used in Telepathy API.
 
## Start on boot

A script added to /etc/init.d named "rr".

To make it executable and run on boot.
```
sudo chmod 755 /etc/init.d/rr
sudo update-rc.d rr defaults
```

#### Script
```
#! /bin/sh
# /home/pi/TelepathyAPI-Robot/startserver.py

### BEGIN INIT INFO
# Provides:          rr
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       
# From www.stuffaboutcode.com which will start / stop a program a boot / shutdown.
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting RollingStone Server"
    # run application you want to start
    screen -d -m -S "rr-server" python3 /home/pi/TelepathyAPI-Robot/startserver.py 
    ;;
  stop)
    echo "Stopping RollingStone Server"
    # kill application you want to stop
    screen -X -S rr-server quit
    ;;
  *)
    echo "Usage: /etc/init.d/rr {start|stop}"
    exit 1
    ;;
esac

exit 0
```
