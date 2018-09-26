/****
 * Please read READMD.md
 *
 * install lib : $ sudo apt-get install libjsoncpp-dev
 * 
 * how to compile : 
 * $ g++ -o exefileName sourceFile.cpp -ljsoncpp
 * ex) $ g++ -o nodeMined minedBlockCounter.cpp -ljsoncpp
 * 
 * how to run
 * $ ./nodeMined
 */

#include <iostream>
#include <fstream>
#include <jsoncpp/json/json.h>
#include <vector>
#include <stdio.h>      /* printf */
#include <stdlib.h> 
#include <unistd.h>
//#include <conio.h>
#include <vector>
#include <map>
#include <algorithm>
#include <time.h>

using namespace std;

/*
template<template <typename> class P = std::less >
struct sortMapByValue {
    template<class T1, class T2> bool operator()(const std::pair<T1, T2>&left, const std::pair<T1, T2>&right) {
        return P<T2>()(left.second, right.second);
    }
};
*/

struct Block
{
    int height;
    int blockTime;
    double amount;
};

string myExec(const char* cmd) {
    char buffer[512];
    std::string result = "";
    FILE* pipe = popen(cmd, "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (!feof(pipe)) {
            if (fgets(buffer, 128, pipe) != NULL)
                result += buffer;
        }
    } catch (...) {
        pclose(pipe);
        throw;
    }
    pclose(pipe);
    return result;
}

int getHeight(string hash) {
    int height = 0;
    
    string cmd = "~/komodo/src/komodo-cli getblock " + hash;
    string jsonOutput = myExec(cmd.c_str());
    
    Json::Reader reader;
    Json::Value obj;
    reader.parse(jsonOutput, obj); // Reader can also read strings
    
    height = obj["height"].asInt();
    return height;
}

string getTimeStr(int timestamp) {
    time_t rawtime = timestamp;
    struct tm * timeinfo;
    char buffer [80];

    //time (&rawtime);
    timeinfo = localtime (&rawtime);

    strftime (buffer,80,"%F %R",timeinfo);
   
    return buffer;
}

int main() {

    Json::Reader reader;
    Json::Value obj;

    cout << "Loading blockchain info...please wait..." << endl;
    
    string jsonOutput = myExec("~/komodo/src/komodo-cli listsinceblock 01d2c8f63c0c4b0da415a928a94f05b8c1a6070d092e3800ab8bbb37f36b842d"); // since block 814000
    reader.parse(jsonOutput, obj); // Reader can also read strings

    int size = obj["transactions"].size();
    int i=0, j=0;

    double total = 0;
    int lastBlock = getHeight(obj["lastblock"].asString());

    map<int, Block> my_map; // height, amount
    
    cout << fixed;
    cout.precision(8);
    
    cout << "--------------------------------------------------------" << endl;
    cout << "num\t" << "Amount\t\t" << "Height" << "\t\tTime Interval(M)" << endl;
    cout << "--------------------------------------------------------" << endl;
    
    for (i=0; i< size; i++)
    {
        if (obj["transactions"][i]["generated"].asBool() == false) {
            // cout << "generated : false" << endl;
            continue;
        }

        double amountIn = obj["transactions"][i]["amount"].asDouble();;
        string hash = obj["transactions"][i]["blockhash"].asString();
        int time = obj["transactions"][i]["blocktime"].asInt();
        
        int height = getHeight(hash);
        
        Block blockinfo;
        blockinfo.height = height;
        blockinfo.amount = amountIn;
        blockinfo.blockTime = time;

        my_map[height] = blockinfo;
        
        total += amountIn;
        j++;
    }

    vector<pair<int, Block> > my_vector(my_map.begin(), my_map.end()); // height, amount
    //sort(my_vector.begin(), my_vector.end(), sortMapByValue<less>());    
    
    int sumTime = 0;
    
    for (i=0; i < j; i++) {
        Block block = my_vector[i].second;
        double amount = block.amount;
        
        if (i > 0) {
            int sub = my_vector[i].first - my_vector[i-1].first;
            Block prevBlock = my_vector[i-1].second;
            int timesub = (block.blockTime - prevBlock.blockTime) / 60;
            sumTime += timesub;
            //string time = getTimeStr(timesub);
            cout << i+1 << "\t" << amount << "\t" <<  my_vector[i].first << " (+" << sub << ")\t" << timesub << endl;

        } else {
            cout << i+1 << "\t" << amount << "\t" <<  my_vector[i].first << "\t-----" << endl;
        }
    }

    int average = (my_vector[j-2].first - my_vector[0].first) / (j-1);
    int nextTarget = my_vector[j-1].first + average;
    
    int now = time(NULL);
    Block lastblock = my_vector[j-1].second;
    int last = lastblock.blockTime;
    double minedPerHour = total / sumTime * 60;
    
    cout << "--------------------------------------------------------" << endl;
    cout << "Total : " << total << " KMD" << " (avrg interval : " << average << ")" << endl;
    cout << "--------------------------------------------------------" << endl;
    cout << "Cur last block : " << lastBlock <<  endl;
    cout << "Est next block : " << nextTarget << " (" << nextTarget - lastBlock << " left)" << endl;
    cout << "--------------------------------------------------------" << endl;
    cout << "Time mined : " << getTimeStr(last) <<  " (-" << (now-last)/60 << " mins)" << endl;
    cout << "Time curr  : " << getTimeStr(now) << endl;
    cout << "--------------------------------------------------------" << endl;
    cout << "Mined per Hour : " << minedPerHour << " KMD" << endl;
    cout << "Mined per Day  : " << minedPerHour * 24 << " KMD" << endl;
    cout << "--------------------------------------------------------" << endl;
    
    return 1;
}

