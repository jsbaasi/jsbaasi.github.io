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
`docker exec -it <container_name> bash`
to get a bash shell to a running container
# how to see where a volume is stored on host
`docker volume ls`
`docker volume inspect myapp_dbdata`
# fixing permission errors
```
docker exec <container> id
sudo chown -R <UID>:<GID>
```
# how to get a shell in a stripped down image?
`docker debug` that is all
# confused about docker layers
my image name: `stormblessed/fudbot`
sources of confusion:
1) in `dive stormblessed/fudbot` the commands that separate layers doesn't make sense, they don't appear in my dockerfile at all
2) the files that i copy across are not seen in the dive layer images? like where is dpp_source or the app directory that I supposedly build my source code in?
3) i'm getting a linking error from my `cmake build` command in the `build` layer, i think this is from the lack of dpp `.so` libraries to link with? though I have copied them in from `dependencies` layer?