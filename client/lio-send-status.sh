#!/bin/bash

#set -e -u

ip=''
mac=''
uptime=''
user=''
delay='10s'
url="http://olimpiada.lan:8000/submit/"

get_mac_ip() {
	local _dev="$(ip route | grep '^default ' | head -n 1 | \
		 cut -d ' ' -s -f 5)"
	mac="$(ip addr show dev ${_dev} | \
		sed -n -e 's#^ *\(link/ether .*\)$#\1#p' | \
		cut -d ' ' -s -f 2)"
	ip="$(ip addr show dev ${_dev} | \
		sed -n -e 's/^ *\(inet .*\)$/\1/p' | \
		cut -d ' ' -s -f 2 | cut -d '/' -f 1)"
}

get_user() {
    user="$(who | cut -d ' ' -f 1 | sort | uniq)"
}

get_uptime() {
	uptime="$(uptime | sed -n -e 's/^.* up *\([^,]*\),.*$/\1/p')"
}

show_status() {
	echo "ip: ${ip}"
	echo "mac: ${mac}"
	echo "user: ${user}"
	echo "uptime: ${uptime}"
}

send_status() {
	curl \
		-F "ip=${ip}" \
		-F "mac=${mac}" \
		-F "user=${user}" \
		-F "uptime=${uptime}" \
		"${url}"
}

while true; do
	get_mac_ip
	get_uptime
	get_user
	#show_status
	send_status
	sleep "${delay}"
done
