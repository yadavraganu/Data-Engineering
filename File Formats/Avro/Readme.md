An Avro file is a self-describing file format that stores data in a compact, row-based format. Its architecture is composed of a header followed by one or more data blocks. This structure makes Avro files highly portable and efficient for data storage and serialization.

## Header

The **header** is the first part of an Avro file and contains essential metadata about the file's contents. It includes:

* **Magic Number**: A four-byte sequence (`'O', 'b', 'j', 1`) that identifies the file as an Avro object container file.
* **Schema**: The JSON-formatted schema that defines the structure and types of the data stored in the file. This schema is crucial because it allows the file to be self-describing.
* **Codec**: The name of the compression codec used for the data blocks (e.g., `null`, `deflate`, `snappy`). If no codec is specified, the data is uncompressed.
* **Synchronization Marker**: A 16-byte random sequence that helps in splitting the file and validating data. This marker is also used to separate data blocks.

## Data Blocks

Following the header are one or more **data blocks**. Each data block consists of:

* **Number of Objects**: A long integer indicating how many data records are present in the block.
* **Serialized Objects**: The actual data records, serialized according to the schema defined in the header. The serialization is compact and binary, which is a key reason for Avro's efficiency.
* **Synchronization Marker**: A repetition of the 16-byte synchronization marker from the header. This marker signals the end of a data block and the beginning of the next one. It also enables readers to efficiently seek to different parts of the file and recover from corruption.

The data within each block is often compressed using the codec specified in the header, further reducing the file size. 
