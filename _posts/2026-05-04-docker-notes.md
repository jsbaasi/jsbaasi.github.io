---
layout: post
title: Docker Notes
date: 2026-05-04 22:36:54 +0000
categories: development docker
permalink: /docker-notes/
---
`docker build -t <app_name> <path_to_working_directory>`
docker build -t bot .
`docker run <app_name>`
whatever you tagged your app with
docker run bot
`docker run --rm -it <app_name> sh`
interactive and tty shell into image. remove after done