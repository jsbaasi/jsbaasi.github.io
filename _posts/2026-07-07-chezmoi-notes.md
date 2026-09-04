---
layout: post
title: Chezmoi Notes
date: 2026-07-07 21:34:05 +0000
categories: notes
permalink: /chezmoi-notes/
---
- [x] need to make gacp clean up subshells and make tmux close pane bind
- `cz update` to pull in changes and apply them e.g. you made changes on machine 1 and want to sync that to machine 2
# starting on a new machine
- install chezmoi, ideally through some kind of package manager
- `chezmoi init git@github.com:jsbaasi/dotfiles.git`
- config should be in `~/.local/share/chezmoi`
- `cz diff` and tweak the templates so you don't have your existing config overwritten (see top of page to make and edit templates)
# i made edits outside of chezmoi edit?
- use chezmoi add to add your local file. it may lose template attributes so not sure how to get around that