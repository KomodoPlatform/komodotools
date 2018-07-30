#!/bin/bash
cd ~/scripts/
curdir=$(pwd)
curluser=userfb6d081f05e889ac
curlpass=9db93973b9a4e0a222e6d961d8086987
curlport=7771

curl -s --user $curluser:$curlpass --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listunspent", "params": [0, 9999999]}' -H 'content-type: text/plain;' http://127.0.0.1:$curlport/ | jq .result > $curdir/createrawtx.txt
# we will send all spendable and generated coins
transactions=$(cat $curdir/createrawtx.txt | jq '.[] | select (.spendable == true and .generated == true) | del (.generated, .address, .account, .scriptPubKey, .amount, .interest, .confirmations, .spendable)' |  jq -r -s '. | tostring')
balance=$(cat $curdir/createrawtx.txt      | jq '.[] | select (.spendable == true and .generated == true) | .amount' | jq -s add)
balance=$(echo "scale=8; $balance/1*1" | bc -l | sed 's/^\./0./')

# Print Date and Time
echo "----------------------------------------------------------------"
now=$(date +"%Y-%m-%d %T%z")
printf "$now \n";

# Print balance.
echo 'Balance: '$balance

# Balance less than 10 abort, we want maximum rewards.
if (( $(echo "$balance < 10" | bc -l) )); then
  echo "----------------------------------------------------------------"
  echo " "
  exit
fi

# Set the send to address, and send all coinbase transactions
addresses='{"RPx6hcNQkGSE3VLPupnQ45NNYR3NJbkbpk":'$balance'}'
echo "{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"createrawtransaction\", \"params\": [$transactions,$addresses] }" > $curdir/createrawtx.curl

hex=$(curl -s --user $curluser:$curlpass --data-binary "@$curdir/createrawtx.curl" -H 'content-type: text/plain;' http://127.0.0.1:$curlport/ | jq -r .result)
# setting of nLockTime
nlocktime=$(printf "%08x" $(date +%s) | dd conv=swab 2> /dev/null | rev)
hex=${hex::-8}$nlocktime
signed=$(curl -s --user $curluser:$curlpass --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "signrawtransaction", "params": ["'$hex'"]}' -H 'content-type: text/plain;' http://127.0.0.1:$curlport/  | jq -r .result.hex)

#Broadcast the transaction
txid=$(curl -s --user $curluser:$curlpass --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "sendrawtransaction", "params": ["'$signed'"]}' -H 'content-type: text/plain;' http://127.0.0.1:$curlport/ | jq -r .result)
echo $txid
echo "----------------------------------------------------------------"
echo " "
