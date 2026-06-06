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
- pub/sub pattern generally. clients connected on a websocket to the server, server subscribes to updates from wherever the responses will come from. data flows through the long living connections constantly, meeting the realtime property
## managing long-running tasks
- client request long-running task. server acknowledges instantly and 1) responds a uid 2) creates job in the database 3) appends job to the queue. queue gets consumed by workers, workers perform work and update the job status in database/other system. server notices that work is done somehow and then follow up response is given to client
## dealing with contention
- cinema booking seats. key is to start with atomicity and transactional model where everything happens in one go or doesn't happen, then transition (deadlock or too complicated) to more complex distributed synchronisation techniques (distributed lock, two phase commit protocol, queue based serialisation). make it deterministic
## scaling reads
users are always reading more than writing, 10:1 ratio initially then becomes 100:1. first optimise db, optimise sql queries, denormalise your data (instead of having 0 duplication of data so a query could be multiple joins, have data copied to each table so reads don't have to join and are fast), indexes, perhaps different database technology (elasticsearch) THEN scale horizontally with read replicas (replication lag bad) THEN add caching considerations to the system network (cache invalidation, how to deal with a key that is particularly hot). trading off consistency for high availability. maybe redis cache for the database and then a cdn for the user
## scaling writes
optimise data model in database. normalise our data, remove indexes that aren't required. batching techniques for business logic THEN horizontal sharding (hash ring complexity, difficult to reverse this decision once set, but it is hard to definitively know your future needs of your system so always has to be considered carefully) THEN if there's unavoidable work to do then add a queue for the job, to be done asynchronously. cost of distributed synchronisation between workers and queue. OR add vertical partitioning, requests use a partition key to write to where their data is stored, challenging to get a good key, e.g. country is bad because it could be skewed towards one country, good is user ids, if its in 1xx range then location A, else it's 2xx then location B.
## handling large blobs
don't try to stream blobs through application server, will just exhause memory of the server. instead blob services like s3 (simple storage service) and gcp buckets can provide presigned urls, so client uploads directly to blob service and reads directly from blob service. system stores the metadata of the blob and it's location in the blob service, inside the system's database. challenges of this is maintaining consistency between metadata and what's in the blob, failures between client/blob service interactions. blob services anticipate this so provide an api for application servers, need to learn what's available for you to use in your system
## multi-step processes
instead of state of a process stored in different places and error handling of steps stored by the step, we can pull it out into central store of process state. client interaction kicks off the process, event is started in the store and pub sub topics are populated and subscribed to. the service that manages the "contract" of the process coordinates the different topics and workers and is responsible for kicking off error handling
## proximity based services
suppose we want to search something close to us. take for example an uber driver that is close to me, we shouldn't need to enumerate all drivers that are active o(N) we have a range query index instead o(logN) where we discard sections of our data entirely by location. implemented by special indexes in database. reducing search space well. costs a lot to accurately maintain this index. increases cost of adding a driver perhaps, and then replication of this index is complex as well