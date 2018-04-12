#!/bin/bash
#Dependacies without QT, DBD, vim
sudo apt-get install build-essential pkg-config git libc6-dev m4 g++-multilib autoconf libtool ncurses-dev unzip python zlib1g-dev wget bsdmainutils automake libssl-dev libprotobuf-dev protobuf-compiler libqrencode-dev ntp ntpdate software-properties-common curl libcurl4-gnutls-dev cmake clang libevent-dev libboost-all-dev
./buildkomodo.sh
./buildchips.sh
./buildbitcoin.sh
./symlinks.sh

#Create Conf Files
#BTC
cd ~
mkdir .bitcoin
cd .bitcoin
touch bitcoin.conf
echo "rpcuser=user`head -c 32 /dev/urandom | base64`" > bitcoin.conf
echo "rpcpassword=password`head -c 32 /dev/urandom | base64`" >> bitcoin.conf
echo "daemon=1" >> bitcoin.conf
echo "server=1" >> bitcoin.conf
echo "txindex=1" >> bitcoin.conf
echo "bind=127.0.0.1" >> bitcoin.conf
chmod 0600 bitcoin.conf

#Chips
cd ~
mkdir .chips
cd .chips
touch chips.conf
echo "rpcuser=user`head -c 32 /dev/urandom | base64`" > chips.conf
echo "rpcpassword=password`head -c 32 /dev/urandom | base64`" >> chips.conf
echo "daemon=1" >> chips.conf
echo "server=1" >> chips.conf
echo "txindex=1" >> chips.conf
echo "bind=127.0.0.1" >> chips.conf
chmod 0600 chips.conf

#Komodo
cd ~
mkdir .komodo
cd .komodo
touch komodo.conf
echo "rpcuser=user`head -c 32 /dev/urandom | base64`" > komodo.conf
echo "rpcpassword=password`head -c 32 /dev/urandom | base64`" >> komodo.conf
echo "daemon=1" >> komodo.conf
echo "server=1" >> komodo.conf
echo "txindex=1" >> komodo.conf
echo "bind=127.0.0.1" >> komodo.conf
chmod 0600 komodo.conf
