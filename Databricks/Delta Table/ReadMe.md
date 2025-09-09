# What Are Deletion Vectors?

**Deletion vectors** are a **storage optimization feature** in **Delta Lake** tables on Databricks. They allow Spark to **logically delete or update rows** without rewriting entire Parquet files.

Instead of physically removing rows, deletion vectors **mark rows as deleted or modified**, and these changes are applied during read operations.

### Why Are Deletion Vectors Needed?

#### Without deletion vectors:
- A **DELETE**, **UPDATE**, or **MERGE** operation requires **rewriting the entire Parquet file** containing the affected row.
- This is **expensive**, especially for large datasets.

#### With deletion vectors:
- Spark **marks rows as deleted or changed**.
- No need to rewrite the whole file.
- Improves performance and reduces I/O.

### How Deletion Vectors Work

1. **Logical Modification**:
   - Rows are marked as deleted or updated in a separate metadata structure.
   - The original Parquet file remains unchanged.

2. **Read-Time Resolution**:
   - When reading the table, Spark applies the deletion vectors to filter out or modify rows.

3. **Physical Rewrite (Optional)**:
   - You can run commands like `OPTIMIZE`, `REORG TABLE ... APPLY (PURGE)`, or `VACUUM` to physically rewrite files and apply deletions.

4. **Photon Acceleration**:
   - Photon engine uses deletion vectors for **predictive I/O**, speeding up `DELETE`, `UPDATE`, and `MERGE` operations.

### Compatibility & Enablement

- Supported in **Databricks Runtime 12.2 LTS and above**.
- Recommended to use **Databricks Runtime 14.3 LTS or higher** for full optimization.
- Can be enabled via:
  ```sql
  CREATE TABLE ... TBLPROPERTIES ('delta.enableDeletionVectors' = true);
  ALTER TABLE ... SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);
  ```

### Limitations & Issues

1. **Protocol Upgrade**:
   - Enabling deletion vectors upgrades the table protocol.
   - Older Delta clients may not be able to read the table.

2. **Manifest Generation**:
   - You cannot generate manifest files unless you purge deletion vectors using `REORG TABLE ... APPLY (PURGE)`.

3. **Streaming & Materialized Views**:
   - Deletion vectors are **not enabled by default**.
   - Once enabled, they **cannot be removed**.

4. **UniForm Format**:
   - Not supported with deletion vectors.

5. **Concurrency**:
   - Supports **row-level concurrency** in Databricks Runtime 14.2+.

### Use Cases

- Large-scale **DELETE/UPDATE/MERGE** operations.
- **Time travel** and **audit** scenarios.
- **Streaming ingestion** with frequent updates.
