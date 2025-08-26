## **1. What is Apache Kafka?**
Apache Kafka is a distributed event streaming platform used to build real-time data pipelines and streaming applications. It was originally developed by LinkedIn and is now an open-source project maintained by the Apache Software Foundation.
3. **Kafka Use Cases**
4. **Kafka Architecture Overview**
   - Brokers
   - Topics
   - Partitions
   - Producers
   - Consumers
5. **Kafka Installation and Setup**
6. **Creating Topics**
7. **Producing and Consuming Messages**
8. **Kafka CLI Tools**

---

## 9. **Message Retention and Durability**

### What is Message Retention?
Kafka retains messages in topics for a configurable period, **regardless of whether they’ve been consumed**. This allows consumers to re-read messages or recover from failures.

#### Retention Configuration Options:
- **Time-Based Retention** (`retention.ms`):  
  Messages are retained for a specified duration (e.g., 7 days).
- **Size-Based Retention** (`retention.bytes`):  
  Messages are retained until the total size of the log reaches a threshold.

#### Log Segments:
- Kafka stores messages in **log segments**.
- Old segments are deleted based on retention policies.

#### Log Compaction:
- Kafka can also retain the **latest value for each key** using **log compaction**.
- Useful for stateful applications (e.g., user profiles, configs).

### **2. Kafka Durability**

#### What is Durability?
Durability ensures that once a message is written to Kafka, it **won’t be lost**, even if a broker crashes.

#### Replication:
- Kafka replicates partitions across multiple brokers.
- Each partition has:
  - **Leader**: Handles reads/writes.
  - **Followers**: Replicate data from the leader.

#### Acknowledgment Levels (`acks`):
- **acks=0**: No acknowledgment (fast, but risky).
- **acks=1**: Leader acknowledges after writing.
- **acks=all** (or `-1`): Leader waits for all replicas to acknowledge — **most durable**.

#### Write-Ahead Log:
- Kafka writes messages to disk before acknowledging.
- Ensures durability even in case of broker failure.

#### Best Practices
- Use **acks=all** for critical data.
- Set appropriate **retention.ms** based on business needs.
- Enable **log compaction** for key-value use cases.
- Monitor disk usage to avoid retention-related issues.
- Use **replication factor ≥ 3** for high availability.

---

10. **Basic Configuration Files (`server.properties`)**
11. **ZooKeeper Role in Kafka (pre-KRaft)**

---

## 🟡 **Intermediate Topics: Development & Integration**

### 🎯 Goal: Build applications using Kafka and integrate with other systems.

11. **Kafka Producer API**
12. **Kafka Consumer API**
13. **Consumer Groups and Offsets**
14. **Kafka Streams API (Intro)**
15. **Kafka Connect (Intro)**
16. **Serialization and Deserialization (Avro, JSON, Protobuf)**
17. **Kafka with Python (e.g., `confluent-kafka`, `kafka-python`)**
18. **Kafka with Java (native client)**
19. **Kafka REST Proxy**
20. **Kafka Integration with Databases (via Kafka Connect)**

---

## 🔵 **Advanced Topics: Performance & Reliability**

### 🎯 Goal: Optimize Kafka for production use.

21. **Kafka Partitioning Strategies**
22. **Replication and Fault Tolerance**
23. **High Availability and Failover**
24. **Kafka Security**
   - SSL/TLS
   - SASL
   - ACLs
25. **Monitoring Kafka (JMX, Prometheus, Grafana)**
26. **Kafka Metrics and Health Checks**
27. **Kafka Log Compaction vs Retention**
28. **Kafka Rebalancing and Lag Monitoring**
29. **Kafka Performance Tuning**
30. **Kafka Backup and Disaster Recovery**

---

## 🔴 **Expert Topics: Architecture & Ecosystem**

### 🎯 Goal: Design scalable, resilient, and real-time data platforms.

31. **Kafka Streams (Advanced)**
32. **Kafka Connect (Advanced)**
33. **Kafka KRaft Mode (Kafka without ZooKeeper)**
34. **Exactly-Once Semantics**
35. **Schema Registry and Data Governance**
36. **Kafka in Microservices Architecture**
37. **Kafka in Event-Driven Architecture**
38. **Kafka with Flink, Spark, and other stream processors**
39. **Multi-Cluster and Cross-Region Kafka**
40. **Real-World Kafka Use Cases (e.g., Uber, LinkedIn, Netflix)**

---

Would you like this roadmap turned into a **study plan**, or want help setting up a **Kafka project** (e.g., real-time analytics or event-driven microservices)?
