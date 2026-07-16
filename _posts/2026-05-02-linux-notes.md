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
