#!/bin/bash

source config.sh

case "$1" in

	# Start bitcoin and chips
	"bitchips")
		./do/bitchips.sh
		exit 1
	;;

	# Example
	"example")
		./do/example.sh
		exit 1
	;;

	# Default
	*)
		echo -e "James, is that ${RED}you${NC}?!"
		exit 1
	;;

esac
