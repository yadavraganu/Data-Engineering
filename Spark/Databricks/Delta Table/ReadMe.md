## 1. Storage Layout & Internal Mechanics
Delta Lake transforms cloud object storage into an ACID-compliant transactional database by pairing raw data files with an immutable transaction log.
### The Transaction Log Structure
Every table operation (write, delete, optimize) writes a single JSON file to the log (`000000.json`, `000001.json`, etc.).
* **The Checkpoint Mechanism:** To prevent Spark from reading millions of JSON files to construct the current state of a table, Delta creates a compressed **Parquet checkpoint file every 10 commits** (e.g., `000010.checkpoint.parquet`). This checkpoint aggregates all previous metadata state into a single, quickly readable file.
* **File Statistics Ingestion:** When writing a Parquet file, Delta computes and stores column-level statistics (**minimum, maximum, and null counts**) directly in the JSON log file for the first 32 columns by default.

```text
your_table/
├── _delta_log/
│   ├── 00000000000000000000.json               <-- Commit 0: Schema, file additions
│   ├── 00000000000000000001.json               <-- Commit 1: Row mutations
│   ├── ...
│   ├── 00000000000000000010.json
│   └── 00000000000000000010.checkpoint.parquet <-- Aggregated state up to V10 (written every 10 commits)
├── deletion_vector_abcd-1234.bin               <-- Optional: Auxiliary bitmap row-delete flags
├── partition_date=2026-05-20/
│   ├── part-00000-data-block.c000.snappy.parquet
│   └── part-00001-data-block.c000.snappy.parquet
└── partition_date=2026-05-21/

```
### Data Skipping Mechanics
* **The Routine:** Spark queries the transaction log *first*. If your query filter falls entirely outside a file's min/max range, Spark skips that file entirely without making a storage API call.
* **Warning Pattern:** Monotonically increasing values (like auto-incrementing IDs or explicit timestamps) get highly optimized data skipping naturally. High-cardinality, randomly distributed string values do not—they require explicit layout optimization.
