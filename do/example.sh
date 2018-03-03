#!/bin/bash

source config.sh

echo
echo -e "${GREEN}This is example action${NC}"
echo

cat ./do/pony.art | base64 -d | gunzip
exit 1
