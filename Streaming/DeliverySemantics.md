In stream processing, **delivery semantics** define how a system guarantees that a message is processed. Because streaming systems are distributed and prone to failures (network issues, machine crashes, etc.), ensuring data integrity is a major challenge. These semantics determine the trade-offs between data loss, duplication, and performance.

### At-Most-Once

**At-most-once** semantics guarantee that each message is processed **zero or one time**. This is the fastest but least reliable option. If a failure occurs during processing, the system simply gives up and doesn't retry, so the message might be lost.

* **How it works:** The system commits or acknowledges a message as processed as soon as it's received, before the actual processing logic runs. If the system crashes after the acknowledgement but before processing is complete, the message is lost forever.
* **Use Case:** Ideal for scenarios where data loss is acceptable and speed is the top priority, such as in-app logging or sensor data that only provides non-critical metrics.

### At-Least-Once

**At-least-once** semantics guarantee that each message is processed **one or more times**. This prevents data loss but can introduce duplicates. If a system fails before it can confirm that a message was processed, it will reprocess the message upon recovery, potentially leading to duplication.

* **How it works:** The system processes the message first, and then commits or acknowledges it. If a crash occurs after processing but before the acknowledgment is sent, the message will be reprocessed.
* **Use Case:** Common for many stream processing applications where data integrity is important. To handle duplicates, downstream systems must be **idempotent**, meaning that processing the same message multiple times has the same effect as processing it just once.

### Exactly-Once

**Exactly-once** semantics guarantee that each message is processed **exactly one time**, with no duplicates and no data loss. This is the most complex to achieve but provides the highest level of data integrity.  It requires a sophisticated, coordinated effort between the producer, the streaming system, and the consumer.

* **How it works:** Achieving this typically involves a two-phase commit protocol or a transactional system. The system bundles the message processing, the state updates (if any), and the message acknowledgment into a single, atomic transaction. If any part of the transaction fails, the entire thing is rolled back, ensuring that the message is reprocessed in its entirety upon recovery.
* **Use Case:** Critical for applications where correctness is non-negotiable, like financial transactions, where a duplicate credit or debit would be catastrophic.
