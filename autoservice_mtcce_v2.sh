#!/bin/bash
echo "Hello World"

# Loop forever (until break is issued)
while true; do

Year=`date +%Y`
Month=`date +%m`
Day=`date +%d`
Hour=`date +%H`
Minute=`date +%M`
Second=`date +%S`
echo `date`
echo "Current Date is: $Day-$Month-$Year"
echo "Current Time is: $Hour:$Minute:$Second"
echo "Local Time is: [$Year-$Month-$Day $Hour:$Minute:$Second]"

echo "MT CCE starting in 5s"


#sleep
echo "Wait for 5 seconds to Kill processes"
sleep 5
echo "Completed"


#ps aux  |  grep -i csp_build  |  awk '{print $2}'  |  xargs sudo kill -9
ps aux  |  grep -i c1pyprox.py  |  awk '{print $2}'  |  xargs kill -2
sleep 0.3
ps aux  |  grep -i c1pyprox.py  |  awk '{print $2}'  |  xargs kill -9

echo "Wait for 10 seconds to start /xxxxxx.sh"
sleep 10
echo "Completed" 

#nohup ./run_cce_.sh &

# with local MQTT
#python3  c1pyprox.py -I 0.0.0.0  -v -t -M 127.0.0.1 -o canon 40065 192.168.1.1 30240

# standard
#python3  c1pyprox.py -I 0.0.0.0  -v -t -o canon 40065 192.168.1.1 30240

## nohup ./run_mtcce_.sh >> "./logfile.$(date +'%Y-%m-%d').log"   &

nohup python3  ./c1pyprox.py -I 0.0.0.0  -v -t -o canon 40065 192.168.1.1 30240  >> "./logfile.$(date +'%Y-%m-%d').log"   &


echo "Wait for  12 mins to loop"
sleep  720
echo "Completed"


done


