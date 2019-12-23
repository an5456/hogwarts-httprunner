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
<<<<<<< HEAD
        echo "report server pid  kill"
=======
        echo "start report server"
>>>>>>> 8c8f5de50eb2cf91b2de21f62168eb6cc26126fd
    fi
}
killReport
cd ./html/
echo "start report server"
nohup python3 -m http.server 8899 >out.log 2>&1 &
<<<<<<< HEAD
=======
#
#     if pid is not "":
#         subprocess.run("kill -9" + str(pid) + "", shell=True)
#         print("kill report server ")
#     print("start report server")
#     subprocess.run("nohup python3 -m http.server 8899 >out.log 2>&1 & ", shell=True)
>>>>>>> 8c8f5de50eb2cf91b2de21f62168eb6cc26126fd
