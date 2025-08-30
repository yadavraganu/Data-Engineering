## How Database Indexes Are Categorized

### 1. **By Logical Role**

| Category           | Description                                           | Example Use Case                     |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **Primary Index**   | Built on the primary key; enforces uniqueness         | `id` column in a user table          |
| **Secondary Index** | Built on non-primary columns; allows fast lookups    | `email`, `username`, `branch_code`   |
| **Unique Index**    | Ensures all values in the indexed column are unique  | `email`, `SSN`, `license_number`     |
| **Composite Index** | Index on multiple columns                            | `city + age`, `first_name + last_name` |

---

### 2. **By Physical Structure**

| Category           | Description                                           | Strengths                            |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **Dense Index**     | Every search key has an index entry                  | Fast lookups; more space             |
| **Sparse Index**    | Index entries for only some keys                     | Less space; slower lookups           |
| **Multilevel Index**| Index of indexes; hierarchical                       | Efficient for large datasets         |
| **Clustered Index** | Data rows sorted by index key                        | Fast range queries; only one allowed |
| **Non-clustered Index** | Separate structure with pointers to data         | Multiple allowed; flexible           |

---

### 3. **By Access Method / Engine Optimization**

| Category           | Description                                           | Best For                             |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **B-tree Index**    | Balanced tree; supports range and equality queries   | General-purpose queries              |
| **Hash Index**      | Uses hash function; fast for exact matches           | Key-value lookups                    |
| **Bitmap Index**    | Bitmaps for low-cardinality columns                  | OLAP, analytics                      |
| **Full-text Index** | Tokenizes text for search                            | Articles, logs, documents            |
| **Spatial Index**   | Optimized for geometric data                         | GIS, maps, coordinates               |
| **Function-based Index** | Indexes computed values                        | `LOWER(name)`, `ROUND(price)`        |

---

### 4. **By Storage Format / File Organization**

| Category           | Description                                           | Example                              |
|--------------------|-------------------------------------------------------|--------------------------------------|
| **Sequential (Ordered)** | Sorted index values; dense or sparse           | Traditional B-tree indexes           |
| **Hashed File Organization** | Hash buckets for keys                     | Hash indexes                         |

---

### Summary

- **Logical role** helps you decide *what* you're indexing.
- **Physical structure** affects *how* it's stored and accessed.
- **Access method** determines *performance characteristics*.
- **Storage format** is more relevant for low-level DBMS internals.

## Bitmap Indexes

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
