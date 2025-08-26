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
