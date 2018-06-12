from easysnmp import Session
import argparse
import socket

# Define constantes para TCP
STATE = {"01": "STABLISHED"}

# Resgata argumentos da linha de comando
parser = argparse.ArgumentParser(prog="netstat.py")
parser.add_argument(
    "-p", help="TCP or UDP protocol. If left blank, will display both."
)
parser.add_argument(
    "-a",
    help="IPv4 Address of remote client. If left blank, defaults to localhost.",
)

args = parser.parse_args()

if args.a:
    host = args.a
else:
    host = "localhost"

# Cria uma sessão SNMP
session = Session(hostname=host, community="public", version=2)

# Walk
if args.p is None:
    items = session.walk("tcp")
    for item in session.walk("udp"):
        items.append(item)
elif args.p.lower() == "tcp":
    items = session.walk("tcp")
elif args.p.lower() == "udp":
    items = session.walk("udp")
else:
    raise Exception


tcpdict = {}
udpdict = {}

if args.p is None or args.p.lower() == 'tcp':
    for item in items:
        if item.oid == "tcpConnState" and item.value == "5":
            tcpdict[item.oid_index] = {
                "status": "ESTABLISHED",
                "localAddr": "",
                "remoteAddr": "",
                "localPort": "",
                "remotePort": "",
            }
        if item.oid == "tcpConnLocalAddress" and item.oid_index in tcpdict.keys():
            tcpdict[item.oid_index]["localAddr"] = item.value
        if item.oid == "tcpConnRemAddress" and item.oid_index in tcpdict.keys():
            tcpdict[item.oid_index]["remoteAddr"] = item.value
        if item.oid == "tcpConnLocalPort" and item.oid_index in tcpdict.keys():
            tcpdict[item.oid_index]["localPort"] = item.value
        if item.oid == "tcpConnRemPort" and item.oid_index in tcpdict.keys():
            tcpdict[item.oid_index]["remotePort"] = item.value

    print(
        "proto\tLocal Address\tForeign Address\t(state)\t\tLocal Port\tRemote Port"
    )

    for key in tcpdict:
        # try:
        #     remoteAddr = socket.gethostbyaddr(tcpdict[key]["remoteAddr"])[0]
        # except:
        remoteAddr = tcpdict[key]["remoteAddr"]
        print(
            "tcp\t%s\t%s\t%s\t%s\t\t%s"
            % (
                tcpdict[key]["localAddr"],
                remoteAddr,
                tcpdict[key]["status"],
                tcpdict[key]["localPort"],
                tcpdict[key]["remotePort"],
            )
        )

if args.p is None or args.p.lower() == 'udp':
    #print(items)
    for item in items:
        if item.oid == "udpLocalAddress":
            udpdict[item.oid_index] = {
                "localAddr": item.value,
                "localPort": "",
            }
        if item.oid == "udpLocalPort" and item.oid_index in udpdict.keys():
            udpdict[item.oid_index]["localPort"] = item.value

    print(
        "proto\tLocal Address\tLocal Port"
    )

    for key in udpdict:
        print(
            "udp\t%s\t\t%s"
            % (
                udpdict[key]["localAddr"],
                udpdict[key]["localPort"],
            )
        )

#
# print(items)
#
# for item in items:
#     print(
#         "{oid}.{oid_index} {snmp_type} = {value}".format(
#             oid=item.oid,
#             oid_index=item.oid_index,
#             snmp_type=item.snmp_type,
#             value=item.value,
#         )
#     )
