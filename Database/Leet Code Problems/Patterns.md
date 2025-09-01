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

# Indetify Consequtive Groups

### STEP 0: SAMPLE INPUT TABLE
```SQL
CREATE TABLE EVENTS (
    ID INT,
    STATUS CHAR(1)
);
INSERT INTO EVENTS (ID, STATUS) VALUES
(1, 'A'),
(2, 'A'),
(3, 'B'),
(4, 'B'),
(5, 'B'),
(6, 'C'),
(7, 'C'),
(8, 'B'),
(9, 'B');
```
### Step 1: Assign Row Numbers
```sql
WITH NUMBERED AS (
    SELECT *,
        ROW_NUMBER() OVER (ORDER BY ID) AS RN_ALL,         -- SEQUENTIAL ROW NUMBER
        ROW_NUMBER() OVER (PARTITION BY STATUS ORDER BY ID) AS RN_STATUS -- ROW NUMBER WITHIN EACH STATUS
    FROM EVENTS
)
```
**Output of `Numbered`:**
| id | status | rn_all | rn_status |
|----|--------|--------|-----------|
| 1  | A      | 1      | 1         |
| 2  | A      | 2      | 2         |
| 3  | B      | 3      | 1         |
| 4  | B      | 4      | 2         |
| 5  | B      | 5      | 3         |
| 6  | C      | 6      | 1         |
| 7  | C      | 7      | 2         |
| 8  | B      | 8      | 4         |
| 9  | B      | 9      | 5         |

### Step 2: Calculate Group Identifier

```sql
GROUPED AS (
    SELECT *,
        RN_ALL - RN_STATUS AS GRP  -- CONSTANT FOR CONSECUTIVE SAME-STATUS ROWS
    FROM NUMBERED
)
```
**Output of `Grouped`:**
| id | status | rn_all | rn_status | grp |
|----|--------|--------|-----------|-----|
| 1  | A      | 1      | 1         | 0   |
| 2  | A      | 2      | 2         | 0   |
| 3  | B      | 3      | 1         | 2   |
| 4  | B      | 4      | 2         | 2   |
| 5  | B      | 5      | 3         | 2   |
| 6  | C      | 6      | 1         | 5   |
| 7  | C      | 7      | 2         | 5   |
| 8  | B      | 8      | 4         | 4   |
| 9  | B      | 9      | 5         | 4   |

### Step 3: Count Consecutive Streaks

```sql
SELECT
    MIN(ID) AS START_ID,
    MAX(ID) AS END_ID,
    STATUS,
    COUNT(*) AS STREAK_LENGTH
FROM GROUPED
GROUP BY GRP, STATUS
ORDER BY MIN(ID);
```

**Final Output:**

| status | streak_length |
|--------|---------------|
| A      | 2             |
| B      | 3             |
| C      | 2             |
| B      | 2             |
