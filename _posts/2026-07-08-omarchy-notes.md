---
layout: post
title: Omarchy Notes
date: 2026-07-08 21:02:26 +0000
categories: notes
permalink: /omarchy-notes/
---
# setup
- `hyprctl reload`
- `SUPER + CTRL + E` for emojis
- chezmoi should bring in most of the bindings, just need to setup the repo so get ssh and possibly download firefox
- downloaded ghostty and then deleted alacritty
- installed vesktop
- added windows to limine with `sudo limine-scan` and it managed to find windows boot manager automagically
- edited `/boot/limine.conf` to add `timeout: no` to not have a timeout as opposed to 0 which is insta boot and then ran `limine-update`
# stuff to remember
- `CTRL + SUPER + SPACE` gives option to change backgrounds
- media player is `mpv`
- `SUPER + G` toggles the title of the application from showing
- `caligula` for burning images to disk
- `pkill waybar` and `hyprctl dispatch exec waybar` to restart after changes
- walker entries are stored in `.local/share/applications` but I could also have found it from `pacman -Fl $pkg | grep -re '\.desktop$'` `sudo find / -name "*.desktop" | grep obs` found it in `/usr/share/applications`
- `hyprctl globalshortcuts` to see what shortcuts you can bind to from an app
- firewall is on by default so need to allow ports
# to do
- waybar change to add more weather information
- [x] waybar chnage to add ram and cpu information
- waybar change to show when i'm in window resizing mode (SUPER+R)
# manual stuff
`cryptsetup open /dev/sdc2 root` to unlock the drive with my password, and open it as "root"
`mount /dev/mapper/root /mnt -o subvol=@` to see more of the directories
`arch-chroot /mnt`
replaced encrypt hook with encryptssh hook in /etc/mkinicpio.conf
`lspci` to get my ethernet interface driver, r8169
`/etc/default/limine` this is where limine-snapper-sync generates the limine.conf config to which i added
net.ifnames=0 so my interface is named eth0 instead of some gobbldygook
had to remove plymouth from my mkinitcpio hooks, which omarchy already had, and also removed splash from my 
cmdline in `/etc/default/limine`
`su` for changing user
@	/
@home	/home
@log	/var/log
@pkg	/var/cache/pacman/pkg