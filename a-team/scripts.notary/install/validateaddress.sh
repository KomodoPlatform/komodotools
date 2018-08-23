cd ~/scripts
BTCpub=$(sed -n 's|.*"BTC":"\([^"]*\)".*|\1|p' wallet.txt)
BTCDpub=$(sed -n 's|.*"BTCD":"\([^"]*\)".*|\1|p' wallet.txt)
komodo-cli validateaddress $BTCDpub
sleep 1
chips-cli validateaddress $BTCDpub
sleep 1
bitcoin-cli validateaddress $BTCpub
sleep 1
assets-cli validateaddress $BTCDpub
