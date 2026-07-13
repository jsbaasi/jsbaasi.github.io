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
- added MODULES=(amdgpu) to `/etc/mkinitcpio.conf` and rebuilt with `sudo mkinitcpio -P` which was met by `WARNING: This does not update Limine boot entries. Use 'limine-mkinitcpio' or 'limine-update' instead.` i just agreed
# stuff to remember
- `CTRL + SUPER + SPACE` gives option to change backgrounds
- media player is `mpv`
- `SUPER + G` toggles the title of the application from showing
- `caligula` for burning images to disk
- `pkill waybar` and `hyprctl dispatch exec waybar` to restart after changes
# to do
- waybar change to add more weather information
- waybar chnage to add ram and cpu information
- waybar change to show when i'm in window resizing mode (SUPER+R)