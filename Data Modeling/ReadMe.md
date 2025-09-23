# What is Data Modeling?
Data modeling is the process of creating a visual representation of a system or database to show how data is stored, connected, and accessed. It’s a foundational step in designing databases and data systems, especially in data engineering, software development, and business intelligence.
### Why is Data Modeling Important?
- Ensures data consistency and quality
- Helps in understanding data requirements
- Improves communication between stakeholders (business and technical)
- Optimizes database performance and scalability

# Types of Data Models
[Go here](https://github.com/yadavraganu/Data-Engineering/blob/main/Data%20Modeling/Stages%20of%20Data%20Modeling.md)

# Entity-Relationship (ER) Modeling

# Normalization & Denormalization
[Go Here](https://github.com/yadavraganu/Data-Engineering/blob/main/Data%20Modeling/Normalization.md)

# Type of Keys
[Go Here](https://github.com/yadavraganu/Data-Engineering/blob/main/Data%20Modeling/Type%20of%20Keys.md)

# Data Types and Domains

In data modeling, **Data Types** and **Domains** are essential concepts that define the **structure, constraints, and validity** of the data stored in a database.
**Data types** define the kind of data that can be stored in a column. They help ensure **data integrity**, **optimize storage**, and **improve performance**.

#### Common Categories of Data Types

| **Category**     | **Examples**                          | **Purpose**                                      |
|------------------|----------------------------------------|--------------------------------------------------|
| **Numeric**       | `INT`, `BIGINT`, `FLOAT`, `DECIMAL`   | Store numbers (whole or decimal)                 |
| **Character/String** | `CHAR`, `VARCHAR`, `TEXT`              | Store text data                                  |
| **Date/Time**     | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | Store temporal data                              |
| **Boolean**       | `BOOLEAN`, `BIT`                      | Store true/false values                          |
| **Binary**        | `BLOB`, `VARBINARY`                   | Store binary data (e.g., images, files)          |
| **UUID**          | `UUID`                                | Store universally unique identifiers             |
| **JSON/XML**      | `JSON`, `XML`                         | Store structured data in semi-structured format  |

A **domain** defines the **permissible values** for a column. It can be thought of as a **constraint** or **rule** applied to a data type.

### Why Use Domains?
- Enforce **business rules**
- Ensure **data consistency**
- Simplify **validation logic**

#### Domain Examples

| **Domain Name**     | **Base Type** | **Constraint**                          | **Use Case**                        |
|---------------------|---------------|------------------------------------------|-------------------------------------|
| `EmailDomain`       | `VARCHAR(100)`| Must match email format                  | For `Email` column                  |
| `SalaryDomain`      | `DECIMAL`     | Must be > 0                              | For `Salary` column                 |
| `PhoneDomain`       | `VARCHAR(15)` | Must match phone number pattern          | For `Phone` column                  |
| `GenderDomain`      | `CHAR(1)`     | Must be 'M', 'F', or 'O'                 | For `Gender` column                 |
| `CountryCodeDomain` | `CHAR(2)`     | Must be in ISO country code list         | For `CountryCode` column           |

### Summary Table

| **Concept**   | **Definition**                                                                 | **Why Use It?**                                      | **Example**                        |
|---------------|----------------------------------------------------------------------------------|------------------------------------------------------|------------------------------------|
| **Data Type** | Defines the kind of data a column can store                                     | To ensure correct format and optimize storage        | `VARCHAR(100)`, `INT`, `DATE`      |
| **Domain**    | Defines the valid set of values for a column (rules/constraints)                | To enforce business rules and maintain data quality  | `Salary > 0`, `Gender in ('M','F')`|

- **Cardinality and Relationships**
- **Data Integrity and Referential Integrity**

---

## 🧠 **Advanced Data Modeling Concepts**
- **Dimensional Modeling**
  - Star Schema
  - Snowflake Schema
  - Galaxy Schema (Fact Constellation)
- **Fact and Dimension Tables**
- **Slowly Changing Dimensions (SCD Types 0–6)**
- **Surrogate Keys vs Natural Keys**
- **Hierarchies in Dimensions**
- **Bridge Tables**
- **Junk Dimensions**
- **Degenerate Dimensions**

---

## 🏗️ **Modeling for Data Warehousing**
- **Kimball vs Inmon Methodologies**
- **Data Vault Modeling**
  - Hubs, Links, Satellites
- **Operational Data Store (ODS)**
- **Staging Area Design**
- **ETL vs ELT Implications on Modeling**
- **Schema Evolution and Versioning**

---

## ⚙️ **Modeling for Big Data & NoSQL**
- **Schema-on-Read vs Schema-on-Write**
- **Modeling in Columnar Databases (e.g., Cassandra)**
- **Document Store Modeling (e.g., MongoDB)**
- **Key-Value Store Modeling**
- **Graph Data Modeling (e.g., Neo4j)**
- **Time-Series Data Modeling**

---

## 🧪 **Modeling for Analytics & ML**
- **Feature Store Design**
- **Modeling for Real-Time Analytics**
- **Aggregated vs Raw Data Models**
- **Data Lineage and Provenance**
- **Data Quality Dimensions in Modeling**

---

## 🛡️ **Governance, Security & Compliance**
- **Metadata Modeling**
- **Data Catalogs and Business Glossaries**
- **Data Classification Models**
- **Access Control Models**
- **GDPR/CCPA-Compliant Modeling**
- **Audit Trail Modeling**

---

## 🧰 **Tools & Techniques**
- **Modeling Tools**: ER/Studio, dbt, Lucidchart, SQL DBM, PowerDesigner
- **Version Control for Data Models**
- **Modeling in Cloud Data Warehouses**: Snowflake, BigQuery, Redshift
- **CI/CD for Data Models**

---

Would you like this list as a **mind map**, **PDF**, or broken down into a **learning roadmap** for self-study or team training?
