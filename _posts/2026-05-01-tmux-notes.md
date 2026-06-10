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

our config already has split bindings (lines 14–17 of

~/.config/tmux/tmux.conf

). With your prefix being

Ctrl+Space

(or

Ctrl+b

as a secondary): ┌───────────────┬────────────────────────────────────────────────────────────┐ │ Keys │ Result │ ├───────────────┼────────────────────────────────────────────────────────────┤ │

prefix

then

h

│ split

horizontally

— new pane below (

split-window -v

) │ ├───────────────┼────────────────────────────────────────────────────────────┤ │

prefix

then

v

│ split

vertically

— new pane to the right (

split-window -h

) │ ├───────────────┼────────────────────────────────────────────────────────────┤ │

prefix

then

x

│ kill the current pane │ └───────────────┴────────────────────────────────────────────────────────────┘ So e.g. press

Ctrl+Space

, release, then

h

. Both splits open in the

current pane's directory

(the

-c "#{pane_current_path}"

part), so a new pane starts wherever you already are. A couple of related things already in your config: -

Move between panes:

Ctrl+Alt+arrow

(no prefix needed) — lines 19–22. -

Resize panes:

Ctrl+Alt+Shift+arrow

(no prefix) — lines 24–27.