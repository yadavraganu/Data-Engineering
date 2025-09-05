# Query Writing Best Practices

### Indexing
* **Use indexes wisely**: Create indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses. Indexes significantly speed up data retrieval by providing a quick lookup path to the data.
* **Avoid over-indexing**: Too many indexes can slow down data modification operations (`INSERT`, `UPDATE`, `DELETE`) because each index needs to be updated as well.
* **Understand composite indexes**: For queries that filter on multiple columns, a composite index (an index on two or more columns) can be more efficient than multiple single-column indexes. The order of columns in a composite index is crucial; it should match the order of columns in the query's `WHERE` clause.

### Query Structure
* **Select only necessary columns**: Instead of using `SELECT *`, specify the columns you need. This reduces the amount of data the database has to retrieve from the disk and send over the network.
* **Use `JOIN` instead of subqueries**: For filtering or combining data, a well-structured `JOIN` is often faster than a subquery. Subqueries can force the database to re-execute the inner query for each row of the outer query, which is inefficient.
* **Filter early and aggressively**: Place your most restrictive `WHERE` clauses first. This reduces the number of rows the database has to process for subsequent operations.
* **Use `EXISTS` over `IN` for subqueries**: When you are just checking for the existence of a row in a subquery, `EXISTS` is generally more efficient than `IN`, especially when the subquery returns a large result set.
* **Avoid functions on indexed columns in `WHERE` clauses**: Applying a function to a column in a `WHERE` clause can prevent the database from using an index on that column, forcing a full table scan.
    * **Bad**: `WHERE YEAR(order_date) = 2023`
    * **Good**: `WHERE order_date >= '2023-01-01' AND order_date < '2024-01-01'`

### CTE Vs Subquries

A **Common Table Expression (CTE)** is a named, temporary result set that you define with a `WITH` clause at the beginning of a query. A **subquery** is a nested `SELECT` statement that you write directly within another query's `WHERE`, `FROM`, or `HAVING` clause. 
The choice between the two often comes down to readability, reusability, and specific use cases.

#### Key Differences

| Feature | Common Table Expression (CTE) | Subquery |
| :--- | :--- | :--- |
| **Syntax** | Defined at the start of the query using `WITH`. | Nested inside the main query, often in parentheses. |
| **Readability** | Excellent. Breaks complex queries into logical, named steps. | Can be poor. Deeply nested subqueries become difficult to read and debug. |
| **Reusability** | A CTE can be referenced multiple times within the same query. | A subquery is inline and must be rewritten if needed elsewhere. |
| **Recursive Queries** | Supports recursion, allowing you to traverse hierarchical data. | Cannot be used for recursive queries. |

#### When to Use Which

* **Use a CTE when:**
    * You need to simplify a complex, multi-step query.
    * You have a result set that you need to reference more than once in the same query.
    * You are writing a recursive query (e.g., to find all managers above a given employee).
    * You want to improve the overall readability and maintainability of your code.
* **Use a subquery when:**
    * You are performing a simple, one-off task like filtering a `WHERE` clause based on an aggregated value.
    * The query is small and nesting it doesn't significantly hurt readability.
    * You are using it with operators like `IN` or `EXISTS` to filter the main query.

#### Performance Comparison

For simple, single-use queries, there is usually **no significant performance difference** between a CTE and a subquery. Modern database optimizers are sophisticated and will often generate the same execution plan for both. 

However, a CTE may offer a performance advantage in specific scenarios:

* **Caching/Materialization**: When a CTE is referenced multiple times, the query optimizer may choose to execute it once and cache or "materialize" the result set, which can be faster than re-executing a subquery multiple times.
* **Complex Logic**: For very complex queries with multiple joins and aggregations, a CTE can sometimes help the optimizer create a more efficient execution plan by providing it with a clearer, structured view of the query's steps.

Ultimately, the best practice is to **write for readability first** using CTEs, and then profile performance with tools like `EXPLAIN` to identify any bottlenecks. If a CTE is causing a performance issue, it may be more efficient to replace it with a temporary table.
