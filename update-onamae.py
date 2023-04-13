#!/usr/bin/python3
# coding: utf-8
import os
import sys
import shutil
import subprocess
import socket
import ssl
import requests
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='update script for onamae ddns service')
    parser.add_argument('-f', '--filename',
                    metavar='script_filename',
                    type=str,
                    nargs=1,
                    default='./.onamae-env',
                    help='Set script filename')
    parser.add_argument('-i', '--interval',
                metavar='interval',
                type=str,
                nargs=1,
                default="0",
                help="Interval time(0(defalut):update only once, X:update every Xs, X[mh]: update every X[mh])." )
    return parser.parse_args()


def retrieve_ns_record(domain):
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
 
