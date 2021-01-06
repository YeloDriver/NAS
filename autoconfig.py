#! usr/bin/py3

import json


def autoconfigurator(nb, hostname, router_id, interfaces, ttl, label_range):
    f = open("D:/GITHUB/NAS/i"+nb+"_startup-config.cfg", "w")
    f.write('''!
!
!

!
! Last configuration change at 13:59:25 UTC Sat Dec 12 2020
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname %s
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
no ipv6 cef
!
!
mpls label range %s
mpls ldp maxhops %s
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
''' %(hostname, label_range, ttl))

    f = open("D:/GITHUB/NAS/i"+nb+"_startup-config.cfg", "a")
    for i in range(len(interfaces)):
        if interfaces[i]["status"] == "shutdown":
            f.write('''interface %s
 no ip address
 shutdown
 duplex full
 !
 '''%(interfaces[i]["name"]))
        else:
            f.write('''interface %s
 ip address %s
 negotiation auto
 mpls ip
 mpls mtu %s
 !
 '''%(interfaces[i]["name"],interfaces[i]["ip4"], interfaces[i]["mtu"]) )
    



with open('D:/GITHUB/NAS/config.json') as file:
    data = json.load(file)

for i in data["Routers"]:
    hostname = data["Routers"][str(i)]["hostname"]
    router_id = data["Routers"][str(i)]["router_id"]
    interfaces = data["Routers"][str(i)]["Interfaces"]
    ttl = data["Routers"][str(i)]["ttl"]
    label_range = data["Routers"][str(i)]["label_range"]
    autoconfigurator(i[1], hostname, router_id, interfaces, ttl, label_range)
