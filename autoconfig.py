#! usr/bin/py3

import json
import sys
import os

def autoconfigurator(path, nb, hostname, ospf_process_id, router_id, interfaces, ttl, label_range):
    dirs = os.listdir( path)
    if dirs[0] == "i"+nb+"_startup-config.cfg":
        f = open(path+"/i"+nb+"_startup-config.cfg", "w")
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
''' % (hostname, label_range, ttl))

        f = open(path+"/i"+nb+"_startup-config.cfg", "a")
        for i in range(len(interfaces)):
        
            if interfaces[i]["status"] == "shutdown":
                f.write('''interface %s
no ip address
shutdown
duplex full
!
''' % (interfaces[i]["name"]))
            else:
                f.write('''interface %s
ip address %s
negotiation auto
mpls ip
mpls mtu %s
!
''' % (interfaces[i]["name"], interfaces[i]["ip4"], interfaces[i]["mtu"]))

        f.write('''router ospf %s
router-id %s
''' % (ospf_process_id, router_id))
        for i in range(len(interfaces)):
            if interfaces[i]["status"] == "on":
                f.write(''' network %s area % s\n'''%(interfaces[i]["network"],interfaces[i]["area"]))

        f.write('''!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
!
!
control-plane
!
!
line con 0
exec-timeout 0 0
privilege level 15
logging synchronous
stopbits 1
line aux 0
exec-timeout 0 0
privilege level 15
logging synchronous
stopbits 1
line vty 0 4
login
!
!
end
''')


path = sys.path[0]
with open(path + '/config.json') as file:
    data=json.load(file)

for i in data["Routers"]:
    hostname=data["Routers"][str(i)]["hostname"]
    router_id=data["Routers"][str(i)]["router_id"]
    interfaces=data["Routers"][str(i)]["Interfaces"]
    ttl=data["Routers"][str(i)]["ttl"]
    label_range=data["Routers"][str(i)]["label_range"]
    ospf_process_id = data["Routers"][str(i)]["ospf_process_id"]
    dirs = os.listdir( path +"\\project-files\\dynamips")
    for file in dirs:
        autoconfigurator(path +"\\project-files\\dynamips\\"+file + "\\configs", i[1], hostname, ospf_process_id, router_id, interfaces, ttl, label_range)
