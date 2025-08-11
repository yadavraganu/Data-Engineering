## 1. Strong Consistency

**Definition**:  
Every read returns the **most recent write**, regardless of which node is queried. All nodes reflect the same state at all times.

**Guarantees**:
- Total ordering of operations.
- No stale reads.
- Immediate propagation of updates.

**How It Works**:
- Often implemented using consensus protocols like **Paxos** or **Raft**.
- Requires coordination between nodes before confirming a write.

**Example**:
- **Google Spanner** uses TrueTime to ensure strong consistency across global replicas.
- **Banking systems**: You withdraw ₹500, and your balance reflects it instantly across all branches.

**Trade-offs**:
- ✅ High correctness  
- ❌ Lower availability and higher latency  
- ❌ Complex coordination overhead

## 2. Eventual Consistency

**Definition**:  
If no new updates are made, all replicas will **eventually converge** to the same value.

**Guarantees**:
- Asynchronous propagation of updates.
- Temporary inconsistencies allowed.
- High availability and partition tolerance.

**How It Works**:
- Updates are propagated in the background.
- Conflict resolution strategies like **last-write-wins** or **vector clocks** are used.

**Example**:
- **Amazon DynamoDB**, **Cassandra**, **shopping carts** in e-commerce.
- You add an item to your cart; it may not appear immediately on all devices, but eventually it will.

**Trade-offs**:
- ✅ High availability and scalability  
- ❌ Temporary inconsistencies  
- ❌ Complex conflict resolution

## 3. Causal Consistency

**Definition**:  
Operations that are **causally related** (e.g., A causes B) are seen in the same order by all nodes. Unrelated operations may be seen in different orders.

**Guarantees**:
- Preserves cause-effect relationships.
- Partial ordering of events.
- More intuitive than eventual consistency.

**How It Works**:
- Uses **vector clocks** or **Lamport timestamps** to track causal dependencies.
- Ensures that if A → B, then all nodes see A before B.

**Example**:
- **Chat apps** like WhatsApp: If Alice sends a message and Bob replies, everyone sees Alice’s message before Bob’s.
- **MongoDB** and **AntidoteDB** support causal consistency.

**Trade-offs**:
- ✅ Preserves logical order  
- ✅ Better than eventual consistency for user experience  
- ❌ Requires metadata tracking  
- ❌ Slightly more overhead than eventual consistency

## Summary Comparison

| Model               | Consistency Level | Availability | Latency | Use Cases                          |
|---------------------|-------------------|--------------|---------|------------------------------------|
| **Strong Consistency** | Highest            | Low          | High     | Banking, real-time analytics       |
| **Eventual Consistency** | Lowest             | High         | Low      | Social media, shopping carts       |
| **Causal Consistency** | Medium             | Medium       | Medium   | Messaging apps, collaborative tools|
