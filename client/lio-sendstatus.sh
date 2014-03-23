#!/bin/bash

#set -e -u

url="http://localhost:8000/submit/"
delay='10s'

usage_error() {
	echo "usage: $0 [-d DELAY] [URL]"
	exit 1
}

if [[ $# -eq 1 ]]; then
	url="$1"
elif [[ $# -ge 2 ]]; then
	if [[ "$1" -ne "-d" ]]; then
		usage_error
	fi
	delay="$2"
	if [[ $# -eq 3 ]]; then
		url="$3"
	elif [[ $# -gt 3 ]]; then
		usage_error
	fi
fi

ip=''
mac=''
uptime=''
user=''

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
