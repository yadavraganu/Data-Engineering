# **What Is a Kafka Record?**

A Kafka record is a **key-value pair** sent by a producer to a specific **topic-partition**, and later consumed by a consumer. It contains metadata that helps Kafka manage and route the message efficiently.

### **Fields in a Kafka Record**

| Field | Description |
|-------|-------------|
| **Key** | Optional. Used to determine the partition (via hashing). Ensures ordering for messages with the same key. |
| **Value** | The actual payload or data (e.g., JSON, Avro, string, binary). |
| **Topic** | The name of the Kafka topic the record belongs to. |
| **Partition** | The partition number within the topic. If not specified, Kafka uses a partitioner. |
| **Offset** | A unique, sequential ID assigned by Kafka within a partition. Used for tracking consumption. |
| **Timestamp** | Time when the record was produced (or logged by the broker). |
| **Headers** | Optional key-value metadata pairs (e.g., for tracing, content-type). |
| **Checksum** | Used internally to verify data integrity. |

# In Sync Replica
In Kafka, **In-Sync Replicas (ISR)** are a critical part of the **replication mechanism** that ensures **data durability and consistency** across the cluster.

### What Are In-Sync Replicas (ISR)?

An **In-Sync Replica** is a **replica of a partition** that is **fully caught up with the leader**. This means it has all the messages that the leader has written to its log, up to the latest committed offset.

### Components Involved

- **Leader Replica**: The broker that handles all read/write operations for a partition.
- **Follower Replicas**: Brokers that replicate data from the leader.
- **ISR**: A subset of replicas (including the leader) that are **up-to-date** with the leader.

### How ISR Works

1. **Producer sends data** to the leader of a partition.
2. **Leader writes** the data to its local log.
3. **Followers pull** the data from the leader.
4. Kafka checks if followers are **caught up** (within a configured lag).
5. If yes, they remain in the ISR. If not, they are **temporarily removed**.

### Configuration Parameters

- `replica.lag.time.max.ms`: Maximum time a follower can lag behind the leader before being removed from ISR.
- `min.insync.replicas`: Minimum number of ISR members required for Kafka to acknowledge a write (used with `acks=all`).

### Why ISR Matters

- **Data Reliability**: Ensures that data is replicated before acknowledging to producers.
- **Leader Election**: Only ISR members are eligible to become the new leader if the current one fails.
- **Write Guarantees**: With `acks=all`, Kafka waits for all ISR members to confirm the write.

### What Happens If ISR Shrinks?

- If the number of ISR members drops below `min.insync.replicas`, Kafka **rejects writes** with `acks=all`.
- This protects against **data loss** in case of broker failures.

# Kafka Offsets
In Kafka, an **offset** is a unique identifier assigned to each message within a **partition**. It represents the **position** of a record in the log and is crucial for tracking and consuming data reliably.

### What Is an Offset?

- Think of a Kafka partition as a **log file**.
- Each message in that log has a **sequential number** called an **offset**.
- Offsets are **per-partition**, not global across the topic.

### Why Offsets Matter

Offsets allow:
- **Consumers** to track where they left off.
- **Kafka** to support **replayability** (you can re-read messages).
- **Parallelism**: Each partition has its own offset sequence.

### Offset Management

Consumers can:
- **Auto-commit** offsets (default, but risky if processing fails).
- **Manually commit** offsets after successful processing.
- Store offsets in:
  - Kafka itself (default)
  - External systems (e.g., Zookeeper, databases)

### Key Concepts

| Term | Description |
|------|-------------|
| **Offset** | Position of a message in a partition |
| **Committed Offset** | Last offset acknowledged by the consumer |
| **Current Offset** | Offset of the message being processed |
| **Lag** | Difference between latest offset and committed offset |

# Kafka Log Segments
In Kafka, a **segment** is a **chunk of a partition log file** stored on disk. Each Kafka topic partition is made up of **multiple segments**, and these segments are the basic units Kafka uses to manage, store, and clean log data.

### What Is a Segment?

- A **log segment** is a file that stores a **sequence of messages** (records) for a partition.
- Kafka **appends** new messages to the **active segment**.
- When the segment reaches a certain **size** or **age**, it is **rolled** (closed), and a new segment is created.

### Segment Structure

Each segment consists of:
- A **log file** (e.g., `00000000000000000000.log`)
- An **index file** (e.g., `.index`) for fast offset lookup
- A **time index** (e.g., `.timeindex`) for time-based searches

### Segment Lifecycle

1. **Active Segment**: Kafka writes new messages here.
2. **Rolled Segment**: Once full (based on `log.segment.bytes` or `log.segment.ms`), it becomes inactive.
3. **Eligible for Compaction or Deletion**:
   - If `cleanup.policy=compact`, Kafka may compact it.
   - If `cleanup.policy=delete`, Kafka may delete it after `retention.ms`.

### Key Configs

| Config | Description |
|--------|-------------|
| `log.segment.bytes` | Max size of a segment before rolling |
| `log.segment.ms` | Max time before rolling |
| `retention.ms` | How long to keep segments (for delete policy) |
| `cleanup.policy` | Determines if segments are compacted or deleted |

# Kafka Log Compaction Config
Kafka log compaction is a mechanism for data retention that ensures only the latest value for each message key is retained within a topic's log. This contrasts with time-based retention (the default), which simply discards old segments based on age or size.
### Key Settings and Explanation:
#### cleanup.policy=compact (Topic Level).
This is the primary setting to enable log compaction for a specific topic. When set, Kafka's log cleaner process will periodically scan the topic's partitions and remove older records with the same key, keeping only the most recent one.
#### min.cleanable.dirty.ratio (Broker/Topic Level):
This setting defines the minimum ratio of "dirty" (uncompacted) bytes to total log size that triggers a compaction cycle. For example, a value of 0.5 (default) means compaction will be considered when at least 50% of the data in a log segment is eligible for compaction.
#### min.compaction.lag.ms (Broker/Topic Level):
This setting prevents overly aggressive compaction. It ensures that a message remains in the log for at least this duration before it becomes eligible for compaction, even if a newer message with the same key arrives. This provides a grace period for consumers to process older messages before they are potentially removed.
#### max.compaction.lag.ms (Broker/Topic Level):
This setting acts as an upper bound, forcing compaction to occur if a message has existed in the log for longer than this duration, regardless of the min.cleanable.dirty.ratio. This prevents data from remaining uncompacted indefinitely if the dirty ratio threshold is not met. delete.retention.ms (Broker/Topic Level).  
When a message is "deleted" by sending a new message with the same key and a null value (a "tombstone" message), this setting determines how long the tombstone will be retained before being permanently removed during compaction. This allows consumers to observe the deletion event.
#### How it Works:
- Kafka partitions are divided into segments.
- The log cleaner identifies "dirty" segments containing older versions of records with duplicated keys.
- It then creates new, "cleaned" segments containing only the latest value for each key.
- These new segments replace the old, dirty ones, effectively compacting the log.
- Offsets remain consistent: if a message is removed, consumers simply skip over its offset.

# Kafka Delivery Semantics
Kafka provides three delivery semantics to control how messages are sent and received: **at-most-once**, **at-least-once**, and **exactly-once**. The chosen semantic depends on the application's tolerance for data loss or duplication.

### At-Most-Once Delivery
In **at-most-once** delivery, the producer sends a message and considers it successful without waiting for an acknowledgment from the broker. This approach is the fastest and offers the lowest latency, but it risks message loss if the producer fails before the broker receives the message.

* **How it works**: The producer sends the message and immediately moves on. If a network error or broker failure occurs, the message might be lost.
* **Use case**: This is suitable for applications where some data loss is acceptable, like logging or real-to-time telemetry, where the goal is to get as much data as possible, and losing a small fraction isn't critical.

### At-Least-Once Delivery
**At-least-once** delivery ensures that a message is delivered to the broker at least once. The producer re-sends a message until it receives an acknowledgment (ACK) from the broker, confirming the message was successfully written to the topic partition.

* **How it works**: The producer sends a message and waits for an ACK. If the ACK isn't received within a timeout period, the producer retries. This can lead to duplicate messages if the ACK is delayed or lost, but the message itself is guaranteed not to be lost.
* **Use case**: This is the default setting in Kafka and is widely used for applications where data loss is unacceptable but duplication can be handled by the consumer, such as an idempotent consumer that processes a message multiple times without side effects.

### Exactly-Once Delivery
**Exactly-once** delivery guarantees that a message is delivered and processed by the consumer exactly one time, with no duplicates and no data loss. This is the most complex semantic and requires coordination between the producer, broker, and consumer. It is achieved through Kafka's **idempotent producers** and **transactions**.

* **How it works**:
    1.  **Idempotent Producers**: The producer assigns a unique identifier to each batch of messages. The broker tracks these identifiers and ignores any duplicate batches, preventing duplicate writes to the log.
    2.  **Transactions**: Transactions group multiple message writes across various partitions into a single, atomic unit. All messages within a transaction are either committed successfully or aborted. This ensures that the messages are processed together.
* **Use case**: This is essential for financial transactions, inventory management, or any application where data integrity is paramount and both data loss and duplication are unacceptable.

# How Kafka Log Compaction Works

Kafka topics support two main ways of discarding old data: time-based deletion and key-based compaction. Time-based deletion removes messages older than a configured retention period, while compaction retains only the latest value for each unique key.

- delete  
  Removes all records older than `retention.ms`, regardless of key.  

- compact  
  Keeps only the newest record per key; earlier versions are dropped. Requires non-null keys.  

- delete_and_compact  
  First compacts by key, then deletes any remaining records older than the retention window.

Common use cases for compaction include storing each customer’s most recent shipping address and maintaining an application’s latest state checkpoint for crash recovery. Compacted topics provide a space-efficient snapshot of current state without historical noise.

Kafka compaction is a background process that shrinks each partition down to exactly one record per key—the latest value—by scanning only the “dirty” portion of the log and merging it with the already “clean” history.

### 1. Partition Layout: Clean vs. Dirty

- **Clean portion**  
  Contains segments that were processed in previous compaction runs. Each key appears exactly once here, holding its latest known value at that time.

- **Dirty portion**  
  Holds all messages written since the last compaction. Keys may appear multiple times, with newer updates appended to the tail.

### 2. Compaction Threads

- When you enable `log.cleaner.enabled=true`, each broker spins up:  
  - A **compaction manager** that coordinates work  
  - Multiple **cleaner threads** that actually do the compaction  
- Each thread picks the partition with the highest ratio of dirty data to total size—so Kafka focuses on the messiest logs first.

### 3. Building the Offset Map

1. The cleaner reads the dirty segments of a chosen partition.  
2. It constructs an in-memory map of `(keyHash → offsetOfNextNewerRecord)`.  
3. Each entry is 24 bytes (16 bytes for the key hash + 8 bytes for the offset).  
   - E.g., a 1 GB segment with 1 million 1 KB messages uses ~24 MB of map memory.  
4. If keys repeat, the map reuses entries and memory needs shrink further.

### 4. Memory Configuration

- You set a total budget for all cleaner threads via `log.cleaner.dedicated.max.memory`.  
- That budget is divided evenly across threads—so 1 GB total with 5 threads → each gets 200 MB.  
- Kafka only requires that at least one full segment fit in a thread’s map:  
  - If no segment fits, you’ll see errors.  
  - If only some segments fit, the cleaner compacts the oldest ones first and leaves the rest dirty for later.

### 5. The Compaction Pass

1. **Scan Clean Segments**  
   The cleaner reads the oldest clean segment one record at a time.  
2. **Check the Map**  
   - If the record’s key is still present in the map → skip it (a newer version exists).  
   - If the key is absent → copy the record into a new replacement segment (it’s still the most recent).  
3. **Swap Segments**  
   Once all surviving records are copied, the new segment replaces the old clean segment on disk.  
4. **Repeat**  
   The thread moves on to the next segment until the dirty portion is fully processed or memory runs out.

### 6. End Result

After compaction finishes, the partition holds exactly one message per key—and that message is the most recent update. Historical churn is eliminated, making compacted topics an efficient snapshot of current state.

### Beyond the Basics

- **Tuning tips**  
  - Adjust `log.cleaner.threads` and total map memory based on your throughput and key-cardinality.  
  - Monitor `LogCleanerManager` JMX metrics (`percentDirty`, `cleanerIdleRatio`) to spot lagging compaction.  

- **Trade-offs**  
  - Very large keys or ultra-high update rates can bloat map requirements.  
  - Compaction still incurs I/O and CPU overhead—plan your cluster size accordingly.

# What Is the Kafka Controller?

- Kafka is a distributed system with multiple brokers.
- One broker is elected as the **controller** to manage tasks that affect the entire cluster.
- The controller is responsible for **partition leadership**, **broker failure handling**, and **metadata propagation**.

### How Is the Kafka Controller Elected?

#### In ZooKeeper-Based Kafka:
1. **Election via ZooKeeper**:
   - Brokers compete to create an ephemeral node in ZooKeeper (e.g., `/controller`).
   - The broker that succeeds becomes the controller.
   - If the controller fails, the node disappears, triggering a new election.

2. **Ephemeral Node**:
   - Ensures only one controller exists at a time.
   - Automatically cleaned up if the broker disconnects or crashes.

#### In KRaft Mode (Kafka Raft Metadata Mode):
1. **Raft-Based Election**:
   - Kafka uses its own internal Raft consensus protocol.
   - One broker is elected as the **active controller**.
   - Metadata is stored in a replicated log across controller quorum nodes.

2. **No ZooKeeper Needed**:
   - KRaft eliminates ZooKeeper, simplifying architecture and improving scalability.

### Responsibilities of the Kafka Controller

| Task | Description |
|------|-------------|
| **Partition Leader Election** | Assigns leaders for partitions across brokers |
| **Broker Failure Detection** | Detects broker crashes and reassigns leadership |
| **Topic Creation/Deletion** | Propagates metadata changes to all brokers |
| **Replica Management** | Updates ISR (In-Sync Replicas) and handles replication |
| **Controlled Shutdown** | Gracefully migrates leadership before broker shutdown |
| **Cluster Metadata Management** | Maintains and distributes metadata across brokers |

### Controller Failover

- If the controller broker fails:
  - A new controller is elected.
  - The new controller reads metadata and resumes coordination.
  - This process is fast but may cause brief delays in cluster operations.


# Apache Kafka settings for high throughput and low latency

### **Producer Optimization**

Producers are the entry point for data into Kafka. Their configuration affects how efficiently data is batched, compressed, and transmitted.

| Setting | Recommended Value | Description |
|--------|-------------------|-------------|
| `acks` | `1` or `0` | Controls how many acknowledgments the producer waits for. `0` offers lowest latency but risks data loss; `1` balances speed and reliability. |
| `batch.size` | `32KB` – `64KB` | Defines how much data to batch before sending. Larger batches reduce network overhead and improve throughput. |
| `linger.ms` | `5ms` – `10ms` | Adds a small delay to allow more records to batch together. Improves throughput with minimal latency impact. |
| `compression.type` | `lz4` or `snappy` | Compresses messages to reduce payload size. These algorithms are fast and efficient for streaming. |
| `max.in.flight.requests.per.connection` | `5` or more | Allows multiple requests to be sent without waiting for responses. Boosts throughput but may affect message ordering. |
| `buffer.memory` | `64MB` or more | Total memory available for buffering unsent records. Prevents producer blocking under high load. |

### **Broker Optimization**

Kafka brokers handle message storage, replication, and coordination. Their performance is critical for both producers and consumers.

| Setting | Recommended Value | Description |
|--------|-------------------|-------------|
| `num.network.threads` | `8+` | Threads for handling network I/O. More threads allow brokers to serve more clients concurrently. |
| `num.io.threads` | `8+` | Threads for disk I/O operations. Helps with log writing and replication. |
| `socket.send.buffer.bytes` | `128KB` | Buffer size for sending data over the network. Larger buffers reduce I/O overhead. |
| `log.segment.bytes` | `1GB+` | Determines when Kafka rolls over to a new log segment. Larger segments reduce disk I/O frequency. |
| `replica.fetch.max.bytes` | `1MB` – `5MB` | Controls how much data replicas fetch per request. Larger values improve replication speed and reduce lag. |

### **Topic & Partition Design**

Topic and partition design affects scalability, parallelism, and message ordering.

| Strategy | Recommended Value | Description |
|----------|-------------------|-------------|
| Partition Count | 2× number of consumers | More partitions allow parallel processing and higher throughput. |
| Key Design | Use meaningful keys (e.g., user ID) | Ensures messages with the same key go to the same partition, preserving order. |
| Replication Factor | `2` or `3` | Ensures fault tolerance. More replicas improve durability but may slightly impact performance. |

### **Consumer Optimization**

Consumers read data from Kafka and must be tuned to process efficiently.

| Setting | Recommended Value | Description |
|--------|-------------------|-------------|
| `fetch.min.bytes` | `1KB` – `10KB` | Minimum amount of data to fetch. Reduces round-trips and improves throughput. |
| `fetch.max.bytes` | `1MB` – `5MB` | Maximum data fetched per request. Larger values allow more efficient batch processing. |
| `max.poll.records` | `500` – `1000` | Number of records returned per poll. Higher values improve throughput but may increase processing time. |
| `enable.auto.commit` | `false` | Manual offset management gives better control and avoids unnecessary commits. |

### **System-Level Tuning**

These optimizations improve Kafka’s performance at the infrastructure level.

| Area | Recommendation | Description |
|------|----------------|-------------|
| Disk | Use SSDs | Kafka is disk-intensive. SSDs improve log write/read speed. |
| OS Tuning | Increase file descriptors, socket buffers | Enhances Kafka’s ability to handle high I/O and many connections. |
| JVM Tuning | Use G1GC or ZGC | Reduces garbage collection pauses, improving latency. |
| Monitoring | Use Prometheus, Grafana | Helps detect bottlenecks and optimize performance in real time. |

### Final Tips

- **Batching and compression** are key for throughput.
- **Low acknowledgment and fast disks** help reduce latency.
- **Partition wisely** to scale horizontally.
- **Monitor everything** to catch performance issues early.
