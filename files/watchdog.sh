#!/bin/bash
# Test if a given CMD_TEST command returns within LIMIT seconds every POOL
# seconds. If it does, executes CMD_OK, otherwise executes CMD_FALSE.

while true; do
    exec $CMD &
    PID=$!

    sleep $LIMIT
    ps -p$PID &>/dev/null
    OUT=$?

    if [ $OUT -eq 0 ]; then
        echo -e $MSG_FAIL
        $CMD_FAIL
    else
        $CMD_OK
    fi
    sleep $POOL
done
