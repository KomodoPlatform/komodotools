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

using namespace std;

/*
template<template <typename> class P = std::less >
struct sortMapByValue {
    template<class T1, class T2> bool operator()(const std::pair<T1, T2>&left, const std::pair<T1, T2>&right) {
        return P<T2>()(left.second, right.second);
    }
};
*/

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

    map<int, double> my_map; // height, amount
    
    cout << fixed;
    cout.precision(8);
    
    cout << "---------------------------------------------" << endl;
    cout << "num\t" << "Height\t" << "Amount" << endl;
    cout << "---------------------------------------------" << endl;
    
    for (i=0; i< size; i++)
    {
        if (obj["transactions"][i]["generated"].asBool() == false) {
            // cout << "generated : false" << endl;
            continue;
        }

        double amountIn = obj["transactions"][i]["amount"].asDouble();;
        string hash = obj["transactions"][i]["blockhash"].asString();
        int height = getHeight(hash);

        my_map[height] = amountIn;
        
        //cout << j << " - blockHash : " << hash << "\tAmount : " << amountIn << endl;
        //cout << j << "\t" << height << "\t" << amountIn << endl;
            
        total += amountIn;
        j++;
    }

    vector<pair<int, double> > my_vector(my_map.begin(), my_map.end()); // height, amount
    //sort(my_vector.begin(), my_vector.end(), sortMapByValue<less>());    
    
    for (i=0; i < j; i++) {
        cout << i+1 << "\t" << my_vector[i].first << "\t" <<  my_vector[i].second << endl;
    }

    int average = (my_vector[j-2].first - my_vector[0].first) / (j-1);
    int nextTarget = my_vector[j-1].first + average;
    
    cout << "---------------------------------------------" << endl;
    cout << "Total : " << total << " KMD" << endl;
    cout << "Est next block : " << nextTarget << " (avr: +" << average << ")" <<endl;
    cout << "Cur last block : " << lastBlock << " (" << nextTarget - lastBlock << " left)" << endl;
    cout << "---------------------------------------------" << endl;
    return 1;
}
