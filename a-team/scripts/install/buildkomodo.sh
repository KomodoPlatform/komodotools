#Install Komodo
cd ~
git clone https://github.com/jl777/komodo
cd komodo
git checkout beta
./zcutil/fetch-params.sh
./zcutil/build.sh -j$(nproc)
