### SCD Type 0: Retain Original

SCD Type 0 is the simplest method where no changes are allowed to the dimension table. Once a record is created, its attributes are considered static and are never updated. This approach is suitable for dimensions where the data is truly unchanging, such as a "Date" dimension.

| Pros                                       | Cons                                         |
|--------------------------------------------|----------------------------------------------|
| **Simple to implement** and maintain       | **Cannot track any changes** to the data     |
| **High performance** for queries           | Data can become outdated and inaccurate      |
| **Low storage cost** as data isn't duplicated | Not suitable for dimensions with changing attributes |

***

### SCD Type 1: Overwrite

SCD Type 1 handles changes by overwriting the existing data with new data. It retains only the most current information, and no history of past changes is preserved.

| Pros                                         | Cons                                             |
|----------------------------------------------|--------------------------------------------------|
| **Easy to implement** with a simple `UPDATE` statement | **Historical data is lost**, preventing trend analysis |
| **Space-efficient** as it doesn't create new rows      | Inability to audit or track changes over time      |
| **Fast query performance** since there's only one record per key | Not suitable for scenarios where historical data is critical |

***

### SCD Type 2: Add New Row

SCD Type 2 is a widely used method that preserves the full history of changes by adding a new row to the table for each change. It typically uses a surrogate key, and start and end dates to define the active period of each version of the record. 

| Pros                               | Cons                                             |
|------------------------------------|--------------------------------------------------|
| **Full historical record** is maintained | **Increased storage requirements** due to new rows |
| **Supports historical analysis** and trend reporting | **More complex ETL process** to manage new row inserts and existing row updates |
| Allows for accurate reporting of past and present states | Can lead to large dimension tables, which can impact query performance |

***

### SCD Type 3: Add New Column

SCD Type 3 is a method that tracks a limited history of changes by adding new columns to the dimension table. It typically stores the **current** and **previous** value of a specific attribute within the same row.

| Pros                                         | Cons                                                  |
|----------------------------------------------|-------------------------------------------------------|
| **Low storage overhead** compared to SCD Type 2 | **Only tracks a limited history** (usually just the previous value) |
| **Easy to query** for both current and previous values | Can become unwieldy if multiple attributes need history tracked, or if history beyond the immediate past is needed |
| **Simple implementation** and management     | Requires new columns for each attribute being tracked |

***

### SCD Type 4: Use a Historical Table

SCD Type 4 uses a separate historical table to store the history of changes. The main dimension table holds only the **current** version of the data (similar to SCD Type 1), while a secondary history table contains all the previous versions of the records.

| Pros                                         | Cons                                                     |
|----------------------------------------------|----------------------------------------------------------|
| **Main table stays small** and optimized for current data | **Requires two tables** to manage, increasing complexity of the data model |
| **Maintains full history** of changes      | **Queries for historical data require a join**, which can be slower |
| Ideal for dimensions with frequent changes | Can be challenging to manage the synchronization between the two tables |

***

### SCD Type 5: Mini-Dimension with Type 1 Outrigger

SCD Type 5 is a hybrid that combines SCD Type 4 and SCD Type 1. It uses a **mini-dimension** table to track the history of a rapidly changing attribute (Type 4), and it also includes an **outrigger** foreign key in the main dimension table. This outrigger is an SCD Type 1 column, meaning it is overwritten with the most current mini-dimension key. This allows for direct access to the current state without a join.

| Pros                                         | Cons                                                     |
|----------------------------------------------|----------------------------------------------------------|
| **Efficiently handles frequently changing attributes** | **Complex design** with multiple tables to manage |
| **Optimized for queries** that need the current state | **Limited historical context** for the frequently changing attribute |
| Reduces the size of the main dimension table | Can be difficult to maintain and understand the data model |

***

### SCD Type 6: Hybrid Approach

SCD Type 6 is a hybrid method that combines the techniques of SCD Type 1, 2, and 3. The name "Type 6" is a mnemonic derived from the sum of the types it combines ($1 + 2 + 3 = 6$). It uses a **single table** with columns for: the **current value** (Type 1), a **start and end date** for historical rows (Type 2), and a **previous value** column for a specific attribute (Type 3).

| Pros                                         | Cons                                                  |
|----------------------------------------------|-------------------------------------------------------|
| **Fast access to current data** in the same row | **Higher storage cost** than Type 1 or 3 |
| **Tracks a full history** with multiple versions of a record | **Complex to implement** and maintain the ETL logic |
| **Provides multiple ways to query** for current, previous, and historical data | Can lead to a wider table with many columns |

---

### SCD Type 0: Retain Original

SCD Type 0 is for attributes that **never change**. The data is loaded once and never updated.

#### **Initial Data**

| `CustomerID` | `CustomerName` | `DateOfBirth` |
|--------------|----------------|---------------|
| 101          | Alice          | 1980-05-15    |
| 102          | Bob            | 1991-08-20    |

*No change:* If Bob's date of birth was incorrectly entered and needs to be corrected to `1992-08-20`, an SCD Type 0 approach **would not allow this update**. The data remains as is.

---

### SCD Type 1: Overwrite

SCD Type 1 handles changes by **overwriting** the existing data. Historical data is lost.

#### **Initial Data**

| `CustomerID` | `CustomerName` | `State` |
|--------------|----------------|---------|
| 101          | Alice          | CA      |

#### **Update**

Alice moves from California (`CA`) to New York (`NY`). The original record is updated.

| `CustomerID` | `CustomerName` | `State` |
|--------------|----------------|---------|
| 101          | Alice          | **NY** |

---

### SCD Type 2: Add New Row

SCD Type 2 handles changes by **adding a new row** to the table. This preserves a complete history of all changes.

#### **Initial Data**

| `CustomerSK` | `CustomerID` | `CustomerName` | `State` | `StartDate`  | `EndDate`    |
|--------------|--------------|----------------|---------|--------------|--------------|
| 1            | 101          | Alice          | CA      | 2024-01-01   | 9999-12-31   |

#### **Update**

Alice moves from California (`CA`) to New York (`NY`) on 2024-06-15. The original record's `EndDate` is updated, and a new record is inserted for the new state.

| `CustomerSK` | `CustomerID` | `CustomerName` | `State` | `StartDate`  | `EndDate`    |
|--------------|--------------|----------------|---------|--------------|--------------|
| 1            | 101          | Alice          | CA      | 2024-01-01   | **2024-06-14** |
| **2** | 101          | Alice          | **NY** | **2024-06-15** | **9999-12-31** |


---

### SCD Type 3: Add New Column

SCD Type 3 tracks a **limited history** by adding columns for both the current and previous values of an attribute.

#### **Initial Data**

| `CustomerID` | `CustomerName` | `CurrentState` | `PreviousState` |
|--------------|----------------|----------------|-----------------|
| 101          | Alice          | CA             | NULL            |

#### **Update**

Alice moves from California (`CA`) to New York (`NY`). The `CurrentState` is updated, and the old value is moved to `PreviousState`.

| `CustomerID` | `CustomerName` | `CurrentState` | `PreviousState` |
|--------------|----------------|----------------|-----------------|
| 101          | Alice          | **NY** | **CA** |

---

### SCD Type 4: Use a Historical Table

SCD Type 4 separates the current and historical data into **two different tables**. The main dimension table (SCD Type 1) is used for current data, while a separate history table (SCD Type 2) stores all past versions.

#### **`DimCustomer` (Current Data Table)**

| `CustomerID` | `CustomerName` | `State` |
|--------------|----------------|---------|
| 101          | Alice          | **NY** |

#### **`CustomerHistory` (Historical Data Table)**

| `CustomerHistoryID` | `CustomerID` | `State` | `StartDate`  | `EndDate`    |
|---------------------|--------------|---------|--------------|--------------|
| 1                   | 101          | CA      | 2024-01-01   | 2024-06-14   |
| 2                   | 101          | NY      | 2024-06-15   | 9999-12-31   |

---

### SCD Type 5: Mini-Dimension with Type 1 Outrigger

SCD Type 5 is a hybrid approach. It uses a separate **mini-dimension** for frequently changing attributes, and the main dimension table has an **outrigger column** that holds a foreign key to the current mini-dimension record. The outrigger column is handled as an SCD Type 1, so it is overwritten with the latest key.

#### **`DimCustomer` (Main Table)**

| `CustomerID` | `CustomerName` | `StateID` |
|--------------|----------------|-----------|
| 101          | Alice          | **2** |

#### **`DimState` (Mini-Dimension Table)**

| `StateID` | `State` |
|-----------|---------|
| 1         | CA      |
| 2         | NY      |

In this example, when Alice moves to NY, the `StateID` in the main `DimCustomer` table is simply updated from `1` to `2`. Historical sales data can still be accurately tied to the state at the time of the sale, because the fact table links to the `StateID` which changes as a Type 1 attribute.

---

### SCD Type 6: Hybrid Approach

SCD Type 6 combines SCD Types 1, 2, and 3 in a **single table**. This provides a complete history, an easy way to get the current state, and the ability to see the immediate previous state for an attribute.

#### **Initial Data**

| `CustomerSK` | `CustomerID` | `CustomerName` | `CurrentState` | `PreviousState` | `StartDate`  | `EndDate`    |
|--------------|--------------|----------------|----------------|-----------------|--------------|--------------|
| 1            | 101          | Alice          | CA             | NULL            | 2024-01-01   | 9999-12-31   |

#### **Update**

Alice moves from California (`CA`) to New York (`NY`) on 2024-06-15.

| `CustomerSK` | `CustomerID` | `CustomerName` | `CurrentState` | `PreviousState` | `StartDate`  | `EndDate`    |
|--------------|--------------|----------------|----------------|-----------------|--------------|--------------|
| 1            | 101          | Alice          | **NY** | **CA** | 2024-01-01   | **2024-06-14** |
| **2** | 101          | Alice          | **NY** | **CA** | **2024-06-15** | **9999-12-31** |

In this example, the first row is expired with an `EndDate`, and a new row is created to represent the new state (Type 2). The new row also carries the `PreviousState` value (Type 3), and a column is updated to reflect the new `CurrentState` (Type 1).
