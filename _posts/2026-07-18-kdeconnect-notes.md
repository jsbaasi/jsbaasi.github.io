---
layout: post
title: KDEConnect Notes
date: 2026-07-18 23:29:26 +0000
categories: notes
permalink: /kdeconnect-notes/
---
some combination of `exec /usr/bin/kdeconnectd` `kdeconnect -platform offscreen`, may require two shells because running the daemon is blocking

# writing commands from console
go to kdeconnect conifg and make sure commands are enabled 
```
[Plugins] kdeconnect_remotecommandsEnabled=true
```
navigate to runcommands , device id, and config should mirror the following format:
```
commands={"ffe82d97-cd8d-4fe6-a585-2df5d6f1f4fc":{"name":"jjpcomarchy","command":"wakeonlan -i 192.168.0.255 b4:2e:99:1f:9c:36"}}
```