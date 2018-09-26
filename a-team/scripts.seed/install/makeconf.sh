#!/bin/bash
if [ "$1" = "" ]
  then
    echo "no coin specified"
    echo "Enter infomation in the format:"
    echo "./makeconf.sh datadir coinname"
    echo "Example:"
    echo "./makeconf.sh .dashcore dash"
  else
    confpath="$2.conf"
    rpcuser=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1)
    rpcpassword=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1)
    mkdir "/mnt/$2_data"
    ln -s /mnt/$2_data ~/$1
    cd ~/$1
    echo "rpcuser=$rpcuser" > $confpath
    echo "rpcpassword=$rpcpassword" >> $confpath
    echo "server=1" >> $confpath
    echo "deamon=1" >> $confpath
    echo "txindex=1" >> $confpath
fi
