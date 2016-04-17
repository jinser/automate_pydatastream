#!/bin/bash

#check that username and password were entered as input arguments
if [ "$#" -ne 2 ]; then
	echo "please enter the username and password, like automate_pydatastream.sh <username> <password>."
else
	#get all data symbols for custom retrieval from input folder
	custom=$(find input/*.json -printf "%f\n")
	for filename in $custom
	do
		python getcustom.py $1 $2 $filename
	done
fi