#!/usr/bin/env bash

killReport()
{
    # shellcheck disable=SC2006
    pid=`ps -ef|grep http.server | grep -E '[0-9] python3'|awk '{print $2}'`
    echo "report server pid :$pid"
    if [[ "$pid" = "" ]]
    then
        echo "no report pid alive"
    else
        kill -9 $pid
        echo "report server pid  kill"
    fi
}
killReport
# shellcheck disable=SC2164
cd ./html/
echo "start report server"
nohup python3 -m http.server 8899 >out.log 2>&1 &


