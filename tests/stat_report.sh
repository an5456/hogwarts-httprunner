#!/usr/bin/env bash

killReport()
{
    pid=`ps -ef|grep http.server | grep -E '[0-9] python3'|awk '{print $2}'`
    echo "report server pid :$pid"
    if [[ "$pid" = "" ]]
    then
        echo "no report pid alive"
    else
        kill -9 $pid

        echo "report server pid  kill"

        echo "start report server"

    fi
}
killReport
cd ./html/
echo "start report server"
nohup python3 -m http.server 8899 >out.log 2>&1 &

<<<<<<< HEAD

=======
>>>>>>> 3ecb6f521e3bb8d32709e3ba0408e3786832a899
