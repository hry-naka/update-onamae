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
    # args = get_args()
    print(retrieve_ns_record('80-81.com'))
