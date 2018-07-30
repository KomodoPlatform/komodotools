cd ~/scripts
BTCDwif=$(sed -n 's|.*"BTCDwif":"\([^"]*\)".*|\1|p' wallet.txt)

assets-cli 'importprivkey' $BTCDwif ' "" false'
