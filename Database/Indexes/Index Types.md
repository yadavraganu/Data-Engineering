# How Database Indexes Are Categorized

### 1. **By Logical Role**

| Category           | Description                                           | Example Use Case                     |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **Primary Index**   | Built on the primary key; enforces uniqueness         | `id` column in a user table          |
| **Secondary Index** | Built on non-primary columns; allows fast lookups    | `email`, `username`, `branch_code`   |
| **Unique Index**    | Ensures all values in the indexed column are unique  | `email`, `SSN`, `license_number`     |
| **Composite Index** | Index on multiple columns                            | `city + age`, `first_name + last_name` |

### 2. **By Physical Structure**

| Category           | Description                                           | Strengths                            |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **Dense Index**     | Every search key has an index entry                  | Fast lookups; more space             |
| **Sparse Index**    | Index entries for only some keys                     | Less space; slower lookups           |
| **Multilevel Index**| Index of indexes; hierarchical                       | Efficient for large datasets         |
| **Clustered Index** | Data rows sorted by index key                        | Fast range queries; only one allowed |
| **Non-clustered Index** | Separate structure with pointers to data         | Multiple allowed; flexible           |

### 3. **By Access Method / Engine Optimization**

| Category           | Description                                           | Best For                             |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **B-tree Index**    | Balanced tree; supports range and equality queries   | General-purpose queries              |
| **Hash Index**      | Uses hash function; fast for exact matches           | Key-value lookups                    |
| **Bitmap Index**    | Bitmaps for low-cardinality columns                  | OLAP, analytics                      |
| **Full-text Index** | Tokenizes text for search                            | Articles, logs, documents            |
| **Spatial Index**   | Optimized for geometric data                         | GIS, maps, coordinates               |
| **Function-based Index** | Indexes computed values                        | `LOWER(name)`, `ROUND(price)`        |

### 4. **By Storage Format / File Organization**

| Category           | Description                                           | Example                              |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **Sequential (Ordered)** | Sorted index values; dense or sparse           | Traditional B-tree indexes           |
| **Hashed File Organization** | Hash buckets for keys                     | Hash indexes                         |

### Summary

- **Logical role** helps you decide *what* you're indexing.
- **Physical structure** affects *how* it's stored and accessed.
- **Access method** determines *performance characteristics*.
- **Storage format** is more relevant for low-level DBMS internals.

# Bitmap Indexes

Bitmap indexes are a type of database index that uses a **bitmap** (a sequence of bits) to represent a row's presence for a specific key value. Unlike traditional B-tree indexes that store a list of row identifiers for each key, a bitmap index stores a bit for each row in the table. If the bit is set to 1, the row contains the key value; if it's 0, it doesn't.

### **Use Cases**

Bitmap indexes are most effective in situations where:

* **Low Cardinality Columns:** The indexed column has a small number of distinct values (e.g., gender: 'male', 'female'; status: 'active', 'inactive'; or a boolean flag). For example, a table of millions of customers could be efficiently queried for all 'female' customers using a bitmap index.
* **Ad-Hoc Queries and Data Warehousing:** They are ideal for complex, multi-column queries commonly found in data warehousing (OLAP) environments. The bitmaps for different conditions can be combined very quickly using bitwise logical operations (AND, OR, NOT). For example, to find all 'female' customers who are 'active' and live in 'California', the database can simply perform a bitwise AND operation on the bitmaps for each condition. 
* **Read-Heavy Environments:** They are optimized for fast reads and are generally not suitable for environments with frequent updates or inserts.

### **Avoidance**

Bitmap indexes should be avoided in scenarios characterized by:

* **High Cardinality Columns:** Columns with a large number of unique values (e.g., social security numbers, email addresses, or timestamps). For such columns, the bitmap would become very large and sparse (mostly zeros), leading to poor performance and excessive storage consumption.
* **Frequent Updates and Inserts:** When a row is updated or inserted, the corresponding bitmaps for all affected indexed columns must be modified. This can cause significant overhead and lock contention, as multiple sessions may need to acquire locks on the same bitmap, severely impacting performance in online transaction processing (OLTP) systems.

### Underlying Data Structure

The underlying data structure for a bitmap index is essentially a **series of bitmaps**, one for each distinct value in the indexed column.

For a column like `marital_status` with values `married`, `single`, and `divorced`, the index would consist of three bitmaps:

* A bitmap for `married`.
* A bitmap for `single`.
* A bitmap for `divorced`.

Each bitmap has a length equal to the number of rows in the table. The bit at a specific position (e.g., the 500th bit) corresponds to the 500th row in the table. If the 500th bit in the `married` bitmap is 1, it means the 500th row has `marital_status = 'married'`.

To manage and compress these bitmaps, database systems often use more sophisticated data structures. For instance, Oracle and other systems use **B-tree indexes** on the distinct values of the indexed column. The B-tree stores the distinct value (e.g., 'married') and a pointer to the associated compressed bitmap. This hybrid approach combines the fast lookup of a B-tree with the efficient bitwise operations of a bitmap.

A hash index uses a **hash function** to compute an address for a specific value, allowing for very fast, direct lookups. Instead of sorting data, it organizes it into "buckets" based on the hashed value of the indexed column. This makes retrieving a single record a nearly constant-time operation.

#  Hash Indexes
### Underlying Data Structure

The underlying data structure for a hash index is a **hash table** 📊. A hash table is an array of pointers to data. Each position in the array is called a "bucket." When a hash index is created, the database system applies a hash function to the values in the indexed column. This function produces a hash code, which is then used as the index to an array.

* **Hash Function**: This is a mathematical algorithm that takes the key (e.g., a `user_id` or `product_code`) and generates a fixed-size integer value, or hash code.
* **Buckets**: The hash table is an array where each index corresponds to a bucket. The hash code determines which bucket the data entry for a particular key will be stored in.
* **Collision Handling**: A hash collision occurs when two different keys produce the same hash code. Hash tables handle this using methods like **separate chaining** (storing a linked list of all records that hash to the same bucket) or **open addressing** (probing for the next available empty slot in the array).

The primary benefit of this structure is that it allows the database to go directly to the correct bucket, significantly reducing the amount of data it has to read to find the desired record.

### When to Use Hash Indexes

Hash indexes are ideal for scenarios where you need to perform **equality lookups** and a **high volume of read-heavy workloads**.

* **Exact Match Queries**: They are most effective for queries that use the `=` operator. For example, `SELECT * FROM users WHERE email = 'john.doe@example.com'`. The hash index can compute the hash of the email address and go directly to its location.
* **Primary Keys or Unique Constraints**: If you frequently search for records by their primary key, a hash index can provide very fast performance.
* **In-Memory Tables**: For database storage engines that keep data in memory (like MySQL's `MEMORY` engine), hash indexes can be extremely fast due to the lack of disk I/O.

### When to Avoid Hash Indexes

Hash indexes are not a good fit for every situation, especially when queries involve sorting or searching for ranges of values.

* **Range Queries**: Hash functions scatter data randomly across the hash table. This means there is no inherent order, making it impossible to perform queries with operators like `<`, `>`, `BETWEEN`, or `LIKE 'prefix%'`. For example, `SELECT * FROM products WHERE price > 50` would require a full table scan.
* **Sorting**: Hash indexes cannot be used to speed up `ORDER BY` clauses because the data is not stored in a sorted manner.
* **Hash Collisions**: If a poor hash function is used or the data has a highly uneven distribution, many keys might hash to the same bucket. This leads to long linked lists, degrading performance from a near-constant time lookup to a linear search within that list.
* **Large Datasets with Skewed Data**: While they are efficient for large datasets with uniformly distributed keys, if data is highly non-unique (e.g., a column with only a few distinct values), a hash index can become unbalanced and perform worse than other index types, like B-trees.

# B-Tree
B-tree indexes are a type of **self-balancing tree data structure** used by most database management systems (DBMS) like MySQL and PostgreSQL. The primary purpose of a B-tree index is to reduce the number of disk I/O operations required to find a specific piece of data, which is crucial for large datasets stored on a disk. They achieve this by organizing data in a hierarchical structure, ensuring that all leaf nodes are at the same depth, which guarantees efficient and consistent search, insertion, and deletion times.

### The Underlying Data Structure

The B-tree index itself is a tree-like structure composed of different types of nodes:

* **Root Node:** The top-most node of the tree, which contains pointers to the branch nodes.
* **Branch Nodes (or Internal Nodes):** These nodes are in between the root and the leaf nodes. They contain key values and pointers to other branch nodes or leaf nodes, directing the search toward the correct data.
* **Leaf Nodes:** These are the lowest level of the tree. They contain the actual index items, which are composed of a key value and a pointer to the physical location of the corresponding row in the database table.

A common variation, the **B+ tree**, is often used in practice. B+ trees store all data pointers only in the leaf nodes, while internal nodes only store keys. This allows for more keys to be stored in each internal node, creating a shorter and wider tree that requires fewer disk reads. Additionally, the leaf nodes in a B+ tree are linked together, which makes range queries (e.g., finding all values between X and Y) very efficient.

### Where to Use and Avoid B-tree Indexes

#### Use Cases

B-tree indexes are highly effective and should be used in the following scenarios:

* **Equality and Range Queries:** They are ideal for queries that use comparison operators like `=`, `>`, `>=`, `<`, `<=`, or `BETWEEN`. For example, `WHERE user_id = 123` or `WHERE order_date BETWEEN '2025-01-01' AND '2025-01-31'`.
* **Primary Keys and Foreign Keys:** They are the standard for columns used as primary keys or foreign keys because they enforce uniqueness and speed up joins between tables.
* **Prefix Searches:** They work well for `LIKE` queries that do not have a leading wildcard, such as `LIKE 'John%'`.
* **Ordering Data:** Queries with an `ORDER BY` clause on an indexed column can be executed much faster because the data is already stored in a sorted order within the index.

#### Scenarios to Avoid

While powerful, B-tree indexes are not a silver bullet. You should avoid them or consider alternatives in these situations:

* **High Write-Heavy Workloads:** Every time data is inserted, updated, or deleted, the B-tree index needs to be updated to maintain its balanced structure. This can introduce a performance overhead, so for tables with frequent writes and few reads, the overhead might outweigh the benefits.
* **Small Datasets:** For tables with only a few hundred or thousand rows, a full table scan may be faster or equally fast, and the storage overhead of the index isn't worth it.
* **Columns with Low Cardinality:** Columns with very few unique values (e.g., a "gender" column with values "Male," "Female," "Other") are not good candidates for a B-tree index. The index won't significantly narrow down the search, and a full table scan might be more efficient.
* **Searches with Leading Wildcards:** B-tree indexes are inefficient for `LIKE` queries that start with a wildcard, such as `LIKE '%smith'`. The index cannot be used to narrow the search, so the database will resort to a full table scan.

In these cases, other index types like **hash indexes** (for exact equality checks) or **full-text indexes** (for text searches with wildcards) may be more appropriate.
