---
layout: post
title: Running a small isolated vm
date: 2026-08-14 13:26:04 +0000
categories: development
permalink: /running-a-small-isolated-vm/
---
1) install qemu, in particular we'll need `qemu-img` and `qemu-system-x86_64` e.g. `sudo apt install qemu` or `pacman -S qemu-desktop`
2) get a small linux distro image, i'm using alpine so https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/ 
3) then create disk image with `qemu-img create -f qcow2 downloaded_image 8G` -f for format `qcow2`
4) boot with `qemu-system-x86_64 -m 512 -nic user -boot once=d -cdrom alpine-standard-3.24.1-x86_64.iso -drive file=alpine.qcow2 -display gtk` and optionally `-enable-kvm` flag if it's supported on your machine
5) login as root user e.g. `su`
6) setup your distro e.g. `setup-alpine`