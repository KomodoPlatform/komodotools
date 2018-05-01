# Mined Block Counter

### instruction

0. Precondition : komodo installed and you are KMD miner

1. please install jsoncpp library to parse response of komodod
```
sudo apt-get install libjsoncpp-dev
```

2. how to compile : 
```
$ g++ -o exefileName sourceFile.cpp -ljsoncpp
ex) $ g++ -o nodeMined minedBlock.cpp -ljsoncpp
```

3. how to run
```
$ ./nodeMined
```

