## Modeling by Structure/Purpose (The Methodologies)

These methodologies define the underlying structure and rules for how data is organized and related.

### Relational Modeling (OLTP)
* **Technique:** **Entity-Relationship (ER) Modeling** is the most common way to design this.
* **Structure:** Data is organized into two-dimensional **tables** (relations) of rows and columns. Relationships are established through **keys**.
* **Purpose:** To support **Online Transaction Processing (OLTP)** systems. The focus is on **minimizing redundancy** and ensuring **data integrity** through **Normalization** (e.g., 3NF), making it excellent for high-volume, real-time data updates.

### Dimensional Modeling (OLAP)
* **Structure:** Uses the **Star Schema** or **Snowflake Schema**. Data is separated into large **Fact Tables** (containing metrics) and smaller **Dimension Tables** (containing descriptive attributes).
* **Purpose:** To support **Online Analytical Processing (OLAP)** in Data Warehouses. The focus is on **fast query performance** for reporting and analytics, often by slightly **denormalizing** the data.

### Data Vault Modeling
* **Structure:** A hybrid approach using three main table types: **Hubs** (business keys), **Links** (relationships), and **Satellites** (descriptive attributes).
* **Purpose:** Designed for **agility, scalability, and historical tracking**. It handles frequent schema changes and integrates data from multiple sources easily, making it popular in large, complex enterprise data warehouses.

### Older/Specialized Models
* **Hierarchical Model:** Data is organized in a tree-like structure, with a strict one-to-many, parent-child relationship (used in early IBM systems).
* **Network Model:** An extension of the hierarchical model where a child can have multiple parents, allowing for more complex relationships.
* **Graph Model:** Uses **Nodes** (entities) and **Edges** (relationships) to represent data. Excellent for modeling complex, many-to-many relationships like social networks or logistics paths.
* **Object-Oriented Model:** Represents data and their relationships as "objects" which encapsulate both data and behavior, often used with object-oriented programming languages.