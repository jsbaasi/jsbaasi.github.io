---
layout: post
title: tmux Notes
date: 2026-05-01 20:40:14 +0000
categories: development notes
permalink: /tmux-notes/
---
prefix = `<C+b>`
prefix, `d` to detach
prefix, " to split vertically
prefix, `%` to split horizontally
prefix, `[` for copy-mode, a mode where you can select and move around output
prefix, `$` rename session

`tmux ls` to list all sessions
`tmux a -t <session_name>` attach to <session_name>

on omarchy
alt+v to enter copy mode (vim scroll mode)
prefix is ctrl+space
(this is opposite of tmux standard)
prefix h - create a horizontal divider
prefix v - create a vertical divider
prefix x - close pane
prefix z - full screen pane
alt + hjkl to move panes
alt + shift + hjkl to move panes

using CTRL-d to close a pane currently