---
layout: post
title: Termux Notes
date: 2026-07-17 14:03:00 +0000
categories: notes
permalink: /termux-notes/
---
Cleaned my git repo. To cd to "home" directory then you have to go to `/storage/emulated/0/` and then this website repo is stored within `Documents`

keys are stored at `~/.ssh` absolute `/data/data/com.termux/files/home/.ssh`

~~To setup again make sure you git clone the ssh version of the repo?~~ obsidian git plugin on termux doesn't seem to recognise ssh, so have to put in a pat even if you cloned via ssh, as I found through setting up personal_notes repo

you can't even clone the repo with ssh despite painstakingly setting up my ssh config, has to be through http, and then have to fill out the pat token again in access credentials of plugin settings