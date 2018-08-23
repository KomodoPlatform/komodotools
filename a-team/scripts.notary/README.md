### Notary Instructions:
Start VM
Run `sync_ramdisk` and let it finish: 20 mins currently.
Run `start` wait for KMD to start.
Run `startassets` wait for all AC to start.
Run `resetALLwallet`
Import privkey to VRSC.
Run m_notary or m_notary_run (depends if iguana needs recompile)
Once Iguana started, run `cron_splitfunds`
Then run `dpowassets` from komodo/src
