curl --url "http://127.0.0.1:7776" --data "{\"poll\":100,\"active\":1,\"agent\":\"iguana\",\"method\":\"addcoin\",\"newcoin\":\"BTCD\",\"startpend\":1,\"endpend\":1,\"services\":128,\"maxpeers\":16,\"RELAY\":0,\"VALIDATE\":0,\"portp2p\":14631,\"rpc\":14632}"
curl --url "http://127.0.0.1:7776" --data "{\"prefetchlag\":5,\"poll\":100,\"active\":1,\"agent\":\"iguana\",\"method\":\"addcoin\",\"newcoin\":\"BTC\",\"startpend\":1,\"endpend\":1,\"services\":128,\"maxpeers\":16,\"RELAY\":0,\"VALIDATE\":0,\"portp2p\":8333}"
cd ~/SuperNET/iguana
cp ~/scripts/install/wp_7776 .
source ~/SuperNET/iguana/passphrase.txt
curl --url "http://127.0.0.1:7776" --data "{\"agent\":\"bitcoinrpc\",\"method\":\"encryptwallet\",\"passphrase\":\"$passphrase\"}" > ~/scripts/wallet.txt
./wp_7776
sleep 5
pkill -15 iguana
