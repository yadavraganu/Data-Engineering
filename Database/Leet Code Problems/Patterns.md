# Change Null Values in a Table to the Previous Value
### Step 0: Original Input Table
```SQL
+----+----------+
| ID | DRINK    |
+----+----------+
| 3  | LATTE    |
| 1  | NULL     |
| 5  | NULL     |
| 2  | MOCHA    |
| 4  | NULL     |
| 6  | ESPRESSO |
| 7  | NULL     |
+----+----------+
```
No guaranteed order.So we’ll simulate one.
### Step 1: Assign Synthetic Row Order
```SQL
WITH ORDERED AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RK
  FROM COFFEESHOP
)
```
**Output:**
```SQL
+----+----------+----+
| ID | DRINK    | RK |
+----+----------+----+
| 3  | LATTE    | 1  |
| 1  | NULL     | 2  |
| 5  | NULL     | 3  |
| 2  | MOCHA    | 4  |
| 4  | NULL     | 5  |
| 6  | ESPRESSO | 6  |
| 7  | NULL     | 7  |
+----+----------+----+
```
### Step 2: Create Group ID Based on Non-Nulls

```SQL
GROUPED AS (
  SELECT *,
    SUM(CASE WHEN DRINK IS NOT NULL THEN 1 ELSE 0 END)
      OVER (ORDER BY RK) AS GRP
  FROM ORDERED
)
```
**Output:**
```SQL
+----+----------+----+-----+
| ID | DRINK    | RK | GRP |
+----+----------+----+-----+
| 3  | LATTE    | 1  | 1   |
| 1  | NULL     | 2  | 1   |
| 5  | NULL     | 3  | 1   |
| 2  | MOCHA    | 4  | 2   |
| 4  | NULL     | 5  | 2   |
| 6  | ESPRESSO | 6  | 3   |
| 7  | NULL     | 7  | 3   |
+----+----------+----+-----+
```
Here, `grp` increments only when a new non-null value appears. All rows in the same group will share the same last known non-null value.

### Step 3: Fill NULLs with Previous Non-Null Value
```SQL
SELECT 
  ID,
  MAX(DRINK) OVER (PARTITION BY GRP ORDER BY RK) AS DRINK
FROM GROUPED;
```
** Final Output:**

```SQL
+----+----------+
| ID | DRINK    |
+----+----------+
| 3  | LATTE    |
| 1  | LATTE    |
| 5  | LATTE    |
| 2  | MOCHA    |
| 4  | MOCHA    |
| 6  | ESPRESSO |
| 7  | ESPRESSO |
+----+----------+
```
