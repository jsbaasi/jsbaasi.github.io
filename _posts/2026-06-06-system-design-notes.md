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
- cdn (nodes on the edge of the network, that serve responses to users. commonly used to serve common responses, replicated across different geographical locations to be as close as possible to the end user)
## compute
- server
- api gateway
- load balancer
## hybrid
- queues (store units of work to be completed however they compute complicated priority stuff in some cases)
- search-optimised database (inverted index where word points resolves to documents that contain the word)
- stream (streaming events)
- distributed lock (sometimes implemented in an in-memory cache like redis. key refers to what the object is, then value is whether the lock is held. relies on the atomicity property of the cache)
# relational db vs nosql:
- rdbs is known for it's ACID properties. atomicity (stores transactions to happen almost in a queue), consistency (write ahead log), isolation (constraints checked before commit), durability (file sync kernel call to the journal then kernel call to the database file. wal does this differently by queueing it) which means uhh data integrity. does this suggest that nosql doesn't have isolation or durability? i don't think  acid is necessarily where nosql fails, nosql can still have durability (replication and erasure coding)
- nosql for changing data schemas
# patterns:
## pushing realtime updates
- 
## managing long-running tasks
## dealing with contention
## scaling reads
## scaling writes
## handling large blobs
## multi-step processes
## proximity based services