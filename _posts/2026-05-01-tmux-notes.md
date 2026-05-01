---
layout: post
title: tmux Notes
date: 2026-05-01 20:40:14 +0000
categories: development
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