#!/usr/bin/python3
# coding: utf-8
import os
import sys
import time
import shutil
import subprocess
import requests
import argparse
import re


def get_args():
    parser = argparse.ArgumentParser(
        description='update config file for onamae ddns service')
    parser.add_argument('-f', '--filename',
                        metavar='config_filename',
                        nargs=1,
                        default=['./.onamae-env'],
                        help='Set config filename')
    parser.add_argument('-i', '--interval',
                        metavar='time',
                        nargs=1,
                        default=['0'],
                        help="Interval time(0(defalut):update only once, X:update every Xs, X[mh]: update every X[mh]).")
    return parser.parse_args()


def convert_interval(interval):
    r = re.match( "([0-9]*)[mM]$", interval )
    if r:
        return int(r.group(1)) * 60
    r = re.match( "([0-9]*)[hH]$", interval )
    if r:
        return int(r.group(1)) * 60 * 60
    r = re.match( "([0-9]*)$", interval )
    if r:
        return int(r.group(1))
    print( "Invalid inteval time.")
    sys.exit(1)


def get_global_ip():
    url = 'https://ifconfig.me'
    return (requests.get(url).content.decode('utf-8'))


def get_a_record(host, domain):
    dig = shutil.which('dig')
    if dig is None:
        print('This tool need dig to be installed to executable path')
        print('Soryy, bye.')
        sys.exit(1)
    else:
        if host == '':
            a_record = subprocess.Popen(
                f'{dig} {domain} a +short'.split(), stdout=subprocess.PIPE)
        else:
            a_record = subprocess.Popen(
                f'{dig} {host}.{domain} a +short'.split(), stdout=subprocess.PIPE)
        a_record = a_record.stdout.read().decode('utf-8')
        return a_record.strip()


def read_config(filename):
    hostname = []
    ipv4 = []
    userid = password = domain = None
    with open(filename) as f:
        for l in f.readlines():
            if len(l) == 0:  # 空白行は無視
                continue
            k, v = l.rstrip().split('=')
            if k == 'USERID':
                userid = v
            elif k == 'PASSWORD':
                password = v
            elif k == 'DOMNAME':
                domain = v
            elif k == 'HOSTNAME':
                if len(v) == 0:
                    v = '@'
                hostname.append(v)
            elif k == 'IPV4':
                ipv4.append(v)
    if userid is None or password is None or domain is None:
        print("Wrong config file. userid,password,domain should be specified.¥n")
        sys.exit(1)
    if len(hostname) == 0 or len(ipv4) == 0:
        print("Wrong config file. hostname, ipv4 should be specified.¥n")
        sys.exit(1)
    if len(hostname) != len(ipv4):
        print('Wrong config file. number of hostname should be the same as the number of ipv4¥n')
        sys.exit(1)
    return userid, password, domain, hostname, ipv4


def convert_cmd(userid, password, domain, hostname, ipv4, global_ip):
    login_cmd = "LOGIN\n"
    login_cmd += f"USERID:{userid}\n"
    login_cmd += f"PASSWORD:{password}\n.\n"
    i = 0
    modify_cmd = ""
    for host in hostname:
        if host == "@":
            host = ""
        if ipv4[i] == 'GLOBAL-IP':
            ipv4[i] = global_ip
        ip = get_a_record(host, domain)
        if ipv4[i] == ip:
            print(
                f"SKIP:{host}.{domain}'s ip address({ip}) won't be changed.")
            i += 1
            continue
        else:
            print(
                f"MODIFY:{host}.{domain}'s ip address({ip}) will be changed to {ipv4[i]}.")
            modify_cmd += "MODIP\n"
            modify_cmd += f"HOSTNAME:{host}\n"
            modify_cmd += f"DOMNAME:{domain}\n"
            modify_cmd += f"IPV4:{ipv4[i]}\n.\n"
            i += 1
    return login_cmd, modify_cmd


def do_update(userid, password, domain, hostname, ipv4):
    global_ip = get_global_ip()  # global_ipを取得する
    login_cmd, modify_cmd = convert_cmd(
        userid, password, domain, hostname, ipv4, global_ip)
    cmd = login_cmd + modify_cmd + "LOGOUT\n.\n"
    #print( cmd )
    openssl = shutil.which('openssl')
    openssl += ' s_client -connect ddnsclient.onamae.com:65010 -quiet'
    p = subprocess.Popen(
        openssl.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # 標準入力にテキストを書き込み、標準出力から暗号化されたテキストを読み込む
    stdout_data, stderr_data = p.communicate(input=cmd.encode())
    # エラーがあれば出力する
    if p.returncode:
        print( f"status code:{p.returncode}\n" )
        if stderr_data:
            print(f"stderr msg:{stderr_data.decode()}")
    if "003 DBERROR" in stdout_data.decode().strip():
        print( "Failed to update.\n" )
    return


def daemonize(userid, password, domain, hostname, ipv4, interval):
    pid = os.fork()  # fork child process
    if pid > 0: 
        sys.exit()
    elif pid == 0:  # 子プロセスの場合
        while True:
            do_update(userid, password, domain, hostname, ipv4)
            time.sleep(interval)


if __name__ == '__main__':
    args = get_args()
    if os.path.isfile( args.filename[0] ) == False:
        print( f"config file {args.filename[0]} doen't exist.")
        sys.exit(1)
    userid, password, domain, hostname, ipv4 = read_config(
        args.filename[0])
    interval = convert_interval(args.interval[0])
    if interval == 0:
        do_update(userid, password, domain, hostname, ipv4)
    else:
        daemonize(userid, password, domain, hostname,
                  ipv4,interval )
