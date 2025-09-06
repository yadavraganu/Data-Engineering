````markdown name=ReadMe.md
# Easy

## [1050. Actors and Directors Who Cooperated At Least Three Times](https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times/description/)
**Official Description:**  
Write a SQL query for a report that provides the pairs (actor_id, director_id) where the actor has cooperated with the director at least three times.

**Table Schema:**
- `ActorDirector(actor_id, director_id, timestamp)`

**Sample Input/Output:**
Input:
| actor_id | director_id | timestamp |
|----------|-------------|----------|
| 1        | 1           | ...      |
| 1        | 1           | ...      |
| 1        | 1           | ...      |
| 2        | 1           | ...      |

Output:
| actor_id | director_id |
|----------|-------------|
| 1        | 1           |

**SQL Solution:**
```sql
SELECT ACTOR_ID, DIRECTOR_ID FROM ACTORDIRECTOR GROUP BY ACTOR_ID, DIRECTOR_ID HAVING COUNT(*) >= 3
```
---

## [1068. Product Sales Analysis I](https://leetcode.com/problems/product-sales-analysis-i/description/)
**Official Description:**  
Write a SQL query that reports the product_name, year, and price for each sale_id in the Sales table.

**Table Schema:**
- `Product(product_id, product_name)`
- `Sales(sale_id, product_id, year, price)`

**Sample Input/Output:**
Input:
| product_id | product_name |
|------------|--------------|
| 100        | Nokia        |
| 200        | Apple        |

| sale_id | product_id | year | price |
|---------|------------|------|-------|
| 1       | 100        | 2008 | 1000  |
| 2       | 200        | 2009 | 2000  |

Output:
| product_name | year | price |
|--------------|------|-------|
| Nokia        | 2008 | 1000  |
| Apple        | 2009 | 2000  |

**SQL Solution:**
```sql
SELECT
    P.PRODUCT_NAME,
    S.YEAR,
    S.PRICE
FROM
    SALES AS S
INNER JOIN
    PRODUCT AS P
ON
    S.PRODUCT_ID = P.PRODUCT_ID;
```
---

## [1069. Product Sales Analysis II](https://leetcode.com/problems/product-sales-analysis-ii/description/)
**Official Description:**  
Write a SQL query that reports the total quantity sold for every product_id.

**Table Schema:**
- `Sales(sale_id, product_id, year, quantity, price)`

**Sample Input/Output:**
Input:
| sale_id | product_id | year | quantity | price |
|---------|------------|------|----------|-------|
| 1       | 100        | 2008 | 10       | 1000  |
| 2       | 200        | 2009 | 5        | 2000  |

Output:
| product_id | total_quantity |
|------------|---------------|
| 100        | 10            |
| 200        | 5             |

**SQL Solution:**
```sql
SELECT
    PRODUCT_ID,
    SUM(QUANTITY) AS TOTAL_QUANTITY
FROM
    SALES
GROUP BY
    PRODUCT_ID;
```
---

## [1075. Project Employees I](https://leetcode.com/problems/project-employees-i/description/)
**Official Description:**  
Write a SQL query that reports the average experience years for each project.

**Table Schema:**
- `Project(project_id, employee_id)`
- `Employee(employee_id, experience_years)`

**Sample Input/Output:**
Input:
| project_id | employee_id |
|------------|-------------|
| 1          | 1           |
| 1          | 2           |

| employee_id | experience_years |
|-------------|------------------|
| 1           | 1                |
| 2           | 2                |

Output:
| project_id | average_years |
|------------|---------------|
| 1          | 1.5           |

**SQL Solution:**
```sql
SELECT
    P.PROJECT_ID,
    ROUND(AVG(E.EXPERIENCE_YEARS),2) AS AVERAGE_YEARS
FROM
    PROJECT AS P
INNER JOIN
    EMPLOYEE AS E
ON
    P.EMPLOYEE_ID = E.EMPLOYEE_ID
GROUP BY
    P.PROJECT_ID;
```
---

# ...

<!-- Continue with the rest of the problems using the same format: Title (with link), official description, table schema, sample input/output, and SQL solution. -->
````