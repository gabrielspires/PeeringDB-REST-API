#!/usr/bin/env python3

#./server port Netfile Ixfile Netixlanfile

import socket
import json
import sys
from flask import Flask

app = Flask(__name__)

host = "127.0.0.1"
# parâmetros da linha de comando
port =              sys.argv[1]
netfilepath =       sys.argv[2]
ixfilepath =        sys.argv[3]
netixlanfilepath =  sys.argv[4]


with open(netfilepath, 'r') as netjson:
    netfile = json.load(netjson)
    if netfile: print("net loaded...")

with open(ixfilepath, 'r') as ixjson:
    ixfile = json.load(ixjson)
    if ixfile: print("ix loaded...")

with open(netixlanfilepath, 'r') as netixlanjson:
    netixlanfile = json.load(netixlanjson)
    if netixlanfile: print("netixlan loaded...")


@app.route('/api/ix')
def ix():
    ixquery = {"data": ixfile["data"]}
    return json.dumps(ixquery)+"\n"


@app.route('/api/ixnets/<ix_id>')
def ixnets(ix_id):
    ixidquery = {"data": []}
    for net in netixlanfile["data"]:
        if net['ix_id'] == int(ix_id):
            ixidquery["data"].append(net["net_id"])
        ixidquery["data"] = sorted(list(set(ixidquery["data"])))
    return json.dumps(ixidquery)+"\n"


@app.route('/api/netname/<net_id>')
def netname(net_id):
    netnamequery = {"data": ''}
    for net in netfile["data"]:
        if net['id'] == int(net_id):
            if "name" in net:
                netnamequery["data"] = net["name"]
                return json.dumps(netnamequery)+"\n"
            else:
                return ""
    return ""


if __name__ == '__main__':
    app.run(debug=True)