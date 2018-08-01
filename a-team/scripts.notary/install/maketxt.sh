cd ~/scripts
sed -n 's|.*"btcpubkey":"\([^"]*\)".*|pubkey=\1|p' ~/scripts/wallet.txt > pubkey.txt
cp pubkey.txt ~/komodo/src
cp pubkey.txt ~/SuperNET/iguana
cd ~/SuperNET/iguana
echo home/$USER > userhome.txt
