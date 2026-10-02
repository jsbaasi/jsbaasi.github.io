---
layout: post
title: Linux Notes
date: 2026-05-02 14:19:00 +0000
categories: development
permalink: /linux-notes/
---
`find <path you want to search> <predicates>`
e.g I want to find all files that start with index in the current directory
`find . -name index*`

# keybind for clearing terminal
cmd + k, ghostty mac

`~/.ssh/config` can contain shortcuts for vps connection but also specify what commands to run when landing there with:
```
RequestTTY yes
RemoteCommand cd Coding/jsbaasi && exec $SHELL
```

and you can also avoid having to eval `$(ssh-agent -s)` with adding:
```
Host gitlab.com
	User git
	IdentityFile ~/.ssh/jsbaasigitlab
```

to get logs from a running process you can do from proc filesystem, `tail -f /proc/<pid>/fd/1`
file descriptor 1 is stdout and 2 is stderr
```
echo -n something | base64
```
if you do echo without the -n then it echos with line break
`netstat -anp | find "port number"` to check if port number is occupied

`killall <username> OR pkill -u <username>` to kill every process owned by a user

```
sudo -u <user> -g <group> test -w /file/to/test || {
   echo "user cannot write the file"
}
```
command to check if a user:group would be able write to a file, can use -r and -x as well
octal notation for permissions is easy rwx:
| owner perms | group perms | anybody else |
`strace -e openat obs` this is how to see what directories an application, in this case obs, opens

`journalctl -xeu` x for mathcing messages to a catalogue defined by the developer, e for pager end shorthand, u for unit
# how do i check if a port is open
with `nmap -p <port> <hostname>`
# how do i change my bash prompt
`set PS1='<prompt>'`
# how to forward a port?
`ssh -L LOCAL_PORT:localhost:REMOTE_PORT user@remote-machine`
so for my psql
`ssh -L 5432:localhost:5432 jjvps`
# how to write a systemd unit file?
```
[Unit]                                                                             Description=Elixir service for flagup                                              After=network.target
                                                               [Service]
ExecStart=/opt/fuservice/bin/lbs start                                             Restart=always

User=deploy
Group=deploy

Environment=PATH=/usr/bin:/usr/local/bin
Environment=PHX_SERVER=true
Environment=DATABASE_PATH=/var/lib/fuservice_data/lbs.sqlite3
Environment=SECRET_KEY_BASE=FzzgfzaVgvdO2+F8yvpBKyxoga4Ksa7QQYdoi2bA375EZxouyNRqKXHLovSHxz9b
Environment=PORT=54001
Environment=API_KEY_FILE=/var/lib/fuservice_data/api_keys.txt
Environment=RELEASE_DISTRIBUTION=none

WorkingDirectory=/opt/fuservice

[Install]
WantedBy=multi-user.target
```
reverse engineer this
# how to generate a random string for a secret token?
`openssl rand -hex 32`