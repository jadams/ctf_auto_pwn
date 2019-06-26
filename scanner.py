#!/usr/bin/env python3
import sys
import json
import socket
import ipaddress
import urllib.request
from socket import timeout
from urllib.error import HTTPError, URLError
from multiprocessing import Pool
from ping3 import ping

NUM_CPUS = 8

def validate_ip(subnet):
    ip = subnet.split('/')[0]
    try:
        socket.inet_aton(ip)
    except socket.error:
        return False
    else:
        return True


def pinger(addr):
    resp = ping(str(addr))
    if(resp):
        return str(addr)

def get_alive(subnet):
    with Pool(NUM_CPUS*10) as p:
        alive_hosts = p.map(pinger, ipaddress.IPv4Network(subnet))
    hosts = []
    for ip in alive_hosts:
        if(ip):
            hosts.append(ip)
    print(hosts)

def httper(host):
    url = 'http://'+host
    try:
        response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
    except:
        return { 'ip': host, 'http':None }
    else:
        return { 'ip': host, 'http':response }

def check_http(hosts):
    with Pool(NUM_CPUS) as p:
        host_responses = p.map(httper, hosts)
    return host_responses

def parse_http(hosts):
    for host in hosts:
        print(host['ip'])
    return

def main():
    if(len(sys.argv) <= 1):
        return -1
    if(validate_ip(sys.argv[1])):
        subnet = sys.argv[1]
    else:
        return -1
    net, cidr = subnet.split('/')
    #alive_hosts = get_alive(subnet)
    alive_hosts = ['10.101.0.1', '10.101.0.11', '10.101.0.13', '10.101.0.14', '10.101.0.15', '10.101.0.16', '10.101.0.17', '10.101.0.18']
    http_hosts = check_http(alive_hosts)
    no_http = []
    for host in http_hosts:
        if not host['http']:
            no_http.append(host)
            http_hosts.remove(host)
    #parse_http(http_hosts)
    print(json.dumps(http_hosts))


if __name__ == '__main__':
    sys.argv.append('10.101.0.0/24')
    main()