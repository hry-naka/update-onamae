#!/usr/bin/python3
# coding: utf-8
import os
import sys
import time
import shutil
import subprocess
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
                        help="Interval time(0(defalut):update only once, X:update every Xs, X[mh]: update every X[mh]).")
    return parser.parse_args()


def convert_interval(interval):
    value = int(interval)  # Not yet to be implemented
    return (value)


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
        if host == '@':
            a_record = subprocess.Popen(
                f'{dig} {domain} a +short'.split(), stdout=subprocess.PIPE)
        else:
            a_record = subprocess.Popen(
                f'{dig} {host}.{domain} a +short'.split(), stdout=subprocess.PIPE)
        # a_record = a_record.stdout.read().decode('utf-8').split()[0]
        a_record = a_record.stdout.read().decode('utf-8')
        return a_record.strip()


def read_config(filename):
    hostname = []
    ipv4 = []
    userid = password = domain = None
    with open(filename) as f:
        for l in f.readlines():
            if len(l) == 0:
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
    login_cmd = 'LOGIN¥n'
    login_cmd += f"USERID:{userid}¥n"
    login_cmd += f"PASSWORD:{password}¥n."
    i = 0
    modify_cmd = ""
    print( f"G-IP: {global_ip}:{type(global_ip)}")
    for host in hostname:
        if ipv4[i] == 'GLOBAL-IP':
            ipv4[i] = global_ip
        if ipv4[i] == get_a_record(host, domain):
            print(
                f"SKIP:{host}.{domain}'s ip address({ipv4[i]}) won't be changed.")
            i += 1
            continue
        modify_cmd += 'MODIP¥n'
        if host == '@':
            modify_cmd += f"HOSTNAME:¥n"
        else:
            modify_cmd += f"HOSTNAME:{host}¥n"
        modify_cmd += f"DOMNAME:{domain}¥n"
        modify_cmd += f"IPV4:{ipv4[i]}¥n."
        i += 1
    return login_cmd, modify_cmd


def connect():
    # ドメインのNSレコードを取得する
    # NSレコードのfqdnにsocketを接続する
    return


def send_login(login_cmd):
    # 　login_cmdを送信する
    # 　エラーだったら念のためLogoutする
    return


def send_modify(modify_cmd):
    # modify_cmdを送信する
    # 　エラーの場合はlogoutする
    return


def send_logout():
    cmd = 'LOGOUT¥n.'
    # cmdをsendする
    # 　エラー処理する
    return


def do_update(userid, password, domain, hostname, ipv4):
    global_ip = get_global_ip()  # global_ipを取得する
    login_cmd, modify_cmd = convert_cmd(
        userid, password, domain, hostname, ipv4, global_ip)
    print(login_cmd)
    print(modify_cmd)
    sys.exit(1)
    connect(get_ns_record(domain))  # domainのNSサーバにコネクト
    send_login(login_cmd)
    send_modify(modify_cmd)
    send_logout()
    return


def daemonize(userid, password, domain, hostname, ipv4, interval):
    pid = os.fork()  # fork child process
    if pid > 0:  # Parrent proocess
        pid_file = open('/var/run/python_daemon.pid', 'w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    elif pid == 0:  # 子プロセスの場合
        while True:
            do_update(userid, password, domain, hostname, ipv4)
            time.sleep(interval)


if __name__ == '__main__':
    args = get_args()

    userid, password, domain, hostname, ipv4 = read_config(
        args.filename[0])  # filenameを読み出す
    if (int(args.interval) == 0):
        do_update(userid, password, domain, hostname, ipv4)
    else:
        daemonize(userid, password, domain, hostname,
                  ipv4, convert_interval(args.interval))
    # print( args.filename )
    # print( args.interval )
    # print( get_global_ip() )
