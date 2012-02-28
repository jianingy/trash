#!/bin/bash

root=$(dirname $0)
source $root/settings.sh

start() {
	$root/emu-daemon --daemon --server $server --cache $cache --tools $tools \
		--log-level $loglevel --log $log --listen $listen --pid $pidfile && echo `hostname`: emu-daemon started.
}

stop() {
    if [ ! -r "$pidfile" ]; then
		echo >&2 "ERROR: PID file '$pid' not found"
        exit 1
	fi

    pid=$(cat $pidfile)
    
	if [ ! -d "/proc/$pid" ]; then
		echo >&2 "ERROR: Process (PID=$pid) does not exist"
		exit 2
    fi

	prog=$(cat /proc/$pid/cmdline | cut -d '' -f 2)
	
	if [ "x$root/emu-daemon" != "x$prog" ]; then
		echo >&2 "ERROR: Process (PID=$pid) is not a instance of emu-daemon"
		exit 3
	fi
	
	kill $pid
	sleep 2
	[ -r /proc/$pid/cmdline ] && kill -9 $pid
	sleep 2

	if [ -r /proc/$pid/cmdline ]; then
		echo >&2 "ERROR: Process (PID=$pid) is still there"
		exit 3
	fi

	echo `hostname`: emu-daemon stopped.
	exit 0
}

action=$1

if [ -z "$action" ];  then
	echo "Usage: $0 {start|stop|restart}"
	exit 0
fi

case "$action" in
	start) start ;;
	stop) stop ;;
	restart) stop;sleep 1;start ;;
esac

