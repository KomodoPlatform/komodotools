#!/bin/bash
sudo renice -n -19 -p `eval "pgrep -f 'iguana notary'"`


