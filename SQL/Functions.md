### 📅 **Date and Time Functions in SQL Server vs MySQL**

#### 🕒 **1. Current Date and Time**

| Function | MySQL | SQL Server |
|---------|-------|------------|
| Current datetime | `SELECT NOW();` | `SELECT GETDATE();` |
| Current date only | `SELECT CURDATE();` | `SELECT CAST(GETDATE() AS DATE);` |
| Current time only | `SELECT CURTIME();` | `SELECT CAST(GETDATE() AS TIME);` |

#### 📆 **2. Extracting Date Parts**

| Part | MySQL | SQL Server |
|------|-------|------------|
| Year | `SELECT YEAR(hire_date) FROM employees;` | `SELECT YEAR(hire_date) FROM employees;` |
| Month | `SELECT MONTH(hire_date) FROM employees;` | `SELECT MONTH(hire_date) FROM employees;` |
| Day | `SELECT DAY(hire_date) FROM employees;` | `SELECT DAY(hire_date) FROM employees;` |
| Day of week | `SELECT DAYOFWEEK(hire_date) FROM employees;` | `SELECT DATEPART(WEEKDAY, hire_date) FROM employees;` |
| Day of year | `SELECT DAYOFYEAR(hire_date) FROM employees;` | `SELECT DATEPART(DAYOFYEAR, hire_date) FROM employees;` |
| Week number | `SELECT WEEK(hire_date) FROM employees;` | `SELECT DATEPART(WEEK, hire_date) FROM employees;` |
| Month name | `SELECT MONTHNAME(hire_date) FROM employees;` | `SELECT DATENAME(MONTH, hire_date) FROM employees;` |
| Weekday name | `SELECT DAYNAME(hire_date) FROM employees;` | `SELECT DATENAME(WEEKDAY, hire_date) FROM employees;` |

#### ➕ **3. Date Arithmetic**

| Operation | MySQL | SQL Server |
|-----------|-------|------------|
| Add days | `SELECT DATE_ADD(hire_date, INTERVAL 10 DAY) FROM employees;` | `SELECT DATEADD(DAY, 10, hire_date) FROM employees;` |
| Subtract days | `SELECT DATE_SUB(hire_date, INTERVAL 10 DAY) FROM employees;` | `SELECT DATEADD(DAY, -10, hire_date) FROM employees;` |
| Date difference (days) | `SELECT DATEDIFF(NOW(), hire_date) FROM employees;` | `SELECT DATEDIFF(DAY, hire_date, GETDATE()) FROM employees;` |

#### 🧮 **4. Formatting Dates**

| Function | MySQL | SQL Server |
|----------|-------|------------|
| Format date | `SELECT DATE_FORMAT(hire_date, '%Y-%m-%d') FROM employees;` | `SELECT FORMAT(hire_date, 'yyyy-MM-dd') FROM employees;` |

#### 📌 **5. Special Date Functions**

| Function | MySQL | SQL Server |
|----------|-------|------------|
| Last day of month | `SELECT LAST_DAY(hire_date) FROM employees;` | `SELECT EOMONTH(hire_date) FROM employees;` |
| Time difference | `SELECT TIMEDIFF('12:00:00', '08:30:00');` | `SELECT DATEDIFF(SECOND, '08:30:00', '12:00:00');` |
| Extract time | `SELECT TIME(hire_date) FROM employees;` | `SELECT CONVERT(TIME, hire_date) FROM employees;` |

#### ⏱️ **6. Unix Timestamp Functions**

| Function | MySQL | SQL Server |
|----------|-------|------------|
| Current Unix timestamp | `SELECT UNIX_TIMESTAMP();` | `SELECT DATEDIFF(SECOND, '1970-01-01', GETUTCDATE());` |
| Convert Unix to date | `SELECT FROM_UNIXTIME(1620000000);` | `SELECT DATEADD(SECOND, 1620000000, '1970-01-01');` |

# String Functions

### Get Length of a String

```sql
-- SQL Server
SELECT LEN('Hello'); -- Returns 5

-- MySQL
SELECT CHAR_LENGTH('Hello'); -- Returns 5
SELECT LENGTH('Hello'); -- Returns 5 (in bytes)

-- PostgreSQL
SELECT CHAR_LENGTH('Hello'); -- Returns 5
SELECT OCTET_LENGTH('Hello'); -- Returns 5 (in bytes)
```

### Extract Substrings

```sql
-- SQL Server
SELECT SUBSTRING('abcdef', 2, 3); -- Returns 'bcd'

-- MySQL
SELECT SUBSTRING('abcdef', 2, 3); -- Returns 'bcd'

-- PostgreSQL
SELECT SUBSTRING('abcdef' FROM 2 FOR 3); -- Returns 'bcd'
```

### Concatenate Strings

```sql
-- SQL Server
SELECT 'Hello' + 'World'; -- Returns 'HelloWorld'
SELECT CONCAT('Hello', 'World'); -- Returns 'HelloWorld'

-- MySQL
SELECT CONCAT('Hello', 'World'); -- Returns 'HelloWorld'

-- PostgreSQL
SELECT 'Hello' || 'World'; -- Returns 'HelloWorld'
SELECT CONCAT('Hello', 'World'); -- Returns 'HelloWorld'
```

### Trim Whitespace

```sql
-- SQL Server
SELECT LTRIM(RTRIM('  Hello  ')); -- Returns 'Hello'
SELECT TRIM('  Hello  '); -- SQL Server 2017+

-- MySQL
SELECT TRIM('  Hello  '); -- Returns 'Hello'

-- PostgreSQL
SELECT TRIM('  Hello  '); -- Returns 'Hello'
```

### Change Case

```sql
-- SQL Server
SELECT UPPER('hello'); -- Returns 'HELLO'
SELECT LOWER('HELLO'); -- Returns 'hello'

-- MySQL
SELECT UPPER('hello'); -- Returns 'HELLO'
SELECT LOWER('HELLO'); -- Returns 'hello'

-- PostgreSQL
SELECT UPPER('hello'); -- Returns 'HELLO'
SELECT LOWER('HELLO'); -- Returns 'hello'
SELECT INITCAP('hello world'); -- Returns 'Hello World'
```

### Replace Substrings

```sql
-- SQL Server
SELECT REPLACE('abcabc', 'a', 'x'); -- Returns 'xbcxbc'

-- MySQL
SELECT REPLACE('abcabc', 'a', 'x'); -- Returns 'xbcxbc'

-- PostgreSQL
SELECT REPLACE('abcabc', 'a', 'x'); -- Returns 'xbcxbc'
```

### Find Position of Substring

```sql
-- SQL Server
SELECT CHARINDEX('b', 'abc'); -- Returns 2

-- MySQL
SELECT INSTR('abc', 'b'); -- Returns 2
SELECT LOCATE('b', 'abc'); -- Returns 2

-- PostgreSQL
SELECT POSITION('b' IN 'abc'); -- Returns 2
```

### Repeat or Reverse Strings

```sql
-- SQL Server
SELECT REPLICATE('ab', 3); -- Returns 'ababab'
SELECT REVERSE('abc'); -- Returns 'cba'

-- MySQL
SELECT REPEAT('ab', 3); -- Returns 'ababab'
SELECT REVERSE('abc'); -- Returns 'cba'

-- PostgreSQL
SELECT REPEAT('ab', 3); -- Returns 'ababab'
SELECT REVERSE('abc'); -- Returns 'cba'
```

### Pad Strings

```sql
-- SQL Server
SELECT RIGHT('000' + '5', 3); -- Returns '005'

-- MySQL
SELECT LPAD('5', 3, '0'); -- Returns '005'
SELECT RPAD('5', 3, '0'); -- Returns '500'

-- PostgreSQL
SELECT LPAD('5', 3, '0'); -- Returns '005'
SELECT RPAD('5', 3, '0'); -- Returns '500'
```

### ASCII and Character Conversion

```sql
-- SQL Server
SELECT ASCII('A'); -- Returns 65
SELECT CHAR(65); -- Returns 'A'

-- MySQL
SELECT ASCII('A'); -- Returns 65
SELECT CHAR(65); -- Returns 'A'

-- PostgreSQL
SELECT ASCII('A'); -- Returns 65
SELECT CHR(65); -- Returns 'A'
```

### Regular Expression Matching

```sql
-- SQL Server
-- SQL Server doesn't support full regex in T-SQL, but you can use LIKE or CLR integration
SELECT CASE WHEN 'abc123' LIKE '[a-z]%[0-9]' THEN 'Match' ELSE 'No Match' END;

-- MySQL
SELECT 'abc123' REGEXP '^[a-z]+[0-9]+$'; -- Returns 1 (true)

-- PostgreSQL
SELECT 'abc123' ~ '^[a-z]+[0-9]+$'; -- Returns true
SELECT 'abc123' ~* 'ABC'; -- Case-insensitive match
```

### String Aggregation

```sql
-- SQL Server
SELECT STRING_AGG(name, ', ') FROM employees;

-- MySQL
SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM employees;

-- PostgreSQL
SELECT STRING_AGG(name, ', ') FROM employees;
```

### Split Strings

```sql
-- SQL Server
SELECT value FROM STRING_SPLIT('a,b,c', ',');

-- MySQL
-- No built-in split-to-rows; use custom function or JSON_TABLE (MySQL 8+)
SELECT JSON_TABLE('["a","b","c"]', '$[*]' COLUMNS(val VARCHAR(10) PATH '$')) AS t;

-- PostgreSQL
SELECT UNNEST(STRING_TO_ARRAY('a,b,c', ',')); -- Returns rows: 'a', 'b', 'c'
```

### Format Strings

```sql
-- SQL Server
SELECT FORMAT(GETDATE(), 'yyyy-MM-dd'); -- Returns formatted date

-- MySQL
SELECT FORMAT(1234567.89, 2); -- Returns '1,234,567.89'

-- PostgreSQL
SELECT FORMAT('Hello %s, you have %s messages', 'Anurag', 5); -- Returns 'Hello Anurag, you have 5 messages'
```

### Insert or Overlay Substrings

```sql
-- SQL Server
SELECT STUFF('abcdef', 2, 3, 'XYZ'); -- Returns 'aXYZef'

-- MySQL
SELECT INSERT('abcdef', 2, 3, 'XYZ'); -- Returns 'aXYZef'

-- PostgreSQL
SELECT OVERLAY('abcdef' PLACING 'XYZ' FROM 2 FOR 3); -- Returns 'aXYZef'
```

### Soundex and Phonetic Matching

```sql
-- SQL Server
SELECT SOUNDEX('Smith'); -- Returns 'S530'
SELECT DIFFERENCE('Smith', 'Smythe'); -- Returns 4 (max similarity)

-- MySQL
SELECT SOUNDEX('Smith'); -- Returns 'S530'

-- PostgreSQL
SELECT SOUNDEX('Smith'); -- Returns 'S530'
```
