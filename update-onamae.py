#!/usr/bin/python3
# coding: utf-8
import os
import sys
import shutil
import subprocess
import logging
import socket
import ssl
import requests
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='update config file for onamae ddns service')
    parser.add_argument('-f', '--filename',
                    metavar='config_filename',
                    type=str,
                    nargs=1,
                    default='./.onamae-env',
                    help='Set config filename')
    parser.add_argument('-i', '--interval',
                metavar='interval',
                type=str,
                nargs=1,
                default="0",
                help="Interval time(0(defalut):update only once, X:update every Xs, X[mh]: update every X[mh])." )
    return parser.parse_args()

def get_global_ip():
    url = 'https://ifconfig.me'
    return( requests.get(url).content.decode('utf-8'))

    
def get_ns_record(domain):
    dig = shutil.which('dig')
    if dig is None:
        print('This tool need dig to be installed to executable path')
        print('Soryy, bye.')
        sys.exit(1)
    else:
        ns_record = subprocess.Popen(f'{dig} {domain} ns +short'.split(), stdout=subprocess.PIPE)
        ns_record = ns_record.stdout.read().decode('utf-8').split()[0]
        return ns_record


if __name__ == '__main__':
    args = get_args()
    print( args.filename )
    print( args.interval )
    print( get_global_ip() )
 
