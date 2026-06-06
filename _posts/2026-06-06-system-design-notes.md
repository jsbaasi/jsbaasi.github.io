---
layout: post
title: system-design-notes
date: 2026-06-06 13:38:16 +0000
categories: development
permalink: /system-design-notes/
---
# building blocks:
## memory
- in-memory cache
- relational database
- nosql database
- blob storage
## compute
- server
- api gateway
- load balancer
## hybrid
- queues (store units of work to be completed however they compute complicated priority stuff in some cases)
- search-optimised database (inverted index where word points resolves to documents that contain the word)
# relational db vs nosql:
- rdbs is known for it's ACID properties. atomicity, consistency, isolation (?), durability (?) which means uhh data integrity. does this suggest that nosql doesn't have isolation or durability? i don't think  acid is necessarily where nosql fails, nosql can still have durability (replication and erasure coding)
- nosql for changing data schemas