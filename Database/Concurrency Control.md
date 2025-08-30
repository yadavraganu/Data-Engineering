Concurrency control is a fundamental concept in database management systems (DBMS) that ensures multiple transactions can be executed simultaneously without compromising data integrity and consistency. It's essential in multi-user environments where multiple processes may try to access and modify the same data at the same time. The primary goal is to manage these concurrent operations to avoid conflicts and maintain the **ACID properties** (Atomicity, Consistency, Isolation, Durability) of transactions.

### Why is concurrency control needed?
Without concurrency control, several problems can arise that lead to data corruption or incorrect results:

* **Lost Updates**: This occurs when two transactions read the same data, and both try to update it. The second update can overwrite the first, causing the initial change to be lost.
* **Dirty Reads**: One transaction reads data that has been modified by another, but the changes have not yet been committed. If the second transaction then fails and rolls back its changes, the data read by the first transaction becomes invalid.
* **Non-repeatable Reads**: A transaction reads the same data item twice but gets a different value each time. This happens when another committed transaction modifies the data between the two reads.
* **Phantom Reads**: A transaction reads a set of data items that satisfy a certain condition. Another transaction then inserts new data items that also satisfy the condition. When the first transaction re-runs its query, it finds a "phantom" new data item.
* **Dirty Write**: It occurs when a transaction writes to a data item that another, uncommitted transaction has already modified. If the first transaction then aborts, its changes are rolled back, and the second transaction's write is left in an invalid state. This is a severe problem that most databases prevent even at low isolation levels.
* **Read Skew**: It happens when a transaction reads two related but different data items at different points in time, and another transaction modifies one of those items in between the reads. This causes the first transaction to see a logically inconsistent state of the data. For example, reading an old balance from one account and a new balance from a related account, resulting in a nonsensical total.
* **Write Skew**: This is a more subtle anomaly where two transactions each read a set of data items and then decide to write to different, non-overlapping items in that same set. The combined effect of their committed changes violates a business rule that would have been maintained in a serial execution. The classic example is two on-call doctors checking that at least one doctor is on-call, and then both deciding to go off-call, resulting in zero doctors on-call.  This is a difficult problem to prevent and typically requires the highest isolation level: **Serializable**.
### Concurrency Control in Single-Node Databases
In a single-node database, all transactions and data reside on a single machine. The primary goal is to ensure serializability, which means that the result of concurrent transactions is the same as if they were executed one after the other in some serial order. The main techniques used are:

* **Locking-Based Protocols**: These are **pessimistic** approaches that assume conflicts are likely. They involve transactions acquiring locks on data items before accessing them.
    * **Shared Locks (Read Locks)**: Allow multiple transactions to read the same data simultaneously but prevent any transaction from writing to it.
    * **Exclusive Locks (Write Locks)**: Give a single transaction exclusive access to a data item, preventing any other transaction from reading or writing to it.
    * **Two-Phase Locking (2PL)**: This is a widely used protocol. A transaction is divided into a "growing phase" where it can acquire locks but not release any, and a "shrinking phase" where it can release locks but not acquire any new ones. This ensures serializability but can lead to deadlocks.
When multiple transactions run simultaneously, they can interfere with each other, leading to data inconsistencies. **Dirty writes**, **read skew**, and **write skew** are three specific types of concurrency anomalies that describe these issues.
* **Timestamp-Based Protocols**: In this approach, each transaction is assigned a unique timestamp when it begins. The DBMS then ensures that the execution of transactions is equivalent to a serial schedule where transactions are ordered by their timestamps. A conflict (like a write operation from an older transaction trying to overwrite a younger one) results in the older transaction being aborted and restarted with a new timestamp.

* **Optimistic Concurrency Control (OCC)**: This is an **optimistic** approach that assumes conflicts are rare. Transactions are allowed to proceed without acquiring locks. When a transaction is ready to commit, it undergoes a validation phase to check if any of the data it read or wrote has been modified by another committed transaction. If a conflict is detected, the transaction is aborted and restarted.

* **Multi-Version Concurrency Control (MVCC)**: Instead of locking data, MVCC allows transactions to access different "versions" of a data item. When a transaction needs to read data, it reads a version that was valid at the start of the transaction. When it needs to write, it creates a new version of the data. This allows readers and writers to operate concurrently without blocking each other. 

### Concurrency Control in Distributed Databases
Distributed databases present additional challenges due to network latency and the potential for network partitions. A transaction in a distributed system might involve operations on data across multiple nodes. Key methods include:

* **Distributed Two-Phase Locking (2PL)**: This extends 2PL to a distributed environment. A distributed lock manager is used to coordinate locks across different nodes. A transaction must acquire locks on all the necessary data items at all sites before it can begin its shrinking phase. This is more complex and prone to deadlocks.

* **Distributed Optimistic Concurrency Control**: Similar to its single-node counterpart, transactions run without locks and validate at commit time. However, this validation must be coordinated across all participating nodes.

* **Timestamp Ordering**: This approach is similar to the single-node version but requires a globally synchronized clock or a logical clock to ensure consistent timestamps across all nodes. This helps to maintain a global ordering of transactions.

* **Two-Phase Commit (2PC)**: This is a protocol used to ensure atomicity for a transaction that spans multiple nodes. It involves a coordinator node and participant nodes.
    1.  **Phase 1 (Vote Phase)**: The coordinator sends a "prepare to commit" message to all participants. Each participant then prepares its part of the transaction and votes "yes" (if it's ready to commit) or "no" (if it cannot).
    2.  **Phase 2 (Commit Phase)**: If the coordinator receives "yes" votes from all participants, it sends a "commit" message. If it receives a "no" vote from even one participant, it sends an "abort" message.
