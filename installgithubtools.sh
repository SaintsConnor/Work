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

call_cmd "git clone https://github.com/SaintsConnor/Exploits"
call_cmd "git clone https://github.com/SaintsConnor/Scripts-PenTest"
call_cmd "git clone https://github.com/danielmiessler/SecLists.git"
call_cmd "git clone https://github.com/SSGorg/Cryptex"
call_cmd "./Cryptex/src/install.sh"
