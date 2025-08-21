## Deployment Types in Amazon Redshift

### 1. **Provisioned Clusters**
- Traditional deployment model.
- You choose node types (e.g., DC2, RA3), cluster size, and manage scaling manually.
- Best for predictable workloads and fine-grained control.

### 2. **Serverless Deployment**
- No need to manage clusters or nodes.
- Automatically scales based on query load.
- Ideal for unpredictable workloads, ad hoc analytics, or BI integrations.
- You pay per query or compute seconds used.

### 3. **Multi-AZ Deployment**
- Available for **RA3 node types**.
- Deploys compute resources across **multiple Availability Zones**.
- Ensures **high availability** and **zero Recovery Point Objective (RPO)**.
- SLA improves from 99.9% (Single-AZ) to **99.99%**.

### 4. **Redshift Spectrum**
- Not a standalone deployment, but an extension.
- Allows querying data directly from **Amazon S3** using Redshift SQL.
- Useful for **data lake integration** and **cost-effective storage**.

## Choosing the Right Model

| Deployment Type     | Best For                            | Scaling        | Cost Model         |
|---------------------|-------------------------------------|----------------|--------------------|
| Provisioned Cluster | Predictable, high-performance loads | Manual         | Hourly per node    |
| Serverless          | Ad hoc, bursty workloads            | Auto-scaling   | Per query/second   |
| Multi-AZ            | Mission-critical, HA environments   | Manual         | Same as RA3 pricing|
| Spectrum            | Lakehouse architecture              | N/A            | Based on S3 scans  |
