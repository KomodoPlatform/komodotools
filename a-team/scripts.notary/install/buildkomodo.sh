#Install Komodo
cd ~
git clone https://github.com/jl777/komodo
cd komodo
git checkout mergemaster
./zcutil/fetch-params.sh
./zcutil/build.sh -j$(nproc)
