import subprocess
import threading
import socket
import ipaddress
import click
import sys

def is_up(ip):
    """
    Test if a device at a specified ip is responding to ping.
    Returns a subprocess, once complete will have a returncode 0 if device responds.
    """
    return subprocess.Popen(["ping", "-c 1", "-q", ip], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def get_netdevice_list(netlist):
    """
    Create threaded processes to ping a list of ip addresses.
    Once all threads have finished compile a list of which ip
    addresses responded and return that list.
    """
    z = []
    for address in netlist:
        p = is_up(str(address))
        p.addr = str(address)
        z.append(p)

    alive_list = []
    for p in z:
        p.wait()
        if p.returncode == 0:
            alive_list.append(p.addr)
    return alive_list

def get_hostname_list(ip_addr_list):
    """
    Interrogate a list of ip addresses to get the hostname of the device, return a list of [ip address, hostname]
    """
    devlist = []
    for ip in ip_addr_list:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = ""
        devlist.append([ip, hostname])
    return devlist

def get_own_netaddr():
    """
    Get the ip address of the computer running the script.
    """
    hostname = ''.join((socket.gethostname(), '.local'))
    netaddr  = ''.join((socket.gethostbyname(hostname), '/24'))
    return netaddr

@click.command()
@click.argument('network_address', default = "" )
def main(network_address):
    if network_address == "":
        print("Network address not specified, defaulting to own network.")
        network_address = get_own_netaddr()

    netlist = ipaddress.ip_network(u''.join(network_address), strict=False)
    print("Testing addresses %s to %s..." % (ipaddress._find_address_range([x for x in netlist])))
    alivelist = get_netdevice_list(netlist)
    namelist = get_hostname_list(alivelist)
    if len(namelist) != 0:
        print("The following devices are alive")
        print("%15s  %s" % ("IP Address", "Hostname"))
        for dev in namelist:
            print("%15s  %s" % (dev[0], dev[1]))
    else:
        print("No devices found.")

if __name__==("__main__"):
    main()