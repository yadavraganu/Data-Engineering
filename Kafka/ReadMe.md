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
