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
