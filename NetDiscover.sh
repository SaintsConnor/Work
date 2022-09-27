#!/bin/bash

# ------- Notes -------
# This program has not been optimised. This is a python experiment, if successful development will begin on a shell script equivalent that is more optimized. 
# Please contact Connor if any questions, details listed below

# ------- Author Info -------

# Github.com/SaintsConnor
# Discord: connor#2597
# Email: venomsneakymc@gmail.com

if [ "$1" == "" ]
then
echo "You forgot an IP address!"
echo "Syntax: ./ipsweep.sh 192.168.1"

else
  for ip in `seq 1 254`; do
    IP=()
    ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" & IP+=(ip)
    python3 PortScanner.py ip > $1_IP=[ip].txt
   
  done
fi
