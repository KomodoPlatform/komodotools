cd ~
git clone https://github.com/nanomsg/nanomsg
cd nanomsg
mkdir build
cd build
cmake .. -DNN_TESTS=OFF -DNN_ENABLE_DOC=OFF
cmake --build . -j$(nproc)
sudo cmake --build . --target install
sudo ldconfig
