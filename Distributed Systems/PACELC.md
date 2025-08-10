### What Is PACELC?

The **PACELC Theorem** was introduced by Daniel Abadi to address a major gap in the CAP Theorem:  
> CAP only considers trade-offs **during a network partition**, but what about when the system is functioning normally?

PACELC adds this missing dimension by introducing **latency (L)** as a trade-off against **consistency (C)** when there is **no partition (Else)**.

### Breaking Down the Acronym

| Component | Meaning                                                                 |
|-----------|-------------------------------------------------------------------------|
| **P**     | If there is a **Partition**, then...                                   |
| **A or C**| Choose between **Availability** or **Consistency**                     |
| **E**     | **Else**, when there is no partition...                                |
| **L or C**| Choose between **Latency** or **Consistency**                          |

So PACELC = **If Partition (P), then Availability (A) or Consistency (C); Else (E), Latency (L) or Consistency (C)**.

### PACELC Configurations

| Configuration | Partition Scenario | Else Scenario | Example Systems                |
|---------------|--------------------|----------------|-------------------------------|
| **PA/EL**     | Availability        | Latency        | DynamoDB, Cassandra           |
| **PA/EC**     | Availability        | Consistency    | Hazelcast (in-memory grid)    |
| **PC/EL**     | Consistency         | Latency        | Some custom eventual systems  |
| **PC/EC**     | Consistency         | Consistency    | HBase, traditional RDBMS      |

### Why PACELC Matters

- CAP only guides decisions **during failure**.
- PACELC helps design systems that are **optimized for performance and correctness** even when everything is working fine.
- It forces architects to think about **latency vs. consistency trade-offs** in normal operation.

### Example: E-Commerce Checkout System

Imagine a distributed checkout system:

- During a **network partition**, you must choose:
  - **Availability (PA)**: Allow orders to go through, risking double inventory allocation.
  - **Consistency (PC)**: Block orders until partition resolves, ensuring accurate stock.

- During **normal operation**, you must choose:
  - **Latency (EL)**: Respond quickly, possibly with slightly stale inventory.
  - **Consistency (EC)**: Ensure every read reflects the latest stock, even if it adds delay.
