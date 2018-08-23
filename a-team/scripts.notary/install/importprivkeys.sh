cd ~/scripts
BTCwif=$(sed -n 's|.*"BTCwif":"\([^"]*\)".*|\1|p' wallet.txt)
BTCDwif=$(sed -n 's|.*"BTCDwif":"\([^"]*\)".*|\1|p' wallet.txt)
komodo-cli importprivkey $BTCDwif "" false
bitcoin-cli importprivkey $BTCwif "" false
chips-cli importprivkey $BTCDwif "" false
assets-cli 'importprivkey' $BTCDwif ' "" false'
