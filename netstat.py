import subprocess
import threading
import socket
import ipaddress
import click

def is_up(ip):
    return subprocess.Popen(["ping", "-c 1", "-q", ip], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def get_netdevice_list(netlist):
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
    devlist = []
    for ip in ip_addr_list:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = ""
        devlist.append([ip, hostname])
    return devlist

def get_network(raw_input):
    return ipaddress.ip_network(raw_input, strict=False)


@click.command()
@click.argument('network_address')
def main(network_address):
    print("Scanning network for live devices.")
    netlist = get_network(u''.join(network_address))
    alivelist = get_netdevice_list(netlist)
    namelist = get_hostname_list(alivelist)
    for dev in namelist:
        print(dev)

if __name__==("__main__"):
    main()