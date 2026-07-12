---
layout: post
title: Jellyfin Notes
date: 2026-07-12 17:01:37 +0000
categories: notes
permalink: /jellyfin-notes/
---
Each movie needs to be in it's own folder. it can named in the following format:
`<movie_name> <year> <tmbdid>`
so for example
`Welcome (2007) [20294]` and then movie within the folder be named the same thing, with the file extension at the end
and then subtitles with same title
```
-r flag for recursive so you can copy the entire directory
scp -r <path_to_movie_directory> jelly:/var/lib/jellyfin/media/<library>
```