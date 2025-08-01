## Architecture Diagram
Parquet is referred as columnar format in many books but internally it is like an hybrid format ( Combination of Row and Columnar ).
A Parquet file consists of a header followed by one or more blocks, terminated by a footer. The header contains only a 4-byte magic number, PAR1, that identifies the file as being in Parquet format, and all the file metadata is stored in the footer. The footer’s metadata includes the format version, the schema, any extra key-value pairs, and metadata for every block in the file. The final two fields in the footer are a 4-byte field encoding the length of the footer metadata, and the magic number again (PAR1).    
<img width="601" height="478" alt="image" src="https://github.com/user-attachments/assets/cb6cbca0-950e-4e01-9358-35583ec88a2b" />
<img width="305" height="213" alt="image" src="https://github.com/user-attachments/assets/9d52396e-e674-486d-8775-5db5cef48c50" />

Each block in a Parquet file stores one or more row groups, which is made up of column chunks containing the column data for those rows. The data for each column chunk is written in pages. Each page contains values from the same column, making a page a very good candidate for compression since the values are likely to be similar. The first level of compression is achieved through how the values are encoded. There are different encoding techniques ( Simple encoding, Run-Length encoding, Dictionary encoding, Bit Packing, Delta encoding.

Parquet file properties are set at write time. The properties listed below are appropriate if you are creating Parquet files from Map Reduce, Crunch, Pig, or Hive.  
<img width="610" height="250" alt="image" src="https://github.com/user-attachments/assets/16ee21ba-ca99-4ffa-99cf-d060eb7e894f" />

A page is the smallest unit of storage in a Parquet file, so retrieving an arbitrary row requires that the page containing the row be decompressed and decoded. Thus, for single-row lookups, it is more efficient to have smaller pages, so there are fewer values to read through before reaching the target value.

There are three types of metadata: file metadata, column (chunk) metadata and page header metadata.  
<img width="584" height="766" alt="image" src="https://github.com/user-attachments/assets/a3ef4f65-5086-4c86-ad4c-29c29cfd8fde" />

## Pros of Parquet:

- __Columnar Storage:__ Unlike row-based files, Parquet is columnar-oriented. This means it stores data by columns, which allows for more efficient disk I/O and compression. It reduces the amount of data transferred from disk to memory, leading to faster query performance.
- __Schema Evolution:__ Parquet supports complex nested data structures, and allows for schema evolution. This means that as the schema of your data evolves, Parquet can adapt to those changes.
- __Compression:__ Parquet has good compression and encoding schemes. It reduces the disk storage space and improves performance, especially for columnar data retrieval, which is a common case in data analytics.

## Cons of Parquet:

- __Write-heavy Workloads:__ Since Parquet performs column-wise compression and encoding, the cost of writing data can be high for write-heavy workloads.
- __Small Data Sets:__ Parquet may not be the best choice for small datasets because the advantages of its columnar storage model aren’t as pronounced.

