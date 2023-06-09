# update-onamae
update script for onamae ddns service

## 機能(実装仕様）
お名前ドットコムのDNS　Aレコードを更新する。
- "ddnsclient.onamae.com:65010", にopensslコマンドでConfigの内容をsendする。
- このスクリプトのコンフィグファイルには、'IPV4:xx.yy.zz.ww'で更新するIPアドレスを指定できる。'IPV4:GLOBAL-IP'と書くと、'https://ifconfig.me'
から取得したIPv4アドレスに置換して更新に使う。
- 更新する前のIPv4アドレスと、更新するアドレスが同じであれば、対応する更新（’MODIP　〜　.')を抜いたスクリプトをsendする。Skipのメッセージは出す（INFO)。
- すべてのHOSTNAME：の更新がスキップされるときには、”No A-record has to be updated. Continue..”をINFOレベルで出力する。この場合はopnesslの起動も行わない。
- 起動オプションで、デーモン化できるようにして、更新要求を繰り返す周期も起動オプションで設定できるようにする。

## 仕様

```
usage: update-onamae.py [-h] [-f config_filename] [-i time] [-l logfile level]

update config file for onamae ddns service

options:
  -h, --help            show this help message and exit
  -f config_filename, --filename config_filename
                        Set config filename
  -i time, --interval time
                        Interval time(0(defalut):update only once, X:update
                        every Xs, X[mMhH]: update every X[mMhH]).
  -l logfile level, --log logfile level
                        logfile name and loglevel(DEBUG..CRITICAL)
```

## 使い方
### 一回限りの更新
```
% update-onamae
```
### コンフィグファイルを指定して、１０分周期で更新
```
% update-onamae -f ./onamae-env --interval 10m
```
### コンフィグファイルを指定して、１０分周期で更新、ログ・ファイル名とレベルをINFOに指定（デフォルトはINFO）
```
% update-onamae -f ./onamae-env --interval 10m -l test.log INFO
```
### コンフィグファイル
パスワードが入りますので、'chmod　600'等はしておいてください。

```
USERID=<お名前ドットコムのユーザID（何桁かの１０進数数字）＞
PASSWORD=＜パスワード＞
HOSTNAME=www　＜空欄（ドメインのAレコード更新）も可能＞
DOMNAME=＜ドメイン名＞
IPV4=＜IPアドレス＞
HOSTNAME=ssh
DOMNAME=＜ドメイン名、上で指定したドメイン名と違う名前を指定すると、想定しなかったDNSサーバに更新要求することがあるので同じものを指定してほしい＞
IPV4:GLOBAL-IP　＜このように書くと自動取得したグローバルアドレスに置換される＞
```
