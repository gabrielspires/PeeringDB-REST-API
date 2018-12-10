#!/usr/bin/env python3

# ./client IP:port Opt
# IP:port = ip e porto do servidor
# Opt = nº da análise ("0" -> IXPs por rede ou "1" -> redes por IXP)
# fechar após análise

import socket
import json
import sys


def opt0(ip, port):
    analisis = {}
    # cria socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, int(port))
    sock.connect(server_address)

    request_header = 'GET /api/ix HTTP/1.1\r\nHost: http://' + ip + ':' + port + '\r\n\r\n'
    sock.send(request_header.encode())

    responseix = ''
    while True:
        recv = sock.recv(4096)
        if not recv:
            break
        responseix += recv.decode()

    responseix = responseix.split('\n')
    ixdata = json.loads(responseix[-2])
    sock.close()

    for ix in ixdata["data"]:
        # cria socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, int(port))
        sock.connect(server_address)

        request_header = 'GET /api/ixnets/'+str(ix["id"])+' HTTP/1.1\r\nHost: http://' + ip + ':' + port + '\r\n\r\n'
        sock.send(request_header.encode())

        responseixnets = ''
        while True:
            recv = sock.recv(4096)
            if not recv:
                break
            responseixnets += recv.decode()

        responseixnets = responseixnets.split('\n')
        ixnetsdata = json.loads(responseixnets[-2])
        sock.close()

        for item in ixnetsdata["data"]:
            if item not in analisis:
                # cria socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = (ip, int(port))
                sock.connect(server_address)

                request_header = 'GET /api/netname/' + str(item) + ' HTTP/1.1\r\nHost: http://' + ip + ':' + port + '\r\n\r\n'
                sock.send(request_header.encode())

                responsenetname = ''
                while True:
                    recv = sock.recv(4096)
                    if not recv:
                        break
                    responsenetname += recv.decode()

                responsenetname = responsenetname.split('\n')
                netnamedata = json.loads(responsenetname[-2])
                sock.close()

                analisis[item] = {"id": item,"name": netnamedata["data"], "ass": 1}
            else:
                analisis[item]["ass"] += 1

    for netid in sorted(analisis):
        print(analisis[netid]["id"], analisis[netid]["name"], analisis[netid]["ass"], sep='\t')


def opt1(ip, port):
    # cria socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, int(port))
    sock.connect(server_address)

    request_header = 'GET /api/ix HTTP/1.1\r\nHost: http://' + ip + ':' + port + '\r\n\r\n'
    sock.send(request_header.encode())

    response = ''
    while True:
        recv = sock.recv(4096)
        if not recv:
            break
        response += recv.decode()

    response = response.split('\n')
    ixdata = json.loads(response[-2])

    analisis = {}

    for ix in ixdata["data"]:
        analisis.update({str(ix["id"]): {"id": ix["id"], "name": ix["name"], "ass":0}})

    # print(analisis)
    sock.close()


    for item in analisis:
        # cria socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, int(port))
        sock.connect(server_address)

        request_header2 = 'GET /api/ixnets/'+item+' HTTP/1.1\r\nHost: http://' + ip + ':' + port + '\r\n\r\n'
        sock.send(request_header2.encode())

        response2 = ''
        while True:
            recv2 = sock.recv(4096)
            if not recv2:
                break
            response2 += recv2.decode()

        response2 = response2.split('\n')
        ixdata2 = json.loads(response2[-2])
        analisis[item]["ass"] = len(set(ixdata2["data"]))

        sock.close()

        print(analisis[item]["id"],analisis[item]["name"], analisis[item]["ass"],sep='\t')

    return


def main():
    # parâmetros da linha de comando
    ip, port = sys.argv[1].split(":")
    opt = sys.argv[2]

    if opt == '0':
        opt0(ip, port)
    if opt == '1':
        opt1(ip, port)


if __name__ == '__main__':
    main()