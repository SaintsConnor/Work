#!/bin/bash
# ------- Notes -------
# Please contact Connor if any questions, details listed below

# ------- Author Info -------

# Github.com/SaintsConnor
# Discord: connor#2597
# Email: venomsneakymc@gmail.com


function call_cmd(){
	xte "str $1"
	sleep 0.5
	xte "key Return"
}

call_cmd pkill -9 -t pts/$1
