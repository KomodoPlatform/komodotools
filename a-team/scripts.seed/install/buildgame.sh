#!/bin/bash
# GameCredits build script for Debian 9 (c) Decker
# Step 1: Build BDB 4.8
cd ~
git clone https://github.com/gamecredits-project/GameCredits.git
cd GameCredits

GAMECREDITS_ROOT=$(pwd)
GAMECREDITS_PREFIX="${GAMECREDITS_ROOT}/db4"
mkdir -p $GAMECREDITS_PREFIX
wget -N 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz'
echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef db-4.8.30.NC.tar.gz' | sha256sum -c
tar -xzvf db-4.8.30.NC.tar.gz
cd db-4.8.30.NC/build_unix/
../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$GAMECREDITS_PREFIX
​make -j$(nproc)
make install
cd $GAMECREDITS_ROOT

# Step 2: Build OpenSSL (libssl-dev) 1.0.x
version=1.0.2j
mkdir -p openssl_build
wget -qO- http://www.openssl.org/source/openssl-$version.tar.gz | tar xzv
cd openssl-$version
export CFLAGS+="-fPIC"
./config shared --prefix=$GAMECREDITS_ROOT/openssl_build
make -j$(nproc)
make install
cd ..

export PKG_CONFIG_PATH="$GAMECREDITS_ROOT/openssl_build/pkgconfig"
export CXXFLAGS+=" -I$GAMECREDITS_ROOT/openssl_build/include/ -I${GAMECREDITS_PREFIX}/include/"
export LDFLAGS+=" -L$GAMECREDITS_ROOT/openssl_build/lib -L${GAMECREDITS_PREFIX}/lib/"

# Step 3: Build GameCredits daemon
./autogen.sh
./configure --with-gui=no --disable-tests --disable-bench --without-miniupnpc --enable-experimental-asm
make -j$(nproc)


