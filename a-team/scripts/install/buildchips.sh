#Install Chips:
cd ~
git clone https://github.com/jl777/chips3.git -b dev
cd chips3/

#Build Berkly DB 4.8
CHIPS_ROOT=$(pwd)
BDB_PREFIX="${CHIPS_ROOT}/db4"
mkdir -p $BDB_PREFIX
wget 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz'
echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef  db-4.8.30.NC.tar.gz' | sha256sum -c
tar -xzvf db-4.8.30.NC.tar.gz
cd db-4.8.30.NC/build_unix/
../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$BDB_PREFIX
make -j$(nproc)
make install 

#Build Chips
cd ~/chips3
./autogen.sh
./configure LDFLAGS="-L${BDB_PREFIX}/lib/" CPPFLAGS="-I${BDB_PREFIX}/include/" -without-gui -without-miniupnpc
make -j$(nproc)
