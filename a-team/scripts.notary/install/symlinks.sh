cd ~
#Link Bitcoin Exec's.
sudo ln -sf /home/$USER/bitcoin/src/bitcoin-cli /usr/local/bin/bitcoin-cli
sudo ln -sf /home/$USER/bitcoin/src/bitcoind /usr/local/bin/bitcoind

#Link Komodo Exec's.
sudo ln -sf /home/$USER/komodo/src/komodo-cli /usr/local/bin/komodo-cli
sudo ln -sf /home/$USER/komodo/src/komodod /usr/local/bin/komodod

#Link Chips Exec's
sudo ln -sf /home/$USER/chips3/src/chips-cli /usr/local/bin/chips-cli
sudo ln -sf /home/$USER/chips3/src/chipsd /usr/local/bin/chipsd

#Link GameCredits
sudo ln -sf /home/$USER/GameCredits/src/gamecredits-cli /usr/local/bin/gamecredits-cli
sudo ln -sf /home/$USER/GameCredits/src/gamecredits-cli /usr/local/bin/gc-cli
sudo ln -sf /home/$USER/GameCredits/src/gamecreditsd /usr/local/bin/gamecreditsd

#Link scripts
sudo ln -sf /home/$USER/scripts/acsplit /usr/local/bin/acsplit
sudo ln -sf /home/$USER/scripts/assets-cli /usr/local/bin/assets-cli
sudo ln -sf /home/$USER/scripts/asset-cli /usr/local/bin/asset-cli

