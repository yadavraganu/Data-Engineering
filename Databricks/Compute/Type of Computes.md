# **Overview of Databricks Compute on AWS**
Databricks offers various compute options to support data engineering, data science, and analytics workloads. These are categorized into:

#### **1. Serverless Compute**
- **Purpose**: Automatically managed compute that scales based on workload.
- **Use Cases**:
  - **Notebooks**: Interactive Python/SQL execution.
  - **Jobs**: Lakeflow Jobs without infrastructure setup.
  - **Pipelines**: Declarative Pipelines with auto-scaling.
- **Benefits**: No infrastructure management, automatic provisioning.
- **Limitations**: Certain configurations and workloads may not be supported.

#### **2. Classic Compute**
Provisioned and user-managed compute resources. Includes:

- **Standard Compute**:
  - **Multi-user access** with shared resources.
  - **Use Cases**: General ETL, collaborative data science, interactive exploration.
  - **Security**: Uses **Lakeguard** for user isolation.
  - **Language Support**: Python, SQL, Scala (13.3+), no R support.
  - **Default Mode**: Automatically selected unless specific runtimes are used.

- **Dedicated Compute**:
  - **Single-user or group access** for specialized workloads.
  - **Use Cases**: RDD APIs, GPU workloads, R language, privileged machine access, custom containers.
  - **Security**: Enhanced isolation and fine-grained access control.
  - **Requirements**: Databricks Runtime 15.4+ for advanced features.
- **Instance Pools**: Pre-configured instances to reduce startup time and cost.

#### **3. SQL Warehouses**
- Optimized for SQL queries and BI workloads.
- Available in both **serverless** and **classic** modes.

### **Additional Features**
- **Photon**: High-performance query engine for faster SQL execution.
- **Lakeguard**: Security framework for data governance and user isolation.
- **CLI & REST API**: For managing compute programmatically.
Would you like a visual diagram of these compute types or help choosing the right one for your workload?
