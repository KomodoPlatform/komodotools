#!/bin/bash
#Dependacies without QT, DBD, vim
sudo apt-get install build-essential pkg-config git libc6-dev m4 g++-multilib autoconf libtool ncurses-dev unzip python zlib1g-dev wget bsdmainutils automake libssl-dev libprotobuf-dev protobuf-compiler libqrencode-dev ntp ntpdate software-properties-common curl libcurl4-gnutls-dev cmake clang libevent-dev libboost-all-dev
./buildkomodo.sh
./buildchips.sh
./buildbitcoin.sh
./symlinks.sh
