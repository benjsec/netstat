#NetStat

A simple tool for interrogating a given subnet and showing any live devices and their hostname if it exists.

##Usage
python netstat.py ipaddress/netmask

The ipaddress can be ipv4 or ipv6. Netmask can be either short or long form for either. If no netmask is provided only a single ip address will be scanned.
If no argument is provided it will default to the local ip address of the device running the script with a netmask of 255.255.255.0

##Dependencies
Requires ipaddress, tested with v1.0.6
	pip install ipaddress

##TODO
- [x] Accept command line arguments.
- [x] Remove hard-coded parameters.