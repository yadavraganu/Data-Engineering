Time Travel allows you to access historical data (mutated or deleted) at any point within a defined retention window. Fail-Safe provides a non-configurable, 7-day emergency recovery window handled exclusively by Snowflake Support.

## 1. Core Architecture & Retention Windows

Snowflake physical data storage relies on immutable micro-partitions. When data is updated or deleted, the original micro-partitions are not modified; instead, new micro-partitions are written, and the old ones are preserved for Time Travel.

### The Storage Lifecycle

Once data is modified or dropped, it moves through a strict chronologic lifecycle before being permanently deleted:

```
[ Active State ] ---> [ Time Travel Window ] ---> [ Fail-Safe Window ] ---> [ Purged ]
 (Mutable Data)        (Configurable: 0-90 days)    (Strictly 7 days)

```
### Retention Capabilities by Table Type

| Table Type | Time Travel Allowed | Default Retention | Max Retention | Fail-Safe Duration |
| --- | --- | --- | --- | --- |
| **Standard (Permanent)** | Yes | 1 Day | 90 Days (Requires Enterprise+) | 7 Days (Automatic) |
| **Transient** | Yes | 1 Day | 1 Day | 0 Days (None) |
| **Temporary** | Yes | 1 Day | 1 Day | 0 Days (None) |

## 2. Parameter Inheritance Hierarchy (Higher Levels)

Time Travel parameters cascade downward through Snowflake's logical object hierarchy. A parameter set explicitly at a lower level always overrides a setting inherited from a higher level ("lowest level wins").

```
Account Level (Global defaults)
       └── Database Level (Overrides Account)
             └── Schema Level (Overrides Database)
                   └── Table Level (Overrides Schema)

```
### Setting Retention Windows at Higher Levels

```sql
-- 1. Account Level: Set global default for all new objects to 14 days
ALTER ACCOUNT SET DATA_RETENTION_TIME_IN_DAYS = 14;

-- 2. Database Level: Override the account default for an entire database
ALTER DATABASE prod_db SET DATA_RETENTION_TIME_IN_DAYS = 30;

-- 3. Schema Level: Set a short retention for a staging area to control costs
ALTER SCHEMA prod_db.staging SET DATA_RETENTION_TIME_IN_DAYS = 1;

-- 4. Table Level: Break inheritance to give a critical audit table max protection
ALTER TABLE prod_db.sales.financial_audit SET DATA_RETENTION_TIME_IN_DAYS = 90;

-- Revert a table back to inheriting its schema/database default configuration
ALTER TABLE prod_db.sales.financial_audit UNSET DATA_RETENTION_TIME_IN_DAYS;

```
## 3. Querying Historical Data (The `AT` | `BEFORE` Clauses)

You can select historical data from a table, view, or schema using three specific extensions to the `FROM` clause.

### Method 1: Using a Specific Timestamp

```sql
-- Query data exactly as it looked at a precise timestamp
SELECT * 
FROM prod_db.sales.orders 
  AT(TIMESTAMP => '2026-05-16 14:30:00'::TIMESTAMP_TZ);

```

### Method 2: Using a Time Offset (Relative Time)

```sql
-- Query data as it looked 30 minutes ago (-1800 seconds)
SELECT * 
FROM prod_db.sales.orders 
  AT(OFFSET => -1800);

```

### Method 3: Using a Statement ID (Query ID)

Useful if an unexpected or bad DML transaction occurred and you need to see the state of the data immediately *before* that query modified the table.

```sql
-- Find the rogue Query ID in the query history, then query the state BEFORE it executed
SELECT * 
FROM prod_db.sales.orders 
  BEFORE(STATEMENT => '01b45cd6-0000-1234-0000-000012345678');

```
## 4. Disaster Recovery & Restoration (Cloning & Undrop)

### Restoring Errant Subsets of Data

If a bad `UPDATE` or `DELETE` statement corrupts rows, you can rewrite the table using the `BEFORE` clause.

```sql
-- Re-create the table exactly as it was right before the bad statement
CREATE OR REPLACE TABLE prod_db.sales.orders AS
SELECT * FROM prod_db.sales.orders BEFORE(STATEMENT => '01b45cd6-0000-1234-0000-000012345678');

```
### Restoring Dropped Objects (`UNDROP`)

As long as the object was dropped within its retention window, it can be recovered completely intact with its underlying metadata.

```sql
UNDROP TABLE prod_db.sales.orders; -- Recover a dropped table
UNDROP SCHEMA prod_db.sales;       -- Recover an entire dropped schema
UNDROP DATABASE prod_db;           -- Recover an entire dropped database

```
### Historical Snapshots via Zero-Copy Cloning

```sql
-- Clone a production database as it looked 24 hours ago into a dev environment
CREATE DATABASE dev_db_snapshot 
  CLONE prod_db 
  AT(OFFSET => -86400);

```
## 5. Advanced Metadata Functions & Tracking

When managing complex objects or troubleshooting dropped objects, explicit tracking is essential.

### Explicitly Querying Dropped Object History

If an object has been dropped and recreated multiple times, `UNDROP` recovers the most recent instance. To view all past historical instances still residing within the Time Travel buffer, use:

```sql
-- View all history of tables including dropped instances and their unique IDs
SHOW TABLES HISTORY LIKE 'orders';

```
### Checking Active Settings and Parameter Origins

To determine if an object is using its own parameter configuration or inheriting it from a higher level, use `SHOW PARAMETERS`:

```sql
-- Check parameter origins for a specific database
SHOW PARAMETERS LIKE 'DATA_RETENTION_TIME_IN_DAYS' IN DATABASE prod_db;
-- Inspect the 'level' column in the output: 'ACCOUNT', 'DATABASE', etc.

-- Query information schema to check retention days across all tables in a catalog
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, RETENTION_TIME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';

```
## 6. Storage Metrics & Monitoring

Time Travel and Fail-Safe both contribute directly to physical storage costs. You can monitor the exact storage footprint split via system tables.

### Auditing Time Travel & Fail-Safe Costs

```sql
-- Query the global Account Usage schema to check storage costs across active, time travel, and fail-safe categories
SELECT 
    DATABASE_NAME,
    SCHEMA_NAME,
    TABLE_NAME,
    ACTIVE_BYTES / POWER(1024, 3) AS ACTIVE_STORAGE_GB,
    TIME_TRAVEL_BYTES / POWER(1024, 3) AS TIME_TRAVEL_STORAGE_GB,
    FAIL_SAFE_BYTES / POWER(1024, 3) AS FAIL_SAFE_STORAGE_GB
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE DELETED = 'FALSE'
ORDER BY TIME_TRAVEL_STORAGE_GB DESC;

```
## 7. Critical Operational Guardrails

- **The Fail-Safe Point of No Return:** Once configured `DATA_RETENTION_TIME_IN_DAYS` expires on a permanent table, historical data moves permanently to the **Fail-Safe** phase. Data in Fail-Safe *cannot* be queried via SQL statements or restored via `UNDROP`. Recovery out of Fail-Safe requires contacting Snowflake Support and can take several days.
- **Overwriting Objects (`CREATE OR REPLACE`):** Running a `CREATE OR REPLACE TABLE` command on an existing table drops the old table and builds a fresh, empty one. To recover data from an overwritten table, you must first run `DROP TABLE <name>;`, then call `UNDROP TABLE <name>;` to pull the previous instance back out of the Time Travel buffer.
- **Pipeline Dependencies (Streams):** If a stream is created on a table, the stream becomes stale if its transaction offset extends beyond the table's Time Travel retention window. Ensure your stream ingestion/consumption frequencies are tighter than your `DATA_RETENTION_TIME_IN_DAYS`.
