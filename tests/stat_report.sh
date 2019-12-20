#!/usr/bin/env bash

killReport()
{
    pid=`ps -ef|grep http.server | grep -E '[0-9] python3'|awk '{print $2}'`
    echo "report Id :$pid"
    if [[ "$pid" = "" ]]
    then
        echo "no report pid alive"
    else
        kill -9 $pid
    fi
}
killReport
cd ./html/
nohup python3 -m http.server 8899 >out.log 2>&1 &
#
#     if pid is not "":
#         subprocess.run("kill -9" + str(pid) + "", shell=True)
#         print("kill report server ")
#     print("start report server")
#     subprocess.run("nohup python3 -m http.server 8899 >out.log 2>&1 & ", shell=True)