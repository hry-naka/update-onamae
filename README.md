# update-onamae
update script for onamae ddns service

## 機能(実装仕様）
お名前ドットコムのDNS　Aレコードを更新する。
- 更新を要求する先のDNSサーバは、指定されたドメインのNSレコードの一番最初のレコードにある'fqdn'を使う。
- この'fqdn'にsslセッションをはって、使う人が準備したスクリプトをsendする（だけ）。
- このスクリプトには、'IPV4:xx.yy.zz.ww'で更新するIPアドレスを指定できる。'IPV4:GLOBAL-IP'と書くと、'https://ifconfig.me'
から取得したIPv4アドレスに置換して更新に使う。
- 更新する前のIPv4アドレスと、更新するアドレスが同じであれば、対応する更新（’MODIP　〜　.')を抜いたスクリプトをsendする。
すべてのHOSTNAME：の更新がスキップされることがある（LOGIN/LOGOUTするだけ）
- 起動オプションで、デーモン化できるようにして、更新要求を繰り返す周期も起動オプションで設定できるようにする。

## 仕様

```
usage: update-onamae.py [-h] [-f script_filename] [-i interval]

update script for onamae ddns service

optional arguments:
  -h, --help            show this help message and exit
  -f script_filename, --filename script_filename
                        Set script filename
  -i interval, --interval interval
                        Interval time(0(defalut):update only once, X:update every Xs, X[mh]: update every X[mh]).
```

## 使い方
### 一回限りの更新
```
% update-onamae
```
###　更新スクリプトファイルを指定して、１０分周期で更新
```
% update-onamae -f ./onamae-env --interval 10m
```
### スクリプトファイル

```
LOGIN
USERID:<お名前ドットコムのユーザID（何桁かの１０進数数字）＞
PASSWORD:＜パスワード＞
.
MODIP
HOSTNAME:www　＜空欄（ドメインのAレコード更新）も可能＞
DOMNAME:＜ドメイン名＞
IPV4:＜IPアドレス＞
.
MODIP
HOSTNAME:ssh
DOMNAME:＜ドメイン名、上で指定したドメイン名と違う名前を指定すると、想定しなかったDNSサーバに更新要求することがあるので同じものを指定してほしい＞
IPV4:GLOBAL-IP　＜このように書くと自動取得したグローバルアドレスに置換される＞
.
LOGOUT
.
```
