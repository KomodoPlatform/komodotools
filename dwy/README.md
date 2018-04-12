## Lazynode
Still in dev. Purpose is to get the maximum info, with the minimum commands :D. It is NOT optimized, but in its current state, it works (for me :D)
The goal is to see in one command how is node running, if everything is fine, and if there is any action needed. It's obvious any NN operator can do this manually, but simplifying it with global commands can save time.
One thing that is possible is to get a checksequence, and be able to manage it. Possible just to check everything, and/or act on any failed test (sync nok, process KO, etc...)

## Params
Check that your BTC/KMD address are the good ones, or the validate just will throw that it's not yours :).
check that you don't have any specific path for bitcoind/chipsd/komodod. By default it will assume it has been installed as the NN setup guide advised.


## Functions
### check

Checks the actual state of your node.

If a coin is missing, it will just relaunch it, based on assetchains file (komodo/src/assetchains).
When all non commented coins are launched and synced, will launch iguana on a screen called 'iguana'

When every coin and iguana is OK, will call validateaddress.

To work properly, check has to be the "launcher" of all coins/assetchains, just because when it checks coins running/not running, the isrunningcall is based on specific syntax, for example, if you call ./komodod -pubkey=XXX manually, and the check search for komodod -gen, it will return that coin is not properly launched.
Will fix this in future versions.

To summarize it, check will be able to launch everything just after a boot / when everything is stopped : In that case it will launch everything you need.
In case everything is already launched, it will just check that everything is ok. Something missing : It will be relaunched.

### utxo
galtmines script searching for utxo matching the size needed for notarization. Just added parsing file to get those counts for every coin.

### stats
webworker notarization check adapted to get count from every coin.

### validateaddress  [' '|coinname|ac|dpow]
Validate that the address you typed in params (top of the lazynode file) is yours.
That could seem useless, but you can just add parameters : 
	'' : will validate for BTC/CHIPS/KOMODO and any coin on komodo/src/assetchains that are not commented.
	coin : will validate for that specific coin
	ac : will validate every AC not commented on komodo/src/assetchains
	dpow : will validate every AC called by dpowassets (in case you launched it manually)
	
### isrunning  "coinname|iguana" [nolog]
Is this process running? :)

### startac "coinname"
Will launch every AC not commented on assetchains file, if not running

### countac
returns 1 if on AC not commented from assetchains file is missing

### stopiguana
Stops iguana and wipe iguana screen

### stopprocess "coinname"
Stops that coin from running.

### checksync "coinname"
Checks status of the sync for that coin. In case it is not synced, will wait and show the progress.

### startprocess "coinname"
Start that coin. Special case for iguana, starts a screen called iguana, then start all commands to get it running on that screen.

### listac
Lists all AC that are not commented on assetchains file.

### listdpow
Lists all AC that are on dpowassets file.

### listall
Lists everything that will be launched with a check call. To summarize : BTC/KMD/CHIPS/AC*/IGUANA

### listallcommented
List everycoin : BTC/KMD/CHIPS and all AC, commented or not on assetchains file.

### getdebug [' '|coinname|ac|dpow] [tailsize]
Print the debug file for the coin passed as arg, tailsize modifying the... tailsize :D 
	If no coin arg, will just use all coins / AC not commented.
	If numeric value : will change the tail size.
	If specific coin : will only show the debug for that coin.
	
	Possible to get previous build lists (ac: all AC not commented - dpow: all coins from dpowassets file)
	
### stopall
stops everything, iguana included (and its screen)
(manual AC not launched via lazynode won't be stopped)

### shouldrun
is everything running ? BTC/KMD/CHIPS/AC not commented on assetchains/IGUANA ? 1 command, all the info.

### help
list of commands.


## info
Not intended to replace anything... but just help seeing in a very fast way how things are doing.