---
layout: post
title: Chezmoi Notes
date: 2026-07-07 21:34:05 +0000
categories: notes
permalink: /chezmoi-notes/
---
look at chezmoi templates page
variables are like {{ .chezmoi.something }} and you can do conditional logic within the curly brackets as well to determine what gets copied to the relevant files
- my common workflow, `cz add` then `cz chattr +template` then `cz edit` then `cz diff` then `cz apply`