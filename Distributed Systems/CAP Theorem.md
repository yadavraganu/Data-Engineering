### What Is the CAP Theorem?

The **CAP Theorem**, proposed by Eric Brewer and formally proven by Gilbert and Lynch, states that a distributed system can **only guarantee two out of the following three properties** at any given time:

| Property           | Meaning                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **Consistency (C)** | Every read receives the most recent write or an error.                  |
| **Availability (A)** | Every request receives a (non-error) response, without guarantee of the most recent write. |
| **Partition Tolerance (P)** | The system continues to operate despite arbitrary message loss or failure of part of the network. |

🔺 **Key Insight**: In the presence of a **network partition**, a system must choose between **Consistency** and **Availability**.

### Real-World Examples of CAP Trade-offs

#### 1. **CA (Consistency + Availability)** — No Partition Tolerance  
This is only possible in **non-distributed systems** or tightly coupled systems.

- **Example**: A single-node relational database like SQLite.
- **Behavior**: Always consistent and available, but if the node fails or network partitions occur, the system goes down.

#### 2. **CP (Consistency + Partition Tolerance)** — Sacrifices Availability  
System ensures data correctness even during partitions, but may reject requests.

- **Example**: **Google Docs offline editing**
- **Behavior**: You can edit a document offline (partitioned), but syncing waits until the network is restored to ensure consistency.

#### 3. **AP (Availability + Partition Tolerance)** — Sacrifices Consistency  
System remains responsive during partitions but may serve stale or divergent data.

- **Example**: **Social media feeds (Facebook, Instagram)**
- **Behavior**: You post something, but your friends might not see it immediately due to eventual consistency.

### Example Scenario: Banking System

Imagine a distributed banking system with replicas in Mumbai and Delhi.

- A user in Mumbai withdraws ₹500.
- Due to a network partition, Delhi’s replica doesn’t get the update immediately.
- If the system favors **Availability**, Delhi might still show the old balance (₹1000).
- If it favors **Consistency**, it might reject balance inquiries or withdrawals until the partition is resolved.

### Why It Matters

Understanding CAP helps engineers design systems based on their **business priorities**:

- **Financial systems** prioritize **Consistency**.
- **Social platforms** prioritize **Availability**.
- **IoT networks** often prioritize **Partition Tolerance**.
