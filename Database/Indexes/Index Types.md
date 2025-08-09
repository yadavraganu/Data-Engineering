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
