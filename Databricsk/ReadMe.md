## Architecture
Databricks' architecture on AWS is a two-plane model that separates Databricks-managed services from customer-managed resources. This design provides a secure and scalable environment for data and AI workloads.

### The Two Planes: Control and Data
#### Control Plane
The Databricks **Control Plane** is fully managed by Databricks in its own AWS account. It hosts the backend services and user interface (UI) that you interact with. This includes:

* **Databricks Web Application:** The UI for managing notebooks, jobs, and clusters.
* **Metadata and Governance:** Components like Unity Catalog, which manages data access, governance, and lineage.
* **Job Scheduler and Cluster Manager:** These orchestrate the provisioning and termination of compute resources for your workloads.
* **APIs:** REST APIs for programmatic access and automation.
* **Notebooks and Workspace Assets:** Your code, dashboards, and other artifacts are stored here, encrypted at rest.

The control plane is responsible for the overall management and orchestration, but it does not process your data directly.

#### Data Plane
The **Data Plane** is where all the data processing and computation happens. In a Databricks on AWS architecture, the data plane is hosted within your own AWS account. This provides you with full control over the compute resources and data. The key components of the data plane are:

* **Compute Clusters:** These are groups of AWS EC2 instances that Databricks provisions to run your Apache Spark and other workloads. Databricks manages the lifecycle of these clusters, including auto-scaling and termination based on demand.
* **Data Storage:** Your data resides in your own AWS data lake, most commonly in **Amazon S3**. Databricks processes data directly from S3, which means your data never moves out of your AWS account. This design ensures data privacy and security. 

The data plane's isolation within your AWS account gives you control over networking, security, and resource management, while Databricks handles the complex management of the underlying compute engine.

### How Databricks Integrates with AWS
Databricks seamlessly integrates with various AWS services to build a complete data and AI platform. Key integrations include:

* **IAM Roles:** Databricks uses cross-account AWS IAM roles to securely launch compute resources in your AWS account and access your S3 data without requiring you to share credentials.
* **VPC:** You can deploy Databricks clusters within your own Amazon Virtual Private Cloud (VPC), providing network isolation and allowing you to connect to other AWS resources securely.
* **Amazon S3:** As mentioned, Amazon S3 is the primary storage layer for your data lake. Databricks leverages the open-source **Delta Lake** framework on top of S3 to provide features like ACID transactions, schema enforcement, and time travel.
* **Other AWS Services:** Databricks can connect to and leverage a wide range of AWS services, including Amazon Redshift for data warehousing, Amazon Kinesis for streaming data, and AWS Glue for metadata cataloging.
