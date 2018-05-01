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

using namespace std;

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

int main() {

    Json::Reader reader;
    Json::Value obj;

	cout << "Loading blockchain info...please wait..." << endl;
	
    string jsonOutput = myExec("~/komodo/src/komodo-cli listsinceblock 01d2c8f63c0c4b0da415a928a94f05b8c1a6070d092e3800ab8bbb37f36b842d"); // since block 814000
    reader.parse(jsonOutput, obj); // Reader can also read strings

    int size = obj["transactions"].size();
    int i=0, j=1;

    double total = 0;

    cout << fixed;
    cout.precision(8);

    for (i=0; i< size; i++)
    {
        if (obj["transactions"][i]["generated"].asBool() == false) {
            // cout << "generated : false" << endl;
            continue;
        }

        double amountIn = obj["transactions"][i]["amount"].asDouble();;
        string hash = obj["transactions"][i]["blockhash"].asString();

        cout << j << " - blockHash : " << hash << "\tAmount : " << amountIn << endl;
            
        total += amountIn;
		j++;
    }

    cout << "Total : " << total << endl;
    return 1;
}
