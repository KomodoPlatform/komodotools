pubkey='02ffda5a0147e781308fe66a1774793eacd9b35829073746b217845cfe7577b7dc'

# Num of threads for mining kmd
genproc=8

# Homedir if needs to be altered
# userhome='/home/kolo'
userhome=$HOME

# Your IP. Can be set static
# myip='123.45.67.89'
myip=`curl -s4 checkip.amazonaws.com`

piddir='/var/run/'

# Color
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
