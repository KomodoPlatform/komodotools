# Install Instructions:

 - Install [Debian9](https://www.debian.org/distrib/netinst), with only the SSH server and "system utilities" 
 - Create your user in the install
 - On reboot login as your user, then:
 - ` export EDITOR=nano #skip if you can use vi `
 - `visudo`
 - Add your user to the Allow members of group etc line, replace $USER with your user name.
` $USER ALL=(ALL:ALL) ALL `
Save and Exit
Close SSH Session

On your local machine, assuming you have [created an SSH key pair](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server):
> ` ssh-copy-id $USER@"ip address of your node" `

Answer yes then type the current user's password.

#### SSH to your node: 
>` ssh $USER@IPADDRESS`

If it logs in without a password prompt, your key pair is installed and we can go ahead and disable password login (this disables root login by default because root has no key pair) and change the default SSH port. For our production Node, the SSH port will also be changed to a completely separate public internet IP address for security. You should do the same.
> `sudo nano /etc/ssh/sshd_config`

Scroll down to 
>` #Port 22` 

Remove the '#' and change the port, scroll down to
>`#PasswordAuthentication yes `

Remove the '#' and change 'yes' to 'no'

Save and Exit, then run the following commands to restart ssh server.
>` sudo systemctl stop sshd`
>`sudo systemctl start sshd`
>` logout `

#### Upload the scripts folder
Open a local terminal in the folder where the scripts.tar is located
>`sftp -P "ssh port" $USER@IPADDRESS`
> `put scripts.tar`
> `exit`

Login and extract the scripts so we can go ahead and install everything.
> ` ssh -p "ssh port" $USER@IPADDRESS`
> `tar -xvf scripts.tar`

#### Run the install script
>`cd ~/scripts/install`
>`./install.sh`

Enter your users password and answer `Y` to install the dependencies.
> Wait...... Be ready to enter user password again at sudo prompts at the end of the compilation. This will add sym-links for us for commands like: 
> >komodo-cli
> chips-cli
> bitcoin-cli
> assets-cli 
> acsplit

#### Sync all chains up to date.
> `cd ~/scripts`
`./start.first`
Wait a few min's... Start next one in new ssh session
`./sync_assets`

While this is running we can install nanomsg and iguana in another ssh session:
>`cd ~/scripts/install`
`./installnanomsg.sh`
`./installsupernet.sh`

Stop all chains after they have synced, you cannot proceed further until all chains are synced, this is important.
>`cd ~/scripts`
`./stop`

## Create the Wallet  for your node.
In one SSH session run the following commands
>`cd ~/SuperNET/iguana`
`./m_LP`
`../agents/iguana elected`

##### Open a new SSH session for the following section.
The `genwallet.sh` script will create a random passphrase into ~/SuperNET/iguana/passphrase.txt, **if you have a passphrase already skip this step**.
>`cd ~/scripts/install`
`./genwallet.sh`

If you have a passphrase already create passphrase.txt with it.
>`cd ~/scripts/install`
`echo passphrase="your passphrase in quotes" > ~/SuperNET/iguana/passphrase.txt`

Generate the wallet.txt file
>`./genwallet2.sh`

Create pubkey and userhome txt files
>`./maketxt.sh`

Apply Cipi's network tweaks and increase open file limit
>`./applytweaks.sh`

Restart the OS to apply the tweaks and close all SSH sessions.
>`sudo reboot`

### SSH back into your node
At this point I like to use tmux as per advice of ns408. 
>`sudo apt-get install tmux`
`tmux`

Split your screen into 4 terminals at least.
>`ctrl + b then press "`
`ctrl + b then press %`
`ctrl + b then press "up arrow key"`
`ctrl + b then press %`

If you lose SSH session or want to logout and resume session later, you can use: `tmux attach `after you ssh back in to resume this screen. My actual tmux setup has the top right screen split into 3. But set it up however you like.  Here are some links I found helpful:
>> [A Gentle Introduction to tmux – Hacker Noon](https://hackernoon.com/a-gentle-introduction-to-tmux-8d784c404340)
>[Read The Tao of tmux | Leanpub](https://leanpub.com/the-tao-of-tmux/read)

Now we need to start all the coins and import our private keys. All the blockchains should be synced so this should not take long, provided your wallets are empty. 

If you are importing a used passphrase and it has a balance, you need to either restore wallet.dat files here or importprivkey and then restart with a rescan.
>`./start.first `

Wait until komodod has finished loading blocks. On my node this takes about 5mins. Do this in another tmux terminal.
>`./sync_assets`

Wait until assetchains are all synced up. Could take about 15mins.

#### Now ready to start importing private keys
>`cd ~/scripts/install`
`./importprivkeys.sh`

Check the keys were validated, look for ismine: true. There is a 1s delay between each coin to make it easy to read.
>`./validateaddress.sh`

If everything went well you can now stop the node and we can get it running.
>`cd ~/scripts`
`./stop`

If your passphrase is new and there have never been any funds sent to them. You can now start the node! Skip this  step. 
**ONLY PREFORM THIS STEP IF YOU ALREADY HAVE FUNDS IN YOUR NODE WALLET IT WILL TAKE A LONG TIME**
>`cd ~/scripts`
`./rescan`

This could take some hours, unless you are using *shossain's* server from the future. To check progress use something like:
>`tail ~/.komodo/debug.log -f`
`tail ~/.komodo/OOT/debug.log -f`

Once its all finished stop everything again.
>`~/scripts/stop`

We are all finished installing and are now ready to start the node, up to you but I find each command in a new tmux terminal best so you can monitor the outputs.
>`./start `

Start assets mines 10% of assets randomly, mine assets mines them all. Use this option if you have a server from the future.
>`./startassets or ./mineassets`

Once everything is loaded and synced up we can launch iguana and start dpow
>`cd ~/SuperNET/iguana`
`git checkout beta && ./m_notary && cd ~/komodo/src && ./dpowassets`

Congrats, you have installed your Notary Node and it should be running. Other things maybe to look at are setting up `ufw` for a software firewall to block all ports that are not being used. A sample script is included in the scripts folder from node operator *karasugoi*, called PORT_LIST.txt. 

The wallet.txt file in the scripts folder is no longer required. You should write its contents down or encrypt it and keep a copy along with passphrase.txt somewhere very safe in case your node dies and you need to recover the funds in the address or migrate to a new server. 

The passphrase.txt file is used by `wp_7776` to unlock the iguana wallet on node start-up. In the old guide, this passphrase was entered into the file directly, I just moved it to its own file. If anyone has a better or more secure way of doing this step please let me know. I am open to any collaboration to improve this document.

