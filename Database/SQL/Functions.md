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
