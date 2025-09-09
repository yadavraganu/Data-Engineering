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

# Delta Table Optimization Techniques

| Technique / Command        | Purpose                                                                 | Benefits                                                                 | When to Use                                                                 |
|---------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **OPTIMIZE**              | Compacts small files into larger ones                                   | Improves read performance, reduces file overhead                         | After frequent inserts, streaming, or batch loads                           |
| **OPTIMIZE ZORDER BY**    | Reorders data to cluster by specified columns                           | Speeds up filtering and range queries                                    | When queries frequently filter on specific columns                          |
| **VACUUM**                | Removes obsolete files no longer referenced                             | Reclaims storage, cleans up stale data                                   | Periodically, especially after deletes/updates                              |
| **Data Skipping**         | Automatically skips irrelevant files during query execution             | Reduces I/O and speeds up queries                                        | Enabled by default; works best with partitioning and Z-Ordering             |
| **Partitioning**          | Organizes data into directories based on column values                  | Improves query performance and parallelism                               | When data has natural grouping (e.g., by date, region)                      |
| **Delta Caching**         | Caches frequently read data in memory                                   | Speeds up repeated queries                                               | On Databricks clusters with caching enabled                                 |
| **Change Data Feed (CDF)**| Tracks row-level changes in Delta tables                                | Efficient incremental processing                                         | When consuming changes for downstream systems                               |
| **Auto Compaction**       | Automatically merges small files during write operations                | Reduces file count, improves performance                                 | Enabled via `spark.databricks.delta.autoCompact.enabled`                   |
| **Optimize Write**        | Writes fewer, larger files during ingestion                             | Reduces small file problem                                               | Enabled via `spark.databricks.delta.optimizeWrite.enabled`                 |
| **Schema Evolution**      | Automatically updates schema during writes                              | Simplifies ingestion pipeline                                            | When schema changes are expected                                            |
| **Retention Check Config**| Controls safety check for `VACUUM` retention duration                   | Allows aggressive cleanup                                                | Use with caution: `spark.databricks.delta.retentionDurationCheck.enabled`  |
| **Concurrency Control**   | Uses optimistic concurrency for transactions                            | Ensures ACID compliance                                                  | Always active in Delta Lake                                                 |
| **Time Travel**           | Access previous versions of data                                        | Enables debugging, auditing, rollback                                    | Use `VERSION AS OF` or `TIMESTAMP AS OF` in queries                         |
