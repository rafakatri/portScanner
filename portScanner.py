#!/usr/bin/python3

import sys, socket, multiprocessing, argparse
from json import load

def port_scan(host, porta, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    if s.connect_ex((host,int(porta))) == 0:
        desc = ""
        for dic in data[porta]:
            if dic["tcp"]:
                desc += dic['description'] + ";\n"
        print(f"Porta {porta} [TCP] aberta: {desc}")


def multi_process(host, port_scan, porta, data):
    l = multiprocessing.Process(target=port_scan, args=(host,str(porta), data))
    l.start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip",help="Digite o endereço ip ou domínio")
    parser.add_argument("ports", help="Digite o range das portas, usando ':' como separador. Ex: 80:500")
    args = parser.parse_args()

    try:
        host = socket.gethostbyname(args.ip)
    except socket.gaierror:
        print("Host inválido, tente novamente")
        sys.exit(1)

    try:
        arg1, arg2 = args.ports.split(':')
        arg1 = int(arg1)
        arg2 = int(arg2)
    except:
        print("Formatação inválida das portas, tente novamente")
        sys.exit(1)
    
    for p in range(arg1,arg2+1):
        multi_process(host, port_scan, p, data)


if __name__ == "__main__":
    with open("ports.lists.json") as f:
        data = load(f)
    main()