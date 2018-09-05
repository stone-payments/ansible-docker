#!/bin/bash

# Test if a given CMD_TEST command returns within CMD_TEST_MAX_DURATION seconds.
# If it does, executes CMD_OK, otherwise executes CMD_FALSE.

# This workaround script was created to automatically recover from a series
# of know bugs on docker in which it frezzes. An example: https://github.com/moby/moby/issues/13885

# Please note that this script cannot see the diference from docker being slow and docker hanging. 
# Keep that in mind if your docker daemon operates under heavy load.
# Another problem that can cause problems is the daemon taking a lot of time to restart.

while true; do
    exec $CMD_TEST &
    PID=$!

    sleep $CMD_TEST_MAX_DURATION
    ps -p$PID &>/dev/null
    OUT=$?

    if [ $OUT -eq 0 ]; then
        echo -e $MSG_FAIL
        $CMD_FAIL
    else
        $CMD_OK
    fi
done
