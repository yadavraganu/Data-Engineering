# Unity Catalog Components
<img width="1278" height="405" alt="unity" src="https://github.com/user-attachments/assets/adb17796-7285-4473-93ca-4a9dd80092ea" />


| **Component**           | **Description**                                                                 |
|-------------------------|---------------------------------------------------------------------------------|
| **Metastore**          | Top-level container for metadata and permissions; holds catalogs and governance objects. |
| **Catalog**            | Organizes data assets at the highest logical level (e.g., by business unit or environment). |
| **Schema**             | Logical grouping of tables, views, volumes, functions, and models.              |
| **Table**              | Structured data in rows and columns; can be managed or external.                |
| **View**               | Saved query on one or more tables.                                              |
| **Volume**             | Logical storage for non-tabular data (structured, semi-structured, unstructured). |
| **Function**           | User-defined function for reusable logic.                                       |
| **Model**              | ML model registered in Unity Catalog (via MLflow).                              |
| **Storage Credential** | Encapsulates cloud credentials for accessing storage.                           |
| **External Location**  | Combines storage path and credential for external tables or managed storage.    |
| **Connection**         | Credential for federated queries to external databases.                        |
| **Service Credential** | Credential for external services integration.                                   |
| **Share**              | Delta Sharing object representing read-only data assets.                       |
| **Recipient**          | Entity receiving a share.                                                      |
| **Provider**           | Entity providing a share.                                                      |
| **Clean Room**         | Secure collaboration environment without exposing raw data.                    |

# Volumes

- A **Volume** is a **Unity Catalog object** that provides **governance over non-tabular datasets** (files, images, logs, etc.).
- It represents a **logical storage container** in cloud object storage.
- Volumes allow you to **store, organize, and control access** to files in any format: structured, semi-structured, or unstructured.
- **Key difference:**  
  - **Tables** → For tabular data.  
  - **Volumes** → For path-based file access (cannot register files as tables)

### **Hierarchy Level**
- Volumes exist at the **third level** of the Unity Catalog namespace:  
  **`catalog.schema.volume`**
- Example path:  
  ```
  /Volumes/<catalog>/<schema>/<volume>/<path>/<file>
  ```
- They are **siblings to tables and views** under a schema
  
### **Types of Volumes**

1. **Managed Volume**  
   - Created inside the **managed storage location** of the schema.
   - No need to specify a location; UC manages paths.
   - Best for internal governed storage without external credentials.

2. **External Volume**  
   - Registered against a directory in an **external location** using UC-governed credentials.
   - UC does **not** manage file lifecycle; dropping the volume does not delete underlying data

### **Things Required to Set Up a Volume**
- **Unity Catalog-enabled workspace**.
- **Compute requirements:**  
  - SQL Warehouse or cluster with **Databricks Runtime 13.3 LTS or above**.
- **Privileges:**  
  - `CREATE VOLUME` on the schema.
  - `READ FILES` / `WRITE FILES` for file operations.
- **For external volumes:**  
  - **External location** and **storage credentials** configured in UC

### **How to Use Volumes**

- **Create a managed volume:**
  ```sql
  CREATE VOLUME myCatalog.mySchema.myManagedVolume COMMENT 'Managed volume example';
  ```
- **Create an external volume:**
  ```sql
  CREATE EXTERNAL VOLUME myCatalog.mySchema.myExternalVolume
  LOCATION 's3://my-bucket/my-path'
  COMMENT 'External volume example';
  ```
- **Access files:**
  ```sql
  LIST '/Volumes/myCatalog/mySchema/myManagedVolume';
  SELECT * FROM csv.`/Volumes/myCatalog/mySchema/myManagedVolume/sample.csv`;
  ```
- **Manage files:**  
  Use `PUT INTO`, `GET`, `REMOVE` commands or `dbutils.fs` for file operations
