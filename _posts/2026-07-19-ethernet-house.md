---
layout: post
title: Ethernet House
date: 2026-07-19 18:37:30 +0000
categories: notes
permalink: /ethernet-house/
---
![[side_profile.excalidraw]]
238.3 Mbps download, 106.9 Mbps upload, Latency: 7 ms on 28th july using powerline adapters after having new broadband installed

Hosted by Digi UK (Luton) [96.69 km]: 12.453 ms Testing download speed................................................................................ Download: 807.01 Mbit/s Testing upload speed...................................................................................................... Upload: 106.15 Mbit/s on 6th august after installing ethernet sockets from room to router

59.3 mbit download 89.17 mbit upload on home server wifi, mere centimeters away

77.6 mbit download 73 upload on home server ethernet ???

i did `iperf3 -s` and `iperf3 -c <server ip>` between 2 local machines and got 91.3mbit/sec retr 91

snake cow rabbit screwfix reference
orange-white orange
blue-white blue
green-white green
brown-white brown
# options
## 1
## 2
## 3

blinds are on 171-172cm track hook style blinds, 89mm width vanes, centre open

# lighting
writing a mqtt message, need to forward port with `ssh -L 1883:192.168.0.115:1883 jjhome`
```
mosquitto_pub -t 'zigbee2mqtt/bridge/request/device/bind' -m '{ "from":"jj_ceiling_relay","to":"jj_ceiling_light"}'
```
which added two bindings, one for the light source endpoint `11` destination `coordinator` endpoint `1`
then for the relay source endpoint `1` destination `light` endpoint `11`