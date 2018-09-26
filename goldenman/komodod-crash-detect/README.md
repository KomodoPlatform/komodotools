# komodo daemon crash detect and re-run automatically

### 1. creat shell script in home dir
```
$ vim check_komodo.sh
```
```
#!/bin/bash

dt=$(date '+%Y/%m/%d_%H:%M:%S');
psresult=$(ps aux | grep -c "komodod -gen");
#echo "$dt-$psresult"

if [ $psresult -eq 2 ]
then
echo "$dt - result = $psresult - Okay"
else
echo "$dt - result = $psresult - NG"
~/start &
echo "$dt - re-run komodo daemon"
fi
```
This shell will check komodod process is on process list and if not exist, call `~/start` to re-run daemon.


### 2. add this script on `crontab`
```
$ crontab -e
```
And add below at the end of editor
```
# m h  dom mon dow   command
*/5 * * * * ~/check_komodo.sh  >> ~/check_komodo.log 2>&1
```
This will run shell every 5 minute. You can edit interval to check daemon crash.


