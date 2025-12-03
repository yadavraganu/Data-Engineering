## Compression Algorithms in Big Data

| Algorithm | Compression Ratio | Speed | Splitable | Benefits | Drawbacks | Use Cases |
|----------|-------------------|-------|-----------|----------|-----------|-----------|
| **Gzip (DEFLATE)** | High | Slow | ❌ No | Excellent compression; widely supported | Slow decompression; not suitable for parallel processing | Archival storage, backups |
| **Snappy** | Moderate | Very Fast | ✅ Yes (in formats like Parquet, ORC) | Ideal for real-time and streaming; low CPU usage | Lower compression ratio | Kafka, Hadoop, Spark |
| **LZ4** | Moderate | Very Fast | ✅ Yes | Lightweight; fast compression/decompression | Slightly lower compression than Gzip | Columnar formats, Spark, real-time analytics |
| **Zstandard (Zstd)** | High (tunable) | Fast | ✅ Yes (with framing) | Tunable balance of speed and compression; modern and efficient | Newer; not supported everywhere | Balanced workloads, modern data lakes |
| **Brotli** | High | Moderate | ❌ No | Excellent for text and web data | Slower; limited Big Data adoption | Web compression, text-heavy datasets |
| **LZO** | Low to Moderate | Fast | ✅ Yes | Fast decompression; used in Hadoop | Lower compression ratio | Hadoop pipelines, intermediate data |

## Key Considerations

### Splitability
- **Splitable algorithms** allow distributed systems to process chunks of compressed files in parallel.
- **Non-splitable algorithms** require full decompression before processing, which can be a bottleneck.

### Trade-offs
- **Gzip** offers high compression but poor performance in distributed systems.
- **Snappy** and **LZ4** are preferred for speed and splitability.
- **Zstd** is gaining popularity for its tunable performance and splitability.

## Choosing the Right Algorithm

| Scenario | Recommended Algorithm |
|----------|------------------------|
| **Real-time streaming (Kafka, Spark)** | Snappy, LZ4 |
| **Archival storage** | Gzip, Zstd |
| **Distributed processing (Hadoop, Spark)** | LZ4, Snappy, Zstd |
| **Web/text compression** | Brotli |
| **Intermediate Hadoop data** | LZO |

### Compression Options in Parquet:

| Algorithm | Compression Ratio | Speed | Splitable | Use Case |
|----------|-------------------|-------|-----------|----------|
| **Snappy** | Moderate | Very Fast | ✅ Yes | Default in Parquet; ideal for fast analytics |
| **Gzip** | High | Slow | ❌ No | Archival storage; not ideal for distributed queries |
| **LZ4** | Moderate | Very Fast | ✅ Yes | Real-time analytics; good balance |
| **Zstd** | High (tunable) | Fast | ✅ Yes | Modern workloads; tunable performance |

### Trade-Offs in Practice:

- **Snappy** is preferred for **interactive queries** and **streaming** because it's fast and splitable.
- **Gzip** is used for **archival** where compression ratio matters more than speed.
- **Zstd** is gaining popularity for **data lakes** due to its tunable balance of speed and compression.
- **LZ4** is used in **real-time dashboards** where latency is critical.
