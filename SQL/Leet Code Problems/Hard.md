# [1097. Game Play Analysis V](https://leetcode.com/problems/game-play-analysis-v/)
#### Schema

Table: Activity

| Column Name  | Type  |
|--------------|-------|
| player_id    | int   |
| device_id    | int   |
| event_date   | date  |
| games_played | int   |

Primary key: (player_id, event_date)

#### Description

The Activity table records each time a player logs in and plays some games (possibly zero) before logging out on a given day using a specific device. A player’s install date is defined as their very first login day. Day one retention for an install date x is the fraction of players who installed on x and then logged back in on x + 1, rounded to two decimal places. You need to report, for each install date, the total number of installs and the day one retention. Return the result in any order.

#### Sample Input

Activity table:

| player_id | device_id | event_date | games_played |
|-----------|-----------|------------|--------------|
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-03-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-01 | 0            |
| 3         | 4         | 2016-07-03 | 5            |

#### Sample Output

| install_dt  | installs | Day1_retention |
|-------------|----------|----------------|
| 2016-03-01  | 2        | 0.50           |
| 2017-06-25  | 1        | 0.00           |

**Explanation:**  
- Players 1 and 3 installed on 2016-03-01, but only player 1 returned on 2016-03-02, so retention = 1 / 2 = 0.50.  
- Player 2 installed on 2017-06-25 and did not return on 2017-06-26, so retention = 0 / 1 = 0.00.

```sql
WITH  PLAYERTOINSTALLDATE AS (
    SELECT PLAYER_ID, MIN(EVENT_DATE) AS INSTALL_DT
    FROM ACTIVITY
    GROUP BY PLAYER_ID
)
SELECT 
    PLAYERTOINSTALLDATE.INSTALL_DT,
    COUNT(*) AS INSTALLS,
    ROUND(
        CAST(SUM(IIF(DATEDIFF(DAY, PLAYERTOINSTALLDATE.INSTALL_DT, ACTIVITY.EVENT_DATE) = 1, 1, 0)) AS FLOAT) / COUNT(*),
        2
    ) AS DAY1_RETENTION
FROM PLAYERTOINSTALLDATE
LEFT JOIN ACTIVITY
    ON PLAYERTOINSTALLDATE.PLAYER_ID = ACTIVITY.PLAYER_ID
    AND DATEDIFF(DAY, PLAYERTOINSTALLDATE.INSTALL_DT, ACTIVITY.EVENT_DATE) = 1
GROUP BY PLAYERTOINSTALLDATE.INSTALL_DT;
```

# [1127. User Purchase Platform](https://leetcode.com/problems/user-purchase-platform/)
#### Schema

Table: Spending

| Column Name | Type    |
|-------------|---------|
| user_id     | int     |
| spend_date  | date    |
| platform    | varchar |
| amount      | int     |

Primary key: (user_id, spend_date, platform)

#### Description

Given the Spending table, write an SQL query to find, for every spend_date and platform (desktop, mobile, both), the total amount spent and the number of unique users who spent on that platform on that day. If there is no user for a platform on a given day, the result should show 0 for total_amount and total_users.

#### Sample Input

| user_id | spend_date  | platform | amount |
|---------|-------------|----------|--------|
| 1       | 2022-01-01  | desktop  | 100    |
| 1       | 2022-01-01  | mobile   | 200    |
| 2       | 2022-01-01  | desktop  | 300    |
| 3       | 2022-01-02  | mobile   | 400    |

#### Sample Output

| spend_date  | platform | total_amount | total_users |
|-------------|----------|--------------|-------------|
| 2022-01-01  | desktop  | 400          | 2           |
| 2022-01-01  | mobile   | 200          | 1           |
| 2022-01-01  | both     | 300          | 1           |
| 2022-01-02  | desktop  | 0            | 0           |
| 2022-01-02  | mobile   | 400          | 1           |
| 2022-01-02  | both     | 0            | 0           |

**Explanation:**  
- On 2022-01-01, user 1 spent on both platforms, so he is counted for 'both', and also for desktop and mobile individually.

```sql
WITH USERTOAMOUNT AS (
    SELECT
        USER_ID,
        SPEND_DATE,
        CASE 
            WHEN COUNT(DISTINCT PLATFORM) = 2 THEN 'both'
            ELSE MAX(PLATFORM)
        END AS PLATFORM,
        SUM(AMOUNT) AS AMOUNT
    FROM SPENDING
    GROUP BY USER_ID, SPEND_DATE
),
DATEANDPLATFORMS AS (
    SELECT DISTINCT SPEND_DATE, 'desktop' AS PLATFORM FROM SPENDING
    UNION ALL
    SELECT DISTINCT SPEND_DATE, 'mobile' FROM SPENDING
    UNION ALL
    SELECT DISTINCT SPEND_DATE, 'both' FROM SPENDING
)
SELECT
    DP.SPEND_DATE,
    DP.PLATFORM,
    ISNULL(SUM(UA.AMOUNT), 0) AS TOTAL_AMOUNT,
    COUNT(DISTINCT UA.USER_ID) AS TOTAL_USERS
FROM DATEANDPLATFORMS DP
LEFT JOIN USERTOAMOUNT UA
    ON DP.SPEND_DATE = UA.SPEND_DATE AND DP.PLATFORM = UA.PLATFORM
GROUP BY DP.SPEND_DATE, DP.PLATFORM;
```

# [1159. Market Analysis II](https://leetcode.com/problems/market-analysis-ii/)
#### Schema

Table: Users

| Column Name    | Type    |
|----------------|---------|
| user_id        | int     |
| favorite_brand | varchar |

user_id is the primary key for this table.

Table: Orders

| Column Name | Type    |
|-------------|---------|
| order_id    | int     |
| order_date  | date    |
| item_id     | int     |
| seller_id   | int     |

order_id is the primary key for this table.

Table: Items

| Column Name | Type    |
|-------------|---------|
| item_id     | int     |
| item_brand  | varchar |

item_id is the primary key for this table.

#### Description

A seller's second sold item is the item they sold in their second earliest order. Write an SQL query to find whether the seller's favorite brand matches the brand of their second sold item. Return seller_id and 'yes' if their favorite brand matches, 'no' otherwise.

#### Sample Input

Users table:

| user_id | favorite_brand |
|---------|---------------|
| 1       | Lenovo        |
| 2       | Samsung       |

Orders table:

| order_id | order_date | item_id | seller_id |
|----------|------------|---------|-----------|
| 1        | 2020-01-01 | 2       | 1         |
| 2        | 2020-01-02 | 3       | 1         |
| 3        | 2020-01-02 | 4       | 2         |

Items table:

| item_id | item_brand |
|---------|------------|
| 2       | Lenovo     |
| 3       | Samsung    |
| 4       | Samsung    |

#### Sample Output

| seller_id | second_item_fav_brand |
|-----------|----------------------|
| 1         | no                   |
| 2         | yes                  |

**Explanation:**  
- Seller 1's second item is item 3 (Samsung), favorite is Lenovo → "no"
- Seller 2's second item is item 4 (Samsung), favorite is Samsung → "yes"

```sql
-- Rank each seller's orders by order_date
WITH RANKEDORDERS AS (
    SELECT
        ORDER_DATE,
        ITEM_ID,
        SELLER_ID,
        RANK() OVER (
            PARTITION BY SELLER_ID
            ORDER BY ORDER_DATE
        ) AS RK
    FROM ORDERS
)

-- Join users with their second sold item and compare brands
SELECT
    U.USER_ID AS SELLER_ID,
    CASE
        WHEN U.FAVORITE_BRAND = I.ITEM_BRAND THEN 'yes'
        ELSE 'no'
    END AS SECOND_ITEM_FAV_BRAND
FROM USERS AS U
LEFT JOIN RANKEDORDERS AS O
    ON U.USER_ID = O.SELLER_ID AND O.RK = 2
LEFT JOIN ITEMS AS I
    ON O.ITEM_ID = I.ITEM_ID;
```

# [1194. Tournament Winners](https://leetcode.com/problems/tournament-winners/)
#### Schema

Table: Players

| Column Name | Type |
|-------------|------|
| player_id   | int  |
| group_id    | int  |

player_id is the primary key for this table.

Table: Matches

| Column Name   | Type |
|---------------|------|
| match_id      | int  |
| first_player  | int  |
| second_player | int  |
| first_score   | int  |
| second_score  | int  |

match_id is the primary key for this table.

#### Description

Given the results of matches in a tournament, find the player(s) with the highest total score in each group.

#### Sample Input

Players table:

| player_id | group_id |
|-----------|----------|
| 15        | 1        |
| 25        | 1        |
| 30        | 1        |
| 45        | 2        |
| 50        | 2        |
| 60        | 2        |

Matches table:

| match_id | first_player | second_player | first_score | second_score |
|----------|-------------|--------------|-------------|--------------|
| 1        | 15          | 45           | 3           | 5            |
| 2        | 30          | 60           | 2           | 6            |
| 3        | 15          | 60           | 7           | 0            |
| 4        | 25          | 45           | 1           | 2            |
| 5        | 30          | 25           | 5           | 5            |

#### Sample Output

| group_id | player_id |
|----------|-----------|
| 1        | 15        |
| 2        | 45        |
| 2        | 60        |

**Explanation:**  
- Group 1: 15 (3+7=10), 25 (1+5=6), 30 (2+5=7) → 15 wins  
- Group 2: 45 (5+2=7), 50 (0), 60 (6+0=6) → 45 and 60 tie


```sql
-- CTE TO GATHER ALL SCORES FOR EACH PLAYER (AS FIRST OR SECOND PLAYER)
WITH PLAYERTOSCORE AS (
    SELECT 
        P.PLAYER_ID, 
        P.GROUP_ID, 
        M.FIRST_SCORE AS SCORE
    FROM PLAYERS P
    LEFT JOIN MATCHES M ON P.PLAYER_ID = M.FIRST_PLAYER

    UNION ALL

    SELECT 
        P.PLAYER_ID, 
        P.GROUP_ID, 
        M.SECOND_SCORE AS SCORE
    FROM PLAYERS P
    LEFT JOIN MATCHES M ON P.PLAYER_ID = M.SECOND_PLAYER
),

-- CTE TO RANK PLAYERS BY TOTAL SCORE WITHIN EACH GROUP
RANKEDPLAYERS AS (
    SELECT 
        PLAYER_ID, 
        GROUP_ID,
        RANK() OVER (
            PARTITION BY GROUP_ID 
            ORDER BY SUM(SCORE) DESC, PLAYER_ID
        ) AS RANK
    FROM PLAYERTOSCORE
    GROUP BY PLAYER_ID, GROUP_ID
)

-- SELECT TOP-RANKED PLAYER(S) FROM EACH GROUP
SELECT 
    GROUP_ID, 
    PLAYER_ID
FROM RANKEDPLAYERS
WHERE RANK = 1;
```

# [1225. Report Contiguous Dates](https://leetcode.com/problems/report-contiguous-dates/)
#### Schema

Table: Failed

| Column Name | Type    |
|-------------|---------|
| fail_date   | date    |

fail_date is the primary key for this table.

Table: Succeeded

| Column Name   | Type    |
|---------------|---------|
| success_date  | date    |

success_date is the primary key for this table.

#### Description

Given two tables Failed and Succeeded, each with dates in 2019 when a process failed or succeeded, report every contiguous period of days where the process had the same status (either succeeded or failed).

#### Sample Input

Failed table:

| fail_date   |
|-------------|
| 2019-01-01  |
| 2019-01-02  |
| 2019-01-03  |
| 2019-01-07  |
| 2019-01-08  |

Succeeded table:

| success_date |
|--------------|
| 2019-01-04   |
| 2019-01-05   |
| 2019-01-06   |
| 2019-01-09   |

#### Sample Output

| period_state | start_date | end_date   |
|--------------|------------|------------|
| failed       | 2019-01-01 | 2019-01-03 |
| succeeded    | 2019-01-04 | 2019-01-06 |
| failed       | 2019-01-07 | 2019-01-08 |
| succeeded    | 2019-01-09 | 2019-01-09 |

**Explanation:**  
- 2019-01-01 to 2019-01-03: failed  
- 2019-01-04 to 2019-01-06: succeeded  
- 2019-01-07 to 2019-01-08: failed  
- 2019-01-09: succeeded

```sql
-- COMBINE FAILED AND SUCCEEDED DATES WITH STATUS
WITH COMBINED AS (
    SELECT FAIL_DATE AS DT, 'failed' AS ST FROM FAILED WHERE YEAR(FAIL_DATE) = 2019
    UNION ALL
    SELECT SUCCESS_DATE AS DT, 'succeeded' AS ST FROM SUCCEEDED WHERE YEAR(SUCCESS_DATE) = 2019
),

-- ASSIGN RANK TO EACH DATE PER STATUS
RANKED AS (
    SELECT 
        DT, 
        ST,
        RANK() OVER (PARTITION BY ST ORDER BY DT) AS RK
    FROM COMBINED
),

-- CREATE GROUP IDENTIFIER BY SUBTRACTING RANK FROM DATE
GROUPED AS (
    SELECT 
        DT, 
        ST, 
        DATEADD(DAY, -RK, DT) AS GRP
    FROM RANKED
)

-- GROUP BY STATUS AND GROUP IDENTIFIER TO GET CONTIGUOUS RANGES
SELECT 
    ST AS PERIOD_STATE,
    MIN(DT) AS START_DATE,
    MAX(DT) AS END_DATE
FROM GROUPED
GROUP BY ST, GRP
ORDER BY START_DATE;
```

# [1336. Number of Transactions per Visit](https://leetcode.com/problems/number-of-transactions-per-visit/)
#### Schema

Table: Visits

| Column Name  | Type |
|--------------|------|
| user_id      | int  |
| visit_date   | date |

Primary key: (user_id, visit_date)

Table: Transactions

| Column Name      | Type |
|------------------|------|
| user_id          | int  |
| transaction_date | date |

Primary key: (user_id, transaction_date)

#### Description

For each possible number of transactions (including zero), report how many visits had that many transactions. Return the result ordered by transactions_count.

#### Sample Input

Visits table:

| user_id | visit_date  |
|---------|-------------|
| 1       | 2020-01-01  |
| 2       | 2020-01-01  |
| 3       | 2020-01-01  |
| 4       | 2020-01-01  |

Transactions table:

| user_id | transaction_date |
|---------|-----------------|
| 1       | 2020-01-01      |
| 2       | 2020-01-01      |
| 2       | 2020-01-01      |
| 3       | 2020-01-01      |

#### Sample Output

| transactions_count | visits_count |
|--------------------|-------------|
| 0                  | 1           |
| 1                  | 2           |
| 2                  | 1           |

**Explanation:**  
- User 4 had 0 transactions, users 1 and 3 had 1, user 2 had 2.

```sql
-- GENERATE SEQUENCE FROM 0 TO MAX TRANSACTIONS PER VISIT
WITH S AS (
    SELECT 0 AS N
    UNION ALL
    SELECT N + 1
    FROM S
    WHERE N < (
        SELECT MAX(CNT)
        FROM (
            SELECT COUNT(*) AS CNT
            FROM TRANSACTIONS
            GROUP BY USER_ID, TRANSACTION_DATE
        ) AS T
    )
),

-- COUNT TRANSACTIONS PER VISIT (INCLUDE VISITS WITH 0 TRANSACTIONS)
T AS (
    SELECT 
        V.USER_ID, 
        V.VISIT_DATE, 
        ISNULL(T.CNT, 0) AS CNT
    FROM VISITS V
    LEFT JOIN (
        SELECT 
            USER_ID, 
            TRANSACTION_DATE, 
            COUNT(*) AS CNT
        FROM TRANSACTIONS
        GROUP BY USER_ID, TRANSACTION_DATE
    ) T ON V.USER_ID = T.USER_ID AND V.VISIT_DATE = T.TRANSACTION_DATE
)

-- JOIN GENERATED COUNTS WITH ACTUAL VISIT DATA
SELECT 
    S.N AS TRANSACTIONS_COUNT, 
    COUNT(T.USER_ID) AS VISITS_COUNT
FROM S
LEFT JOIN T ON S.N = T.CNT
GROUP BY S.N
ORDER BY S.N;
```

# [1369. Get the Second Most Recent Activity](https://leetcode.com/problems/get-the-second-most-recent-activity/)
#### Schema

Table: UserActivity

| Column Name  | Type    |
|--------------|---------|
| username     | varchar |
| activity     | varchar |
| startDate    | date    |
| endDate      | date    |

Primary key: (username, startDate)

#### Description

Write an SQL query to find the second most recent activity of each user. If there is only one activity for a user, return that activity.

#### Sample Input

| username | activity    | startDate  | endDate    |
|----------|-------------|------------|------------|
| Alice    | Travel      | 2020-02-12 | 2020-02-20 |
| Alice    | Dancing     | 2020-02-21 | 2020-02-23 |
| Bob      | Travel      | 2020-02-12 | 2020-02-20 |

#### Sample Output

| username | activity | startDate  | endDate    |
|----------|----------|------------|------------|
| Alice    | Travel   | 2020-02-12 | 2020-02-20 |
| Bob      | Travel   | 2020-02-12 | 2020-02-20 |

**Explanation:**  
- Alice has two activities, the second most recent is "Travel".
- Bob only has one activity, so it is returned.


```sql
SELECT
    USERNAME,
    ACTIVITY,
    STARTDATE,
    ENDDATE
FROM
(
    SELECT
        *,
        -- RANK ACTIVITIES PER USER BY STARTDATE (LATEST FIRST)
        RANK() OVER (
            PARTITION BY USERNAME
            ORDER BY STARTDATE DESC
        ) AS RK,

        -- COUNT TOTAL ACTIVITIES PER USER
        COUNT(USERNAME) OVER (
            PARTITION BY USERNAME
        ) AS CNT
    FROM USERACTIVITY
) AS A
-- GET SECOND LATEST ACTIVITY OR ONLY ACTIVITY IF USER HAS ONE
WHERE A.RK = 2 OR A.CNT = 1;
```

# [1384. Total Sales Amount by Year](https://leetcode.com/problems/total-sales-amount-by-year/)
```sql
-- DEFINE CALENDAR YEARS WITH START AND END DATES
WITH CALENDAR AS (
    SELECT '2018' AS YEAR, CAST('2018-01-01' AS DATE) AS START_DATE, CAST('2018-12-31' AS DATE) AS END_DATE
    UNION ALL
    SELECT '2019', '2019-01-01', '2019-12-31'
    UNION ALL
    SELECT '2020', '2020-01-01', '2020-12-31'
)

-- CALCULATE TOTAL SALES PER PRODUCT PER YEAR BASED ON OVERLAPPING DAYS
SELECT
    P.PRODUCT_ID,
    P.PRODUCT_NAME,
    C.YEAR AS REPORT_YEAR,

    -- OVERLAPPING DAYS × AVERAGE DAILY SALES
    (DATEDIFF(
        DAY,
        CASE WHEN S.PERIOD_START > C.START_DATE THEN S.PERIOD_START ELSE C.START_DATE END,
        CASE WHEN S.PERIOD_END < C.END_DATE THEN S.PERIOD_END ELSE C.END_DATE END
    ) + 1) * S.AVERAGE_DAILY_SALES AS TOTAL_AMOUNT

FROM SALES S
INNER JOIN CALENDAR C
    ON YEAR(S.PERIOD_START) <= CAST(C.YEAR AS INT)
    AND YEAR(S.PERIOD_END) >= CAST(C.YEAR AS INT)
INNER JOIN PRODUCT P
    ON P.PRODUCT_ID = S.PRODUCT_ID
ORDER BY P.PRODUCT_ID, C.YEAR;
```

# [1412. Find the Quiet Students in All Exams](https://leetcode.com/problems/find-the-quiet-students-in-all-exams/)
A **"quiet" student** is the one who took **at least one exam** and **didn't score** neither the **high score** nor the **low score**.

Write an SQL query to report the students (`student_id`, `student_name`) being **"quiet" in ALL exams**.

- Don't return the student who has **never taken any exam**.  
- Return the result table **ordered by student_id**.

#### Student table:

```
+-------------+---------------+
| student_id  | student_name  |
+-------------+---------------+
| 1           | Daniel        |
| 2           | Jade          |
| 3           | Stella        |
| 4           | Jonathan      |
| 5           | Will          |
+-------------+---------------+
```
#### Exam table:
```
+------------+--------------+-----------+
| exam_id    | student_id   | score     |
+------------+--------------+-----------+
| 10         |     1        |    70     |
| 10         |     2        |    80     |
| 10         |     3        |    90     |
| 20         |     1        |    80     |
| 30         |     1        |    70     |
| 30         |     3        |    80     |
| 30         |     4        |    90     |
| 40         |     1        |    60     |
| 40         |     2        |    70     |
| 40         |     4        |    80     |
+------------+--------------+-----------+
```
#### Result table:
```
+-------------+---------------+
| student_id  | student_name  |
+-------------+---------------+
| 2           | Jade          |
+-------------+---------------+
```

- For exam 1: Student 1 and 3 hold the lowest and high score respectively.  
- For exam 2: Student 1 holds both highest and lowest score.  
- For exam 3 and 4: Student 1 and 4 hold the lowest and high score respectively.  
- Student 2 and 5 have never got the highest or lowest in any of the exams.  
- Since student 5 has not taken any exam, he is excluded from the result.  
- So, we only return the information of Student 2.

```sql
-- Step 1: Create a Common Table Expression (CTE) to rank scores within each exam
WITH T AS (
    SELECT
        STUDENT_ID,
        
        -- Rank scores in ascending order to identify lowest scores (rk1 = 1 means lowest)
        RANK() OVER (
            PARTITION BY EXAM_ID
            ORDER BY SCORE ASC
        ) AS RK1,
        
        -- Rank scores in descending order to identify highest scores (rk2 = 1 means highest)
        RANK() OVER (
            PARTITION BY EXAM_ID
            ORDER BY SCORE DESC
        ) AS RK2
    FROM EXAM
)

-- Step 2: Select students who never had the highest or lowest score in any exam
SELECT S.STUDENT_ID, S.STUDENT_NAME
FROM T
JOIN STUDENT S ON T.STUDENT_ID = S.STUDENT_ID
GROUP BY S.STUDENT_ID, S.STUDENT_NAME
HAVING 
    -- Ensure the student never had the lowest score in any exam
    SUM(CASE WHEN RK1 = 1 THEN 1 ELSE 0 END) = 0
    AND
    -- Ensure the student never had the highest score in any exam
    SUM(CASE WHEN RK2 = 1 THEN 1 ELSE 0 END) = 0
ORDER BY S.STUDENT_ID;
```

# [1479. Sales by Day of the Week](https://leetcode.com/problems/sales-by-day-of-the-week/)
You are the business owner and would like to obtain a **sales report** for:
- **Category items**
- **Day of the week**

Write an SQL query to report **how many units** in each category have been ordered on **each day of the week**.

- Return the result table **ordered by category**.

#### Orders table:

```
+------------+--------------+-------------+--------------+-------------+
| order_id   | customer_id  | order_date  | item_id      | quantity    |
+------------+--------------+-------------+--------------+-------------+
| 1          | 1            | 2020-06-01  | 1            | 10          |
| 2          | 1            | 2020-06-08  | 2            | 10          |
| 3          | 2            | 2020-06-02  | 1            | 5           |
| 4          | 3            | 2020-06-03  | 3            | 5           |
| 5          | 4            | 2020-06-04  | 4            | 1           |
| 6          | 4            | 2020-06-05  | 5            | 5           |
| 7          | 5            | 2020-06-05  | 1            | 10          |
| 8          | 5            | 2020-06-14  | 4            | 5           |
| 9          | 5            | 2020-06-21  | 3            | 5           |
+------------+--------------+-------------+--------------+-------------+
```

#### Items table:

```
+------------+----------------+---------------+
| item_id    | item_name      | item_category |
+------------+----------------+---------------+
| 1          | LC Alg. Book   | Book          |
| 2          | LC DB. Book    | Book          |
| 3          | LC SmarthPhone | Phone         |
| 4          | LC Phone 2020  | Phone         |
| 5          | LC SmartGlass  | Glasses       |
| 6          | LC T-Shirt XL  | T-Shirt       |
+------------+----------------+---------------+
```

#### Result table:

```
+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| Category   | Monday    | Tuesday   | Wednesday | Thursday  | Friday    | Saturday  | Sunday    |
+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
| Book       | 20        | 5         | 0         | 0         | 10        | 0         | 0         |
| Glasses    | 0         | 0         | 0         | 0         | 5         | 0         | 0         |
| Phone      | 0         | 0         | 5         | 1         | 0         | 0         | 10        |
| T-Shirt    | 0         | 0         | 0         | 0         | 0         | 0         | 0         |
+------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
```

### Notes

- On **Monday** (2020-06-01, 2020-06-08): 20 units of **Book** sold (10 + 10).
- On **Tuesday** (2020-06-02): 5 units of **Book** sold.
- On **Wednesday** (2020-06-03): 5 units of **Phone** sold.
- On **Thursday** (2020-06-04): 1 unit of **Phone** sold.
- On **Friday** (2020-06-05): 10 units of **Book** and 5 units of **Glasses** sold.
- On **Saturday**: No items sold.
- On **Sunday** (2020-06-14, 2020-06-21): 10 units of **Phone** sold (5 + 5).
- No sales for **T-Shirt** category.

```sql
SELECT 
    ITEM_CATEGORY AS CATEGORY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Monday' THEN QUANTITY ELSE 0 END) AS MONDAY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Tuesday' THEN QUANTITY ELSE 0 END) AS TUESDAY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Wednesday' THEN QUANTITY ELSE 0 END) AS WEDNESDAY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Thursday' THEN QUANTITY ELSE 0 END) AS THURSDAY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Friday' THEN QUANTITY ELSE 0 END) AS FRIDAY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Saturday' THEN QUANTITY ELSE 0 END) AS SATURDAY,
    SUM(CASE WHEN DATENAME(WEEKDAY, ORDER_DATE) = 'Sunday' THEN QUANTITY ELSE 0 END) AS SUNDAY
FROM ORDERS O
JOIN ITEMS I ON O.ITEM_ID = I.ITEM_ID
GROUP BY ITEM_CATEGORY
ORDER BY ITEM_CATEGORY;
```

# [1635. Hopper Company Queries I](https://leetcode.com/problems/hopper-company-queries-i/)

#### Schema

Table: Employees

| Column Name   | Type    |
|---------------|---------|
| id            | int     |
| name          | varchar |
| department_id | int     |

id is the primary key for this table.

Table: Salaries

| Column Name      | Type |
|------------------|------|
| employee_id      | int  |
| salary           | int  |
| effective_date   | date |

(employee_id, effective_date) is the primary key.

#### Description

Given the Employees and Salaries tables, write an SQL query to find the current salary (i.e., the salary with the most recent effective_date) for each employee. Return the employee id, name, and current salary.

#### Sample Input

Employees table:

| id | name   | department_id |
|----|--------|---------------|
| 1  | Alice  | 1             |
| 2  | Bob    | 1             |
| 3  | Carol  | 2             |

Salaries table:

| employee_id | salary | effective_date |
|-------------|--------|---------------|
| 1           | 1000   | 2022-01-01    |
| 1           | 1100   | 2022-02-01    |
| 2           | 800    | 2022-01-01    |
| 3           | 950    | 2022-01-01    |
| 3           | 1000   | 2022-03-01    |

#### Sample Output

| id | name  | current_salary |
|----|-------|----------------|
| 1  | Alice | 1100           |
| 2  | Bob   | 800            |
| 3  | Carol | 1000           |

**Explanation:**  
- For each employee, select the row with the latest effective_date.

```sql
-- GENERATE MONTHS 1 TO 12
WITH CALENDAR AS (
  SELECT 1 AS MONTH
  UNION ALL
  SELECT MONTH + 1
  FROM CALENDAR
  WHERE MONTH < 12
)

-- MONTHLY REPORT FOR 2020
SELECT
  CALENDAR.MONTH,

  -- COUNT OF DRIVERS ACTIVE BY EACH MONTH
  (
    SELECT COUNT(*)
    FROM DRIVERS
    WHERE
      YEAR(JOIN_DATE) < 2020
      OR (YEAR(JOIN_DATE) = 2020 AND MONTH(JOIN_DATE) <= CALENDAR.MONTH)
  ) AS ACTIVE_DRIVERS,

  -- COUNT OF ACCEPTED RIDES PER MONTH
  (
    SELECT COUNT(*)
    FROM ACCEPTEDRIDES AR
    INNER JOIN RIDES R ON AR.RIDE_ID = R.RIDE_ID
    WHERE
      YEAR(R.REQUESTED_AT) = 2020
      AND MONTH(R.REQUESTED_AT) = CALENDAR.MONTH
  ) AS ACCEPTED_RIDES

FROM CALENDAR
OPTION (MAXRECURSION 12); -- LIMIT RECURSION TO 12 MONTHS
```

# [1645. Hopper Company Queries II](https://leetcode.com/problems/hopper-company-queries-ii/)

#### Schema

Table: Employees

| Column Name   | Type    |
|---------------|---------|
| id            | int     |
| name          | varchar |
| department_id | int     |

id is the primary key.

Table: Salaries

| Column Name      | Type |
|------------------|------|
| employee_id      | int  |
| salary           | int  |
| effective_date   | date |

(employee_id, effective_date) is the primary key.

#### Description

Find the employees whose salary increased compared to their previous salary record. Return the id, name, previous_salary, and new_salary for each such record.

#### Sample Input

Employees table:

| id | name   | department_id |
|----|--------|---------------|
| 1  | Alice  | 1             |
| 2  | Bob    | 1             |

Salaries table:

| employee_id | salary | effective_date |
|-------------|--------|---------------|
| 1           | 1000   | 2022-01-01    |
| 1           | 1100   | 2022-02-01    |
| 2           | 800    | 2022-01-01    |

#### Sample Output

| id | name  | previous_salary | new_salary |
|----|-------|-----------------|------------|
| 1  | Alice | 1000            | 1100       |

**Explanation:**  
- Alice's salary increased from 1000 to 1100.

```sql
```

# [1651. Hopper Company Queries III](https://leetcode.com/problems/hopper-company-queries-iii/)

#### Schema

Table: Employees

| Column Name   | Type    |
|---------------|---------|
| id            | int     |
| name          | varchar |
| department_id | int     |

id is the primary key.

Table: Salaries

| Column Name      | Type |
|------------------|------|
| employee_id      | int  |
| salary           | int  |
| effective_date   | date |

(employee_id, effective_date) is the primary key.

#### Description

Find the average salary for each department as of the most recent effective_date for each employee.

#### Sample Input

Employees table:

| id | name   | department_id |
|----|--------|---------------|
| 1  | Alice  | 1             |
| 2  | Bob    | 1             |
| 3  | Carol  | 2             |

Salaries table:

| employee_id | salary | effective_date |
|-------------|--------|---------------|
| 1           | 1000   | 2022-01-01    |
| 1           | 1100   | 2022-02-01    |
| 2           | 800    | 2022-01-01    |
| 3           | 950    | 2022-01-01    |
| 3           | 1000   | 2022-03-01    |

#### Sample Output

| department_id | avg_salary |
|---------------|-----------|
| 1             | 950.00    |
| 2             | 1000.00   |

**Explanation:**  
- Use the latest salary for each employee.

```sql
```

# [1767. Find the Subtasks That Did Not Execute](https://leetcode.com/problems/find-the-subtasks-that-did-not-execute/)
```sql
-- GENERATE ALL POSSIBLE (TASK_ID, SUBTASK_ID) COMBINATIONS
WITH TASKTOSUBTASK AS (
    SELECT TASK_ID, 1 AS SUBTASK_ID
    FROM TASKS
    UNION ALL
    SELECT TASK_ID, SUBTASK_ID + 1
    FROM TASKTOSUBTASK
    JOIN TASKS ON TASKTOSUBTASK.TASK_ID = TASKS.TASK_ID
    WHERE SUBTASK_ID + 1 <= SUBTASKS_COUNT
)
-- GET SUBTASKS THAT WERE NOT EXECUTED
SELECT TASK_ID, SUBTASK_ID
FROM TASKTOSUBTASK
EXCEPT
SELECT TASK_ID, SUBTASK_ID FROM EXECUTED;
```

# [185. Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/)

#### Schema

Table: Employee

| Column Name   | Type    |
|---------------|---------|
| id            | int     |
| name          | varchar |
| salary        | int     |
| departmentId  | int     |

id is the primary key for this table.

Table: Department

| Column Name   | Type    |
|---------------|---------|
| id            | int     |
| name          | varchar |

id is the primary key for this table.

#### Description

Write an SQL query to find the top three salaries for each department. If there are less than three salaries, return all of them.

#### Sample Input

Employee table:

| id | name  | salary | departmentId |
|----|-------|--------|--------------|
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |

Department table:

| id | name      |
|----|-----------|
| 1  | IT        |
| 2  | Sales     |

#### Sample Output

| Department | Employee | Salary |
|------------|----------|--------|
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| IT         | Janet    | 69000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |

**Explanation:**  
- IT department's top three salaries: 90000, 85000, 85000.

```sql
SELECT DEPARTMENT, EMPLOYEE, SALARY
FROM (
    SELECT 
        D.NAME AS DEPARTMENT,
        E.NAME AS EMPLOYEE,
        E.SALARY AS SALARY,
        -- RANK EMPLOYEES BY SALARY WITHIN EACH DEPARTMENT
        DENSE_RANK() OVER (
            PARTITION BY D.NAME
            ORDER BY E.SALARY DESC
        ) AS RK
    FROM EMPLOYEE E
    JOIN DEPARTMENT D ON E.DEPARTMENTID = D.ID
) AS TAB
-- GET TOP 3 HIGHEST-PAID EMPLOYEES PER DEPARTMENT
WHERE RK <= 3;
```

# [1892. Page Recommendations II](https://leetcode.com/problems/page-recommendations-ii/)

#### Schema

Table: Friendship

| Column Name | Type |
|-------------|------|
| user1_id    | int  |
| user2_id    | int  |

(user1_id, user2_id) is the primary key.

Table: Likes

| Column Name | Type |
|-------------|------|
| user_id     | int  |
| page_id     | int  |

(user_id, page_id) is the primary key.

#### Description

For every user, recommend pages that are liked by their friends but not by themselves. Return user_id and recommended page_id.

#### Sample Input

Friendship table:

| user1_id | user2_id |
|----------|----------|
| 1        | 2        |
| 1        | 3        |

Likes table:

| user_id | page_id |
|---------|---------|
| 2       | 101     |
| 3       | 102     |
| 1       | 103     |

#### Sample Output

| user_id | page_id |
|---------|---------|
| 1       | 101     |
| 1       | 102     |

**Explanation:**  
- User 1's friends are 2 and 3. They liked pages 101 and 102, which user 1 hasn't liked.

```sql
```

# [1917. Leetcodify Friends Recommendations](https://leetcode.com/problems/leetcodify-friends-recommendations/)

#### Schema

Table: Friendship

| Column Name | Type |
|-------------|------|
| user1_id    | int  |
| user2_id    | int  |

(user1_id, user2_id) is the primary key.

#### Description

For every user, recommend all friends of their friends who are not already friends with them and are not themselves.

#### Sample Input

Friendship table:

| user1_id | user2_id |
|----------|----------|
| 1        | 2        |
| 2        | 3        |
| 3        | 4        |

#### Sample Output

| user_id | recommended_id |
|---------|---------------|
| 1       | 3             |
| 2       | 4             |

**Explanation:**  
- User 1's friend is 2, friend of 2 is 3, not already a friend of 1 → recommend 3.

```sql
```

# [1919. Leetcodify Similar Friends](https://leetcode.com/problems/leetcodify-similar-friends/)

#### Schema

Table: Friendship

| Column Name | Type |
|-------------|------|
| user1_id    | int  |
| user2_id    | int  |

(user1_id, user2_id) is the primary key.

#### Description

For every pair of users, return if they have at least two friends in common.

#### Sample Input

Friendship table:

| user1_id | user2_id |
|----------|----------|
| 1        | 2        |
| 2        | 3        |
| 1        | 3        |
| 1        | 4        |
| 2        | 4        |

#### Sample Output

| user1_id | user2_id | common_friends |
|----------|----------|----------------|
| 1        | 2        | 2              |
| 1        | 3        | 2              |
| 2        | 3        | 2              |
| 1        | 4        | 2              |
| 2        | 4        | 2              |

**Explanation:**  
- Users 1 & 2 common friends: 3, 4.

```sql
```

# [1972. First and Last Call On the Same Day](https://leetcode.com/problems/first-and-last-call-on-the-same-day/)

#### Schema

Table: Calls

| Column Name | Type |
|-------------|------|
| call_id     | int  |
| user_id     | int  |
| call_time   | datetime |

call_id is primary key.

#### Description

Find the users who made their first and last call on the same day.

#### Sample Input

Calls table:

| call_id | user_id | call_time           |
|---------|---------|---------------------|
| 1       | 1       | 2022-03-01 08:00:00 |
| 2       | 1       | 2022-03-01 18:00:00 |
| 3       | 2       | 2022-03-01 09:00:00 |
| 4       | 2       | 2022-03-02 10:00:00 |

#### Sample Output

| user_id |
|---------|
| 1       |

**Explanation:**  
- User 1's first and last call are on 2022-03-01.

```sql
```

# [2004. The Number of Seniors and Juniors to Join the Company](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company/)
```sql
WITH ACCUMULATEDCANDIDATES AS (
  SELECT
    EMPLOYEE_ID,
    EXPERIENCE,
    ROW_NUMBER() OVER (
      PARTITION BY EXPERIENCE
      ORDER BY SALARY, EMPLOYEE_ID
    ) AS CANDIDATE_COUNT, -- Rank candidates by salary within experience level
    SUM(SALARY) OVER (
      PARTITION BY EXPERIENCE
      ORDER BY SALARY, EMPLOYEE_ID
    ) AS ACCUMULATED_SALARY -- Running total of salary within experience level
  FROM CANDIDATES
),
MAXHIREDSENIORS AS (
  SELECT
    ISNULL(MAX(CANDIDATE_COUNT), 0) AS ACCEPTED_CANDIDATES, -- Max seniors hired under budget
    ISNULL(MAX(ACCUMULATED_SALARY), 0) AS ACCUMULATED_SALARY -- Total salary of hired seniors
  FROM ACCUMULATEDCANDIDATES
  WHERE EXPERIENCE = 'Senior' AND ACCUMULATED_SALARY < 70000
)
SELECT
  'Senior' AS EXPERIENCE,
  ACCEPTED_CANDIDATES
FROM MAXHIREDSENIORS
UNION ALL
SELECT
  'Junior' AS EXPERIENCE,
  COUNT(*) AS ACCEPTED_CANDIDATES
FROM ACCUMULATEDCANDIDATES AS JUNIORS
WHERE EXPERIENCE = 'JUNIOR'
  AND JUNIORS.ACCUMULATED_SALARY < (
    SELECT 70000 - ACCUMULATED_SALARY FROM MAXHIREDSENIORS
  ); -- Hire juniors within remaining budget
```

# [2010. The Number of Seniors and Juniors to Join the Company II](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company-ii/)
```sql
```

# [2118. Build the Equation](https://leetcode.com/problems/build-the-equation/)
### Table: Terms

| Column Name | Type |
|-------------|------|
| `power`     | int  |
| `factor`    | int  |

- `power` is the **primary key** for this table.
- Each row represents one term of a polynomial equation.
- `power` is an integer in the range **[0, 100]**.
- `factor` is a non-zero integer in the range **[-100, 100]**.

You have a powerful program that can solve any equation of one variable. To use it, the equation must be formatted as follows:

- The **left-hand side (LHS)** should contain all the terms.
- The **right-hand side (RHS)** should be `= 0`.
- Each term in the LHS must follow the format:  
  `"<sign><fact>X^<pow>"` where:
  - `<sign>` is either `+` or `-`
  - `<fact>` is the **absolute value** of the factor
  - `<pow>` is the **power** value

- If `power = 1`, omit `^<pow>` → e.g., `+3X`
- If `power = 0`, omit both `X` and `^<pow>` → e.g., `-3`
- Terms must be ordered by **descending power**
- The final equation must end with `=0`

### Example 1

**Input:**

```text
Terms table:
+-------+--------+
| power | factor |
+-------+--------+
|   2   |   1    |
|   1   |  -4    |
|   0   |   2    |
+-------+--------+
```

**Output:**

```text
+--------------+
| equation     |
+--------------+
| +1X^2-4X+2=0 |
+--------------+
```

### Example 2

**Input:**

```text
Terms table:
+-------+--------+
| power | factor |
+-------+--------+
|   4   |  -4    |
|   2   |   1    |
|   1   |  -1    |
+-------+--------+
```

**Output:**

```text
+-----------------+
| equation        |
+-----------------+
| -4X^4+1X^2-1X=0 |
+-----------------+
```

```sql
SELECT 
  STRING_AGG(
    CASE 
      WHEN FACTOR > 0 THEN '+' ELSE ''
    END +
    CAST(FACTOR AS VARCHAR) +
    CASE 
      WHEN POWER = 0 THEN ''
      ELSE 'X'
    END +
    CASE 
      WHEN POWER IN (0, 1) THEN ''
      ELSE '^' + CAST(POWER AS VARCHAR)
    END,
    ''
  ) WITHIN GROUP (ORDER BY POWER DESC) + '=0' AS EQUATION
FROM TERMS;
```

# [2153. The Number of Passengers in Each Bus II](https://leetcode.com/problems/the-number-of-passengers-in-each-bus-ii/)
```sql
```

# [2173. Longest Winning Streak](https://leetcode.com/problems/longest-winning-streak/)
### Table: Matches

```markdown
| Column Name | Type |
|-------------|------|
| player_id   | int  |
| match_day   | date |
| result      | enum |
```

- (player_id, match_day) is the primary key for this table.  
- Each row of this table contains the ID of a player, the day of the match they played, and the result of that match.  
- The result column is an ENUM type of ('Win', 'Draw', 'Lose').

The winning streak of a player is the number of consecutive wins uninterrupted by draws or losses.

Write an SQL query to count the longest winning streak for each player.

Return the result table in any order.

The query result format is in the following example.

### Example 1:

**Input:**  
Matches table:

```markdown
| player_id | match_day  | result |
|-----------|------------|--------|
| 1         | 2022-01-17 | Win    |
| 1         | 2022-01-18 | Win    |
| 1         | 2022-01-25 | Win    |
| 1         | 2022-01-31 | Draw   |
| 1         | 2022-02-08 | Win    |
| 2         | 2022-02-06 | Lose   |
| 2         | 2022-02-08 | Lose   |
| 3         | 2022-03-30 | Win    |
```

**Output:**

```markdown
| player_id | longest_streak |
|-----------|----------------|
| 1         | 3              |
| 2         | 0              |
| 3         | 1              |
```

**Explanation:**  
**Player 1:**  
From 2022-01-17 to 2022-01-25, player 1 won 3 consecutive matches.  
On 2022-01-31, player 1 had a draw.  
On 2022-02-08, player 1 won a match.  
The longest winning streak was 3 matches.

**Player 2:**  
From 2022-02-06 to 2022-02-08, player 2 lost 2 consecutive matches.  
The longest winning streak was 0 matches.

**Player 3:**  
On 2022-03-30, player 3 won a match.  
The longest winning streak was 1 match.

```sql
WITH S AS (
    SELECT *,
        -- Calculate a group identifier 'rk' for consecutive results
        ROW_NUMBER() OVER (PARTITION BY PLAYER_ID ORDER BY MATCH_DAY)
        - ROW_NUMBER() OVER (PARTITION BY PLAYER_ID, RESULT ORDER BY MATCH_DAY) AS RK
    FROM MATCHES
),
T AS (
    -- Count wins within each streak group
    SELECT PLAYER_ID, SUM(CASE WHEN RESULT = 'Win' THEN 1 ELSE 0 END) AS S
    FROM S
    GROUP BY PLAYER_ID, RK
)
-- Select the maximum win streak per player
SELECT PLAYER_ID, MAX(S) AS LONGEST_STREAK
FROM T
GROUP BY PLAYER_ID;
```

# [2199. Finding the Topic of Each Post](https://leetcode.com/problems/finding-the-topic-of-each-post/)
```sql
SELECT
  POSTS.POST_ID,
  ISNULL(
    STRING_AGG(DISTINCT CAST(KEYWORDS.TOPIC_ID AS VARCHAR), ',' 
      ) WITHIN GROUP (ORDER BY KEYWORDS.TOPIC_ID),
    'Ambiguous!' -- If no match, label as Ambiguous
  ) AS TOPIC
FROM POSTS
LEFT JOIN KEYWORDS
  ON CHARINDEX(' ' + LOWER(KEYWORDS.WORD) + ' ', ' ' + LOWER(POSTS.CONTENT) + ' ') > 0
  -- Match whole word using space padding and case-insensitive comparison
GROUP BY POSTS.POST_ID; -- GROUP BY POST ID
```

# [2252. Dynamic Pivoting of a Table](https://leetcode.com/problems/dynamic-pivoting-of-a-table/)
```sql
```

# [2253. Dynamic Unpivoting of a Table](https://leetcode.com/problems/dynamic-unpivoting-of-a-table/)
```sql
```

# [2362. Generate the Invoice](https://leetcode.com/problems/generate-the-invoice/)
### Table: Products

| Column Name | Type |
|-------------|------|
| product_id  | int  |
| price       | int  |

`product_id` is the primary key for this table.  
Each row in this table shows the ID of a product and the price of one unit.

### Table: Purchases

| Column Name | Type |
|-------------|------|
| invoice_id  | int  |
| product_id  | int  |
| quantity    | int  |

(`invoice_id`, `product_id`) is the primary key for this table.  
Each row in this table shows the quantity ordered from one product in an invoice.

Write an SQL query to show the details of the invoice with the highest price. If two or more invoices have the same price, return the details of the one with the smallest invoice_id.

Return the result table in any order.

The query result format is shown in the following example.

### Example 1:

**Input:**  
**Products table:**

| product_id | price |
|------------|-------|
| 1          | 100   |
| 2          | 200   |

**Purchases table:**

| invoice_id | product_id | quantity |
|------------|------------|----------|
| 1          | 1          | 2        |
| 3          | 2          | 1        |
| 2          | 2          | 3        |
| 2          | 1          | 4        |
| 4          | 1          | 10       |

**Output:**

| product_id | quantity | price |
|------------|----------|-------|
| 2          | 3        | 600   |
| 1          | 4        | 400   |

**Explanation:**  
Invoice 1: price = (2 * 100) = $200  
Invoice 2: price = (4 * 100) + (3 * 200) = $1000  
Invoice 3: price = (1 * 200) = $200  
Invoice 4: price = (10 * 100) = $1000

The highest price is $1000, and the invoices with the highest prices are 2 and 4. We return the details of the
```sql
-- CTE to combine purchase and product details
WITH PURCHASEDETAILS AS (
    SELECT P.INVOICE_ID, P.PRODUCT_ID, P.QUANTITY, PR.PRICE
    FROM PURCHASES P
    INNER JOIN PRODUCTS PR ON P.PRODUCT_ID = PR.PRODUCT_ID
),
-- CTE to find the invoice with the highest total amount
TOPINVOICE AS (
    SELECT TOP 1 INVOICE_ID, SUM(PRICE * QUANTITY) AS TOTAL_AMOUNT
    FROM PURCHASEDETAILS
    GROUP BY INVOICE_ID
    ORDER BY TOTAL_AMOUNT DESC, INVOICE_ID
)
-- Final query to list products from the top invoice
SELECT PD.PRODUCT_ID, PD.QUANTITY, (PD.QUANTITY * PD.PRICE) AS TOTAL_PRICE
FROM PURCHASEDETAILS PD
INNER JOIN TOPINVOICE TI ON PD.INVOICE_ID = TI.INVOICE_ID;
```

# [2474. Customers With Strictly Increasing Purchases](https://leetcode.com/problems/customers-with-strictly-increasing-purchases/)
```sql
```

# [2494. Merge Overlapping Events in the Same Hall](https://leetcode.com/problems/merge-overlapping-events-in-the-same-hall/)
```sql
```

# [262. Trips and Users](https://leetcode.com/problems/trips-and-users/)
```sql
SELECT 
    REQUEST_AT AS DAY,
    ROUND(
        -- CALCULATE CANCELLATION RATE
        SUM(CASE WHEN STATUS != 'COMPLETED' THEN 1 ELSE 0 END) * 1.00 / COUNT(*),
        2
    ) AS 'CANCELLATION RATE'
FROM 
    TRIPS
    INNER JOIN USERS AS CLIENTS ON TRIPS.CLIENT_ID = CLIENTS.USERS_ID
    INNER JOIN USERS AS DRIVERS ON TRIPS.DRIVER_ID = DRIVERS.USERS_ID
WHERE 
    CLIENTS.BANNED = 'No'
    AND DRIVERS.BANNED = 'No'
    AND REQUEST_AT BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY 
    REQUEST_AT
ORDER BY 
    REQUEST_AT;
```

# [2701. Consecutive Transactions with Increasing Amounts](https://leetcode.com/problems/consecutive-transactions-with-increasing-amounts/)
```sql
-- STEP 1: BRING IN THE PREVIOUS DAY’S DATE AND AMOUNT PER CUSTOMER
WITH CTE AS (
    SELECT
        CUSTOMER_ID,
        TRANSACTION_DATE,
        AMOUNT,
        LAG(TRANSACTION_DATE) OVER (
            PARTITION BY CUSTOMER_ID
            ORDER BY TRANSACTION_DATE
        ) AS PREV_DATE,
        LAG(AMOUNT) OVER (
            PARTITION BY CUSTOMER_ID
            ORDER BY TRANSACTION_DATE
        ) AS PREV_AMOUNT
    FROM TRANSACTIONS
),

-- STEP 2: FLAG WHERE A NEW STREAK BEGINS (BREAK IN CONSECUTIVENESS OR NON-INCREASING AMOUNT)
FLAGGED AS (
    SELECT
        CUSTOMER_ID,
        TRANSACTION_DATE,
        AMOUNT,
        CASE 
            WHEN PREV_DATE IS NOT NULL
              AND DATEDIFF(DAY, PREV_DATE, TRANSACTION_DATE) = 1
              AND AMOUNT > PREV_AMOUNT 
            THEN 0 
            ELSE 1 
        END AS IS_NEW_GROUP
    FROM CTE
),

-- STEP 3: BUILD A RUNNING SUM OF THOSE FLAGS TO ASSIGN A GROUP IDENTIFIER TO EACH STREAK
GROUPED AS (
    SELECT
        CUSTOMER_ID,
        TRANSACTION_DATE,
        SUM(IS_NEW_GROUP) 
          OVER (PARTITION BY CUSTOMER_ID 
                ORDER BY TRANSACTION_DATE 
                ROWS UNBOUNDED PRECEDING) AS GRP
    FROM FLAGGED
)

-- STEP 4: AGGREGATE BY GROUP, FILTER FOR STREAKS OF LENGTH ≥ 3, AND REPORT THEIR BOUNDS
SELECT
    CUSTOMER_ID,
    MIN(TRANSACTION_DATE) AS CONSECUTIVE_START,
    MAX(TRANSACTION_DATE) AS CONSECUTIVE_END
FROM GROUPED
GROUP BY CUSTOMER_ID, GRP
HAVING COUNT(*) >= 3
ORDER BY CUSTOMER_ID;
```

# [2720. Popularity Percentage](https://leetcode.com/problems/popularity-percentage/)
```sql
WITH F AS (
    -- MAKE FRIENDSHIPS BIDIRECTIONAL
    SELECT * FROM FRIENDS
    UNION
    SELECT USER2, USER1 FROM FRIENDS
),
T AS (
    -- COUNT TOTAL UNIQUE USERS
    SELECT COUNT(DISTINCT USER1) AS CNT FROM F
)
SELECT DISTINCT
    USER1,
    ROUND(
        -- CALCULATE PERCENTAGE POPULARITY
        (COUNT(1) OVER (PARTITION BY USER1)) * 100.0 / (SELECT CNT FROM T),
        2
    ) AS PERCENTAGE_POPULARITY
FROM F
ORDER BY USER1;
```

# [2752. Customers with Maximum Number of Transactions on Consecutive Days](https://leetcode.com/problems/customers-with-maximum-number-of-transactions-on-consecutive-days/)
```sql
WITH S AS (
    SELECT
        CUSTOMER_ID,
        -- SHIFT DATE BACK BY ROW NUMBER TO GROUP SEQUENCES
        DATEADD(DAY, -ROW_NUMBER() OVER (
            PARTITION BY CUSTOMER_ID
            ORDER BY TRANSACTION_DATE
        ), TRANSACTION_DATE) AS SHIFTED_DATE
    FROM TRANSACTIONS
),
T AS (
    -- GROUP BY CUSTOMER AND SHIFTED DATE TO FIND SEQUENCES
    SELECT CUSTOMER_ID, SHIFTED_DATE, COUNT(*) AS CNT
    FROM S
    GROUP BY CUSTOMER_ID, SHIFTED_DATE
)
-- GET CUSTOMER(S) WITH THE LONGEST SEQUENCE
SELECT CUSTOMER_ID
FROM T
WHERE CNT = (SELECT MAX(CNT) FROM T)
ORDER BY CUSTOMER_ID;
```

# [2793. Status of Flight Tickets](https://leetcode.com/problems/status-of-flight-tickets/)
```sql
-- Step 1: Rank passengers by booking time within each flight
WITH RANKEDPASSENGERS AS (
  SELECT
    P.PASSENGER_ID,
    F.FLIGHT_ID,
    F.CAPACITY,
    RANK() OVER (
      PARTITION BY P.FLIGHT_ID
      ORDER BY P.BOOKING_TIME
    ) AS RNK
  FROM PASSENGERS P
  INNER JOIN FLIGHTS F ON P.FLIGHT_ID = F.FLIGHT_ID
)

-- Step 2: Assign status based on rank vs. flight capacity
SELECT
  PASSENGER_ID,
  CASE
    WHEN RNK <= CAPACITY THEN 'Confirmed'
    ELSE 'Waitlist'
  END AS STATUS
FROM RANKEDPASSENGERS
ORDER BY PASSENGER_ID;
```

# [2991. Top Three Wineries](https://leetcode.com/problems/top-three-wineries/)
```sql
-- STEP 1: AGGREGATE AND RANK WINERIES BY COUNTRY
WITH RANKEDWINERIES AS (
    SELECT 
        COUNTRY,
        WINERY,
        SUM(POINTS) AS TOTAL_POINTS,
        RANK() OVER (
            PARTITION BY COUNTRY 
            ORDER BY SUM(POINTS) DESC, WINERY ASC
        ) AS RK
    FROM WINERIES
    GROUP BY COUNTRY, WINERY
)

-- STEP 2: PIVOT TOP 3 WINERIES PER COUNTRY WITH FALLBACK VALUES
SELECT 
    COUNTRY,
    ISNULL(MAX(CASE WHEN RK = 1 THEN CONCAT(WINERY, ' (', TOTAL_POINTS, ')') END), 'no first winery') AS TOP_WINERY,
    ISNULL(MAX(CASE WHEN RK = 2 THEN CONCAT(WINERY, ' (', TOTAL_POINTS, ')') END), 'No second winery') AS SECOND_WINERY,
    ISNULL(MAX(CASE WHEN RK = 3 THEN CONCAT(WINERY, ' (', TOTAL_POINTS, ')') END), 'No third winery') AS THIRD_WINERY
FROM RANKEDWINERIES
WHERE RK <= 3
GROUP BY COUNTRY
ORDER BY COUNTRY;
```

# [2994. Friday Purchases II](https://leetcode.com/problems/friday-purchases-ii/)

### Description

The `Purchases` table has the following schema:  
- user_id       int  
- purchase_date date  
- amount_spend int  

The primary key is the combination `(user_id, purchase_date, amount_spend)`.  
The `purchase_date` ranges from November 1, 2023, to November 30, 2023.  

Write a query to compute, for each Friday in November 2023, the total amount spent by all users on that day.  
If no purchases occurred on a given Friday, report 0.  
Return the result ordered by `week_of_month` in ascending order, where `week_of_month` is 1 for the first Friday, 2 for the second, and so on.

### Sample Input

Purchases table:

| user_id | purchase_date | amount_spend |
|---------|---------------|--------------|
| 11      | 2023-11-07    | 1126         |
| 15      | 2023-11-30    | 7473         |
| 17      | 2023-11-14    | 2414         |
| 12      | 2023-11-24    | 9692         |
| 8       | 2023-11-03    | 5117         |
| 1       | 2023-11-16    | 5241         |
| 10      | 2023-11-12    | 8266         |
| 13      | 2023-11-24    | 12000        |

### Sample Output

| week_of_month | purchase_date | total_amount |
|---------------|---------------|--------------|
| 1             | 2023-11-03    | 5117         |
| 2             | 2023-11-10    | 0            |
| 3             | 2023-11-17    | 0            |
| 4             | 2023-11-24    | 21692        |

### Explanation

- Week 1’s Friday is 2023-11-03, total spending = 5,117.  
- Week 2’s Friday is 2023-11-10, no purchases → 0.  
- Week 3’s Friday is 2023-11-17, no purchases → 0.  
- Week 4’s Friday is 2023-11-24, two purchases (9,692 + 12,000) → 21,692.

```sql
WITH FRIDAYS AS (
    -- SEED WITH THE FIRST FRIDAY OF NOVEMBER 2023
    SELECT CAST('2023-11-03' AS DATE) AS FRIDAY
    UNION ALL
    -- ADD 7 DAYS UNTIL THE END OF NOVEMBER
    SELECT DATEADD(DAY, 7, FRIDAY)
    FROM FRIDAYS
    WHERE DATEADD(DAY, 7, FRIDAY) <= '2023-11-30'
)
SELECT
    -- CALCULATE WEEK_OF_MONTH AS 1 FOR THE FIRST FRIDAY, 2 FOR THE NEXT, ETC.
    DATEDIFF(DAY, '2023-11-03', F.FRIDAY) / 7 + 1 AS WEEK_OF_MONTH,
    F.FRIDAY           AS PURCHASE_DATE,
    ISNULL(SUM(P.AMOUNT_SPEND), 0) AS TOTAL_AMOUNT
FROM FRIDAYS AS F
LEFT JOIN PURCHASES AS P
    ON P.PURCHASE_DATE = F.FRIDAY
GROUP BY
    F.FRIDAY
ORDER BY
    WEEK_OF_MONTH
OPTION (MAXRECURSION 0);
```

# [2995. Viewers Turned Streamers](https://leetcode.com/problems/viewers-turned-streamers/)
```sql
WITH T AS (
    SELECT
        USER_ID,
        SESSION_TYPE,
        RANK() OVER (
            PARTITION BY USER_ID
            ORDER BY SESSION_START
        ) AS RK
    FROM SESSIONS
)
SELECT 
    T.USER_ID, 
    COUNT(*) AS SESSIONS_COUNT
FROM 
    T T
    INNER JOIN SESSIONS S ON T.USER_ID = S.USER_ID
WHERE 
    T.RK = 1 
    AND T.SESSION_TYPE = 'Viewer' 
    AND S.SESSION_TYPE = 'Streamer'
GROUP BY 
    T.USER_ID
ORDER BY 
    SESSIONS_COUNT DESC, 
    T.USER_ID DESC;
```

# [3052. Maximize Items](https://leetcode.com/problems/maximize-items/)
```sql
WITH PRIME AS (
    SELECT SUM(SQUARE_FOOTAGE) AS SUM_SQUARE_FOOTAGE
    FROM INVENTORY
    WHERE ITEM_TYPE = 'prime_eligible'
)
SELECT
    'prime_eligible' AS ITEM_TYPE,
    COUNT(*) * FLOOR(500000.0 / PRIME.SUM_SQUARE_FOOTAGE) AS ITEM_COUNT
FROM INVENTORY
CROSS JOIN PRIME
WHERE ITEM_TYPE = 'prime_eligible'

UNION ALL

SELECT
    'not_prime' AS ITEM_TYPE,
    COUNT(*) * FLOOR((500000.0 % PRIME.SUM_SQUARE_FOOTAGE) / SUM(SQUARE_FOOTAGE))
FROM INVENTORY
CROSS JOIN PRIME
WHERE ITEM_TYPE = 'not_prime';
```

# [3057. Employees Project Allocation](https://leetcode.com/problems/employees-project-allocation/)
```sql
WITH EMPLOYEESWITHAVGWORKLOAD AS (
    SELECT
        E.EMPLOYEE_ID,
        E.NAME AS EMPLOYEE_NAME,
        E.TEAM,
        P.PROJECT_ID,
        P.WORKLOAD AS PROJECT_WORKLOAD,
        AVG(P.WORKLOAD) OVER (PARTITION BY E.TEAM) AS AVG_TEAM_WORKLOAD
    FROM PROJECT P
    INNER JOIN EMPLOYEES E ON P.EMPLOYEE_ID = E.EMPLOYEE_ID
)
SELECT
    EMPLOYEE_ID,
    PROJECT_ID,
    EMPLOYEE_NAME,
    PROJECT_WORKLOAD
FROM EMPLOYEESWITHAVGWORKLOAD
WHERE PROJECT_WORKLOAD > AVG_TEAM_WORKLOAD
ORDER BY EMPLOYEE_ID, PROJECT_ID;
```

# [3060. User Activities within Time Bounds](https://leetcode.com/problems/user-activities-within-time-bounds/)
```sql
-- COMMON TABLE EXPRESSION TO GET PREVIOUS SESSION_END FOR EACH USER/SESSION_TYPE
WITH T AS (
    SELECT
        USER_ID,
        SESSION_START,
        LAG(SESSION_END) OVER (
            PARTITION BY USER_ID, SESSION_TYPE
            ORDER BY SESSION_END
        ) AS PREV_SESSION_END
    FROM SESSIONS
)

-- SELECT USERS WHOSE SESSION STARTED WITHIN 12 HOURS OF THEIR PREVIOUS ONE
SELECT DISTINCT
    USER_ID
FROM T
WHERE PREV_SESSION_END IS NOT NULL -- EXCLUDE FIRST SESSIONS WITH NO PREVIOUS
  AND DATEDIFF(HOUR, PREV_SESSION_END, SESSION_START) <= 12;
```

# [3061. Calculate Trapping Rain Water](https://leetcode.com/problems/calculate-trapping-rain-water/)
```sql
-- CTE TO COMPUTE LEFT AND RIGHT MAX HEIGHTS FOR EACH POSITION
WITH T AS (
    SELECT
        *,
        MAX(HEIGHT) OVER (ORDER BY ID ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS L, -- MAX TO THE LEFT
        MAX(HEIGHT) OVER (ORDER BY ID DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS R -- MAX TO THE RIGHT
    FROM HEIGHTS
)

-- CALCULATE TRAPPED WATER AT EACH POSITION AND SUM IT
SELECT SUM(
    CASE 
        WHEN L < R THEN L - HEIGHT
        ELSE R - HEIGHT
    END
) AS TOTAL_TRAPPED_WATER
FROM T
WHERE L > HEIGHT AND R > HEIGHT; -- ONLY COUNT WHERE WATER CAN BE TRAPPED
```

# [3103. Find Trending Hashtags II](https://leetcode.com/problems/find-trending-hashtags-ii/)
```sql
WITH RECURSIVE
  FEBRUARYTWEETS AS (
    SELECT * FROM TWEETS
    WHERE YEAR(TWEET_DATE) = 2024 AND MONTH(TWEET_DATE) = 2
  ),
  HASHTAGTOTWEET AS (
    -- ANCHOR MEMBER: FIND THE FIRST HASHTAG AND THE REMAINING TWEET TEXT
    SELECT
      SUBSTRING(TWEET, PATINDEX('%#[^ ]%', TWEET), CHARINDEX(' ', TWEET + ' ', PATINDEX('%#[^ ]%', TWEET)) - PATINDEX('%#[^ ]%', TWEET)) AS HASHTAG,
      SUBSTRING(TWEET, PATINDEX('%#[^ ]%', TWEET) + CHARINDEX(' ', TWEET + ' ', PATINDEX('%#[^ ]%', TWEET)) - PATINDEX('%#[^ ]%', TWEET), LEN(TWEET)) AS TWEET
    FROM FEBRUARYTWEETS
    WHERE PATINDEX('%#[^ ]%', TWEET) > 0

    UNION ALL

    -- RECURSIVE MEMBER: FIND THE NEXT HASHTAG AND THE REMAINING TWEET TEXT
    SELECT
      SUBSTRING(TWEET, PATINDEX('%#[^ ]%', TWEET), CHARINDEX(' ', TWEET + ' ', PATINDEX('%#[^ ]%', TWEET)) - PATINDEX('%#[^ ]%', TWEET)) AS HASHTAG,
      SUBSTRING(TWEET, PATINDEX('%#[^ ]%', TWEET) + CHARINDEX(' ', TWEET + ' ', PATINDEX('%#[^ ]%', TWEET)) - PATINDEX('%#[^ ]%', TWEET), LEN(TWEET)) AS TWEET
    FROM HASHTAGTOTWEET
    WHERE PATINDEX('%#[^ ]%', TWEET) > 0
  )
SELECT
  HASHTAG,
  COUNT(*) AS COUNT
FROM HASHTAGTOTWEET
GROUP BY HASHTAG
ORDER BY COUNT DESC, HASHTAG DESC
LIMIT 3;
---------------
WITH RECURSIVE
  FEBRUARYTWEETS AS (
    SELECT * FROM TWEETS
    WHERE YEAR(TWEET_DATE) = 2024 AND MONTH(TWEET_DATE) = 2
  ),
  HASHTAGTOTWEET AS (
    SELECT
      REGEXP_SUBSTR(TWEET, '#[^\\s]+') AS HASHTAG,
      REGEXP_REPLACE(TWEET, '#[^\\s]+', '', 1, 1) AS TWEET
    FROM FEBRUARYTWEETS
    UNION ALL
    SELECT
      REGEXP_SUBSTR(TWEET, '#[^\\s]+') AS HASHTAG,
      REGEXP_REPLACE(TWEET, '#[^\\s]+', '', 1, 1) AS TWEET
    FROM HASHTAGTOTWEET
    WHERE POSITION('#' IN TWEET) > 0
  )
SELECT
  HASHTAG,
  COUNT(*) AS COUNT
FROM HASHTAGTOTWEET
GROUP BY HASHTAG
ORDER BY COUNT DESC, HASHTAG DESC
LIMIT 3;
```

# [3156. Employee Task Duration and Concurrent Tasks](https://leetcode.com/problems/employee-task-duration-and-concurrent-tasks/)
```sql
-- STEP 1: COLLECT ALL UNIQUE TIME POINTS (START AND END) FOR EACH EMPLOYEE
WITH EMPLOYEETIMES AS (
    SELECT DISTINCT EMPLOYEE_ID, START_TIME AS TM FROM TASKS
    UNION
    SELECT DISTINCT EMPLOYEE_ID, END_TIME AS TM FROM TASKS
),

-- STEP 2: CREATE SEGMENTS BETWEEN CONSECUTIVE TIME POINTS USING LEAD()
SEGMENTS AS (
    SELECT
        EMPLOYEE_ID,
        TM AS START_TIME,
        LEAD(TM) OVER (PARTITION BY EMPLOYEE_ID ORDER BY TM) AS END_TIME
    FROM EMPLOYEETIMES
),

-- STEP 3: COUNT HOW MANY TASKS ARE ACTIVE DURING EACH SEGMENT
SEGMENTSCOUNT AS (
    SELECT
        S.EMPLOYEE_ID,
        S.START_TIME,
        S.END_TIME,
        COUNT(*) AS CONCURRENT_COUNT
    FROM SEGMENTS S
    JOIN TASKS T ON S.EMPLOYEE_ID = T.EMPLOYEE_ID
    WHERE S.START_TIME >= T.START_TIME AND S.END_TIME <= T.END_TIME
    GROUP BY S.EMPLOYEE_ID, S.START_TIME, S.END_TIME
)

-- FINAL STEP: AGGREGATE TOTAL TASK HOURS AND MAX CONCURRENCY PER EMPLOYEE
SELECT
    EMPLOYEE_ID,
    FLOOR(SUM(DATEDIFF(SECOND, START_TIME, END_TIME)) / 3600.0) AS TOTAL_TASK_HOURS,
    MAX(CONCURRENT_COUNT) AS MAX_CONCURRENT_TASKS
FROM SEGMENTSCOUNT
GROUP BY EMPLOYEE_ID
ORDER BY EMPLOYEE_ID;
```

# [3188. Find Top Scoring Students II](https://leetcode.com/problems/find-top-scoring-students-ii/)
```sql
-- STEP 1: FILTER STUDENTS WITH AVERAGE GPA >= 2.5
WITH T AS (
    SELECT STUDENT_ID
    FROM ENROLLMENTS
    GROUP BY STUDENT_ID
    HAVING AVG(GPA) >= 2.5
)

-- STEP 2: JOIN WITH STUDENTS AND THEIR MAJOR COURSES
SELECT S.STUDENT_ID
FROM T
JOIN STUDENTS S ON T.STUDENT_ID = S.STUDENT_ID
JOIN COURSES C ON S.MAJOR = C.MAJOR
LEFT JOIN ENROLLMENTS E ON S.STUDENT_ID = E.STUDENT_ID AND C.COURSE_ID = E.COURSE_ID
GROUP BY S.STUDENT_ID
HAVING
    -- ALL MANDATORY COURSES MUST HAVE GRADE 'A'
    SUM(CASE WHEN C.MANDATORY = 'yes' AND E.GRADE = 'A' THEN 1 ELSE 0 END) = 
    SUM(CASE WHEN C.MANDATORY = 'yes' THEN 1 ELSE 0 END)

    -- All optional courses with grades must be 'A' or 'B'
    AND SUM(CASE WHEN C.MANDATORY = 'no' AND E.GRADE IS NOT NULL THEN 1 ELSE 0 END) = 
        SUM(CASE WHEN C.MANDATORY = 'no' AND E.GRADE IN ('A', 'B') THEN 1 ELSE 0 END)

    -- At least 2 optional courses must be graded
    AND SUM(CASE WHEN C.MANDATORY = 'no' AND E.GRADE IS NOT NULL THEN 1 ELSE 0 END) >= 2
ORDER BY S.STUDENT_ID;
```

# [3214. Year on Year Growth Rate](https://leetcode.com/problems/year-on-year-growth-rate/)
```sql
-- Step 1: Aggregate spend per product per year
WITH T AS (
    SELECT 
        PRODUCT_ID,
        YEAR(TRANSACTION_DATE) AS YEAR,
        SUM(SPEND) AS CURR_YEAR_SPEND
    FROM USER_TRANSACTIONS
    GROUP BY PRODUCT_ID, YEAR(TRANSACTION_DATE)
),

-- Step 2: Join current year with previous year for same product
S AS (
    SELECT 
        T1.YEAR,
        T1.PRODUCT_ID,
        T1.CURR_YEAR_SPEND,
        T2.CURR_YEAR_SPEND AS PREV_YEAR_SPEND
    FROM T T1
    LEFT JOIN T T2 
        ON T1.PRODUCT_ID = T2.PRODUCT_ID 
        AND T1.YEAR = T2.YEAR + 1
)

-- Step 3: Calculate YoY growth rate
SELECT 
    *,
    ROUND(
        (CURR_YEAR_SPEND - PREV_YEAR_SPEND) * 100.0 / NULLIF(PREV_YEAR_SPEND, 0), 
        2
    ) AS YOY_RATE
FROM S
ORDER BY PRODUCT_ID, YEAR;
```

# [3236. CEO Subordinate Hierarchy](https://leetcode.com/problems/ceo-subordinate-hierarchy/)

#### Schema  

Table: Employees  

| Column Name   | Type    |
|---------------|---------|
| employee_id   | int     |
| employee_name | varchar |
| manager_id    | int     |
| salary        | int     |

Primary key: employee_id  

#### Description  

Find all subordinates of the CEO (both direct and indirect), reporting for each:  
- subordinate_id: the employee_id of the subordinate  
- subordinate_name: the name of the subordinate  
- hierarchy_level: the distance from the CEO (1 for direct reports, 2 for their reports, etc.)  
- salary_difference: subordinate’s salary minus the CEO’s salary  

Return the rows ordered by hierarchy_level ascending, then subordinate_id ascending.  

#### Sample Input  

Employees table:  

| employee_id | employee_name | manager_id | salary  |
|-------------|---------------|------------|---------|
| 1           | Alice         | NULL       | 150000  |
| 2           | Bob           | 1          | 120000  |
| 3           | Charlie       | 1          | 110000  |
| 4           | David         | 2          | 105000  |
| 5           | Eve           | 2          | 100000  |
| 6           | Frank         | 3          | 95000   |
| 7           | Grace         | 3          | 98000   |
| 8           | Helen         | 5          | 90000   |

#### Sample Output  

| subordinate_id | subordinate_name | hierarchy_level | salary_difference |
|----------------|------------------|-----------------|-------------------|
| 2              | Bob              | 1               | -30000            |
| 3              | Charlie          | 1               | -40000            |
| 4              | David            | 2               | -45000            |
| 5              | Eve              | 2               | -50000            |
| 6              | Frank            | 2               | -55000            |
| 7              | Grace            | 2               | -52000            |
| 8              | Helen            | 3               | -60000            |  

**Explanation:**  
Bob and Charlie report directly to Alice (levels 1), David and Eve report to Bob (level 2), Frank and Grace report to Charlie (level 2), and Helen reports to Eve (level 3). Salary differences are computed relative to Alice’s salary of 150000.  

```sql
WITH T AS (
    -- Base case: top-level manager(s)
    SELECT
        EMPLOYEE_ID,
        EMPLOYEE_NAME,
        0 AS HIERARCHY_LEVEL,
        MANAGER_ID,
        SALARY
    FROM EMPLOYEES
    WHERE MANAGER_ID IS NULL

    UNION ALL

    -- Recursive case: employees reporting to those in T
    SELECT
        E.EMPLOYEE_ID,
        E.EMPLOYEE_NAME,
        T.HIERARCHY_LEVEL + 1 AS HIERARCHY_LEVEL,
        E.MANAGER_ID,
        E.SALARY
    FROM T
    JOIN EMPLOYEES E ON T.EMPLOYEE_ID = E.MANAGER_ID
),
P AS (
    SELECT SALARY
    FROM EMPLOYEES
    WHERE MANAGER_ID IS NULL
)
SELECT
    T.EMPLOYEE_ID AS SUBORDINATE_ID,
    T.EMPLOYEE_NAME AS SUBORDINATE_NAME,
    T.HIERARCHY_LEVEL,
    T.SALARY - P.SALARY AS SALARY_DIFFERENCE
FROM T
CROSS JOIN P
WHERE T.HIERARCHY_LEVEL != 0
ORDER BY T.HIERARCHY_LEVEL, T.EMPLOYEE_ID;
```

# [3268. Find Overlapping Shifts II](https://leetcode.com/problems/find-overlapping-shifts-ii/)
```sql
-- STEP 1: COLLECT ALL UNIQUE TIME POINTS (START AND END TIMES)
WITH T AS (
    SELECT DISTINCT EMPLOYEE_ID, START_TIME AS ST
    FROM EMPLOYEESHIFTS
    UNION
    SELECT DISTINCT EMPLOYEE_ID, END_TIME AS ST
    FROM EMPLOYEESHIFTS
),

-- STEP 2: CREATE TIME INTERVALS BETWEEN EACH TIME POINT
P AS (
    SELECT
        EMPLOYEE_ID,
        ST,
        LEAD(ST) OVER (
            PARTITION BY EMPLOYEE_ID
            ORDER BY ST
        ) AS ED
    FROM T
),

-- STEP 3: COUNT HOW MANY SHIFTS OVERLAP EACH TIME INTERVAL
S AS (
    SELECT
        P.EMPLOYEE_ID,
        P.ST,
        P.ED,
        COUNT(*) AS CONCURRENT_COUNT
    FROM P
    INNER JOIN EMPLOYEESHIFTS E ON P.EMPLOYEE_ID = E.EMPLOYEE_ID
    WHERE P.ST >= E.START_TIME AND P.ED <= E.END_TIME
    GROUP BY P.EMPLOYEE_ID, P.ST, P.ED
),

-- STEP 4: CALCULATE TOTAL OVERLAPPING DURATION BETWEEN SHIFTS
U AS (
    SELECT
        T1.EMPLOYEE_ID,
        SUM(
            DATEDIFF(
                MINUTE,
                T2.START_TIME,
                CASE
                    WHEN T1.END_TIME < T2.END_TIME THEN T1.END_TIME
                    ELSE T2.END_TIME
                END
            )
        ) AS TOTAL_OVERLAP_DURATION
    FROM EMPLOYEESHIFTS T1
    JOIN EMPLOYEESHIFTS T2
        ON T1.EMPLOYEE_ID = T2.EMPLOYEE_ID
        AND T1.START_TIME < T2.START_TIME
        AND T1.END_TIME > T2.START_TIME
    GROUP BY T1.EMPLOYEE_ID
)

-- STEP 5: FINAL OUTPUT - MAX OVERLAPPING SHIFTS AND AVERAGE OVERLAP DURATION
SELECT
    S.EMPLOYEE_ID,
    MAX(S.CONCURRENT_COUNT) AS MAX_OVERLAPPING_SHIFTS,
    ISNULL(AVG(U.TOTAL_OVERLAP_DURATION), 0) AS TOTAL_OVERLAP_DURATION
FROM S
LEFT JOIN U ON S.EMPLOYEE_ID = U.EMPLOYEE_ID
GROUP BY S.EMPLOYEE_ID
ORDER BY S.EMPLOYEE_ID;
```

# [3368. First Letter Capitalization](https://leetcode.com/problems/first-letter-capitalization/)
```sql
-- Step 1: Recursive CTE to capitalize each word in content_text
WITH CAPITALIZED_WORDS AS (
    -- ANCHOR MEMBER: PROCESS THE FIRST WORD
    SELECT
        CONTENT_ID,
        CONTENT_TEXT,
        CAST(LEFT(CONTENT_TEXT, CHARINDEX(' ', CONTENT_TEXT + ' ') - 1) AS VARCHAR(MAX)) AS WORD,
        CAST(
            LTRIM(SUBSTRING(
                CONTENT_TEXT,
                CHARINDEX(' ', CONTENT_TEXT + ' ') + 1,
                LEN(CONTENT_TEXT)
            )) AS VARCHAR(MAX)
        ) AS REMAINING_TEXT,
        CAST(
            UPPER(LEFT(LEFT(CONTENT_TEXT, CHARINDEX(' ', CONTENT_TEXT + ' ') - 1), 1)) +
            LOWER(SUBSTRING(LEFT(CONTENT_TEXT, CHARINDEX(' ', CONTENT_TEXT + ' ') - 1), 2, LEN(CONTENT_TEXT)))
            AS VARCHAR(MAX)
        ) AS PROCESSED_WORD
    FROM USER_CONTENT

    UNION ALL

    -- RECURSIVE MEMBER: PROCESS NEXT WORD AND APPEND TO PROCESSED_WORD
    SELECT
        CW.CONTENT_ID,
        CW.CONTENT_TEXT,
        LEFT(CW.REMAINING_TEXT, CHARINDEX(' ', CW.REMAINING_TEXT + ' ') - 1),
        LTRIM(SUBSTRING(
            CW.REMAINING_TEXT,
            CHARINDEX(' ', CW.REMAINING_TEXT + ' ') + 1,
            LEN(CW.REMAINING_TEXT)
        )),
        CW.PROCESSED_WORD + ' ' +
        UPPER(LEFT(LEFT(CW.REMAINING_TEXT, CHARINDEX(' ', CW.REMAINING_TEXT + ' ') - 1), 1)) +
        LOWER(SUBSTRING(LEFT(CW.REMAINING_TEXT, CHARINDEX(' ', CW.REMAINING_TEXT + ' ') - 1), 2, LEN(CW.REMAINING_TEXT)))
    FROM CAPITALIZED_WORDS CW
    WHERE CW.REMAINING_TEXT <> ''
)

-- STEP 2: FINAL OUTPUT WITH ORIGINAL AND CONVERTED TEXT
SELECT
    CONTENT_ID,
    CONTENT_TEXT AS ORIGINAL_TEXT,
    MAX(PROCESSED_WORD) AS CONVERTED_TEXT
FROM CAPITALIZED_WORDS
GROUP BY CONTENT_ID, CONTENT_TEXT;
```

# [3374. First Letter Capitalization II](https://leetcode.com/problems/first-letter-capitalization-ii/)
```sql
-- STEP 1: RECURSIVELY SPLIT CONTENT_TEXT INTO WORDS USING SUBSTRING
WITH WORDS AS (
    SELECT
        CONTENT_ID,
        SUBSTRING(CONTENT_TEXT, 1, CHARINDEX(' ', CONTENT_TEXT + ' ') - 1) AS WORD, -- FIRST WORD
        SUBSTRING(CONTENT_TEXT, CHARINDEX(' ', CONTENT_TEXT + ' ') + 1, LEN(CONTENT_TEXT)) AS REMAINING_TEXT, -- REMAINING TEXT
        1 AS TOKEN_INDEX
    FROM USER_CONTENT
    WHERE CONTENT_TEXT IS NOT NULL

    UNION ALL

    SELECT
        CONTENT_ID,
        SUBSTRING(REMAINING_TEXT, 1, CHARINDEX(' ', REMAINING_TEXT + ' ') - 1), -- NEXT WORD
        SUBSTRING(REMAINING_TEXT, CHARINDEX(' ', REMAINING_TEXT + ' ') + 1, LEN(REMAINING_TEXT)), -- REMAINING TEXT
        TOKEN_INDEX + 1
    FROM WORDS
    WHERE REMAINING_TEXT <> ''
),

-- STEP 2: CAPITALIZE EACH WORD, HANDLE HYPHENATED WORDS
FORMATTED AS (
    SELECT
        CONTENT_ID,
        TOKEN_INDEX,
        CASE
            WHEN WORD LIKE '%-%' THEN
                -- CAPITALIZE BOTH PARTS OF HYPHENATED WORD
                UPPER(SUBSTRING(WORD, 1, 1)) +
                LOWER(SUBSTRING(WORD, 2, CHARINDEX('-', WORD) - 2)) +
                '-' +
                UPPER(SUBSTRING(WORD, CHARINDEX('-', WORD) + 1, 1)) +
                LOWER(SUBSTRING(WORD, CHARINDEX('-', WORD) + 2, LEN(WORD)))
            ELSE
                -- CAPITALIZE REGULAR WORD
                UPPER(SUBSTRING(WORD, 1, 1)) + LOWER(SUBSTRING(WORD, 2, LEN(WORD)))
        END AS FORMATTED_WORD
    FROM WORDS
),

-- STEP 3: RECONSTRUCT SENTENCE USING STRING_AGG
CONVERTED AS (
    SELECT
        CONTENT_ID,
        STRING_AGG(FORMATTED_WORD, ' ') WITHIN GROUP (ORDER BY TOKEN_INDEX) AS CONVERTED_TEXT
    FROM FORMATTED
    GROUP BY CONTENT_ID
)

-- FINAL OUTPUT
SELECT
    U.CONTENT_ID,
    U.CONTENT_TEXT AS ORIGINAL_TEXT,
    C.CONVERTED_TEXT
FROM USER_CONTENT U
JOIN CONVERTED C ON U.CONTENT_ID = C.CONTENT_ID;
```

# [3384. Team Dominance by Pass Success](https://leetcode.com/problems/team-dominance-by-pass-success/)
```sql
-- COMMON TABLE EXPRESSION TO PREPARE PASS DATA WITH TEAM AND HALF INFO
WITH T AS (
    SELECT
        T1.TEAM_NAME,
        -- DETERMINE HALF: 1 FOR FIRST HALF, 2 FOR SECOND HALF
        CASE 
            WHEN TRY_CAST(P.TIME_STAMP AS TIME) <= '00:45:00' THEN 1 
            ELSE 2 
        END AS HALF_NUMBER,
        -- +1 IF PASS WITHIN SAME TEAM, -1 IF TO OPPONENT
        CASE 
            WHEN T1.TEAM_NAME = T2.TEAM_NAME THEN 1 
            ELSE -1 
        END AS DOMINANCE
    FROM PASSES P
    JOIN TEAMS T1 ON P.PASS_FROM = T1.PLAYER_ID
    JOIN TEAMS T2 ON P.PASS_TO = T2.PLAYER_ID
)

-- AGGREGATE DOMINANCE PER TEAM PER HALF
SELECT 
    TEAM_NAME, 
    HALF_NUMBER, 
    SUM(DOMINANCE) AS DOMINANCE
FROM T
GROUP BY TEAM_NAME, HALF_NUMBER
ORDER BY TEAM_NAME, HALF_NUMBER;
```

# [3390. Longest Team Pass Streak](https://leetcode.com/problems/longest-team-pass-streak/)
```sql
WITH PASSESWITHTEAMS AS (
    SELECT
        P.PASS_FROM,
        P.PASS_TO,
        T1.TEAM_NAME AS TEAM_FROM,
        T2.TEAM_NAME AS TEAM_TO,
        CASE 
            WHEN T1.TEAM_NAME = T2.TEAM_NAME THEN 1 
            ELSE 0 
        END AS SAME_TEAM_FLAG,
        P.TIME_STAMP
    FROM PASSES P
    JOIN TEAMS T1 ON P.PASS_FROM = T1.PLAYER_ID
    JOIN TEAMS T2 ON P.PASS_TO = T2.PLAYER_ID
),
STREAKGROUPS AS (
    SELECT
        TEAM_FROM AS TEAM_NAME,
        TIME_STAMP,
        SAME_TEAM_FLAG,
        SUM(CASE WHEN SAME_TEAM_FLAG = 0 THEN 1 ELSE 0 END) 
            OVER (PARTITION BY TEAM_FROM ORDER BY TIME_STAMP ROWS UNBOUNDED PRECEDING) AS GROUP_ID
    FROM PASSESWITHTEAMS
),
STREAKLENGTHS AS (
    SELECT
        TEAM_NAME,
        GROUP_ID,
        COUNT(*) AS STREAK_LENGTH
    FROM STREAKGROUPS
    WHERE SAME_TEAM_FLAG = 1
    GROUP BY TEAM_NAME, GROUP_ID
),
LONGESTSTREAKS AS (
    SELECT
        TEAM_NAME,
        MAX(STREAK_LENGTH) AS LONGEST_STREAK
    FROM STREAKLENGTHS
    GROUP BY TEAM_NAME
)
SELECT
    TEAM_NAME,
    LONGEST_STREAK
FROM LONGESTSTREAKS
ORDER BY TEAM_NAME;
```

# [3401. Find Circular Gift Exchange Chains](https://leetcode.com/problems/find-circular-gift-exchange-chains/)
```sql
-- BUILD GIFT CHAINS RECURSIVELY
WITH RECURSIVE CHAINS AS (
  -- BASE CASE: EACH GIVER STARTS A CHAIN
  SELECT *, GIVER_ID AS START_ID
  FROM SECRETSANTA

  UNION ALL

  -- RECURSIVE CASE: EXTEND CHAIN IF NO CYCLE
  SELECT S.*, C.START_ID
  FROM SECRETSANTA S
  JOIN CHAINS C
    ON S.GIVER_ID = C.RECEIVER_ID
   AND S.GIVER_ID != C.START_ID
),

-- SUMMARIZE EACH CHAIN BY START_ID
CHAINSUMMARY AS (
  SELECT
    START_ID,
    COUNT(*) AS CHAIN_LENGTH,
    SUM(GIFT_VALUE) AS TOTAL_GIFT_VALUE
  FROM CHAINS
  GROUP BY START_ID
),

-- GET UNIQUE CHAIN PATTERNS
UNIQUECHAINS AS (
  SELECT DISTINCT CHAIN_LENGTH, TOTAL_GIFT_VALUE
  FROM CHAINSUMMARY
)

-- RANK CHAINS BY LENGTH AND VALUE
SELECT
  RANK() OVER (
    ORDER BY CHAIN_LENGTH DESC, TOTAL_GIFT_VALUE DESC
  ) AS CHAIN_ID,
  CHAIN_LENGTH,
  TOTAL_GIFT_VALUE
FROM UNIQUECHAINS;
```

# [3451. Find Invalid IP Addresses](https://leetcode.com/problems/find-invalid-ip-addresses/)
```sql
SELECT L.IP,
       COUNT(*) AS INVALID_COUNT
FROM LOGS L
WHERE (
    -- IP MUST HAVE EXACTLY 4 PARTS
    (SELECT COUNT(*) FROM STRING_SPLIT(L.IP, '.')) <> 4
    OR
    -- ANY PART > 255
    EXISTS (
        SELECT 1
        FROM STRING_SPLIT(L.IP, '.')
        WHERE TRY_CAST([VALUE] AS INT) > 255
    )
    OR
    -- ANY PART HAS LEADING ZEROS
    EXISTS (
        SELECT 1
        FROM STRING_SPLIT(L.IP, '.')
        WHERE LEN([VALUE]) > 1 AND LEFT([VALUE], 1) = '0'
    )
)
GROUP BY L.IP
ORDER BY INVALID_COUNT DESC, L.IP DESC;
```

# [3482. Analyze Organization Hierarchy](https://leetcode.com/problems/analyze-organization-hierarchy/)
```sql
WITH HIERARCHY AS (
    SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MANAGER_ID, SALARY, DEPARTMENT, 1 AS LEVEL
    FROM EMPLOYEES
    WHERE MANAGER_ID IS NULL

    UNION ALL

    SELECT E.EMPLOYEE_ID, E.EMPLOYEE_NAME, E.MANAGER_ID, E.SALARY, E.DEPARTMENT, H.LEVEL + 1
    FROM EMPLOYEES E
    INNER JOIN HIERARCHY H ON E.MANAGER_ID = H.EMPLOYEE_ID
),
TEAMSIZE AS (
    SELECT EMPLOYEE_ID AS MANAGER_ID, EMPLOYEE_ID AS MEMBER_ID
    FROM EMPLOYEES

    UNION ALL

    SELECT TS.MANAGER_ID, E.EMPLOYEE_ID
    FROM TEAMSIZE TS
    INNER JOIN EMPLOYEES E ON E.MANAGER_ID = TS.MEMBER_ID
),
BUDGET AS (
    SELECT TS.MANAGER_ID, COUNT(*) - 1 AS TEAM_SIZE, SUM(E.SALARY) AS BUDGET
    FROM TEAMSIZE TS
    INNER JOIN EMPLOYEES E ON TS.MEMBER_ID = E.EMPLOYEE_ID
    GROUP BY TS.MANAGER_ID
)
SELECT 
    E.EMPLOYEE_ID,
    E.EMPLOYEE_NAME,
    H.LEVEL,
    B.TEAM_SIZE,
    B.BUDGET
FROM EMPLOYEES E
INNER JOIN HIERARCHY H ON E.EMPLOYEE_ID = H.EMPLOYEE_ID
INNER JOIN BUDGET B ON E.EMPLOYEE_ID = B.MANAGER_ID
ORDER BY H.LEVEL ASC, B.BUDGET DESC, E.EMPLOYEE_NAME ASC;
```

# [3554. Find Category Recommendation Pairs](https://leetcode.com/problems/find-category-recommendation-pairs/)
```sql
WITH USERCATEGORY AS (
    SELECT DISTINCT PP.USER_ID, PI.CATEGORY
    FROM PRODUCTPURCHASES PP
    JOIN PRODUCTINFO PI ON PP.PRODUCT_ID = PI.PRODUCT_ID
),
CATEGORYPAIRS AS (
    SELECT 
        UC1.USER_ID,
        UC1.CATEGORY AS CATEGORY1,
        UC2.CATEGORY AS CATEGORY2
    FROM USERCATEGORY UC1
    JOIN USERCATEGORY UC2 
        ON UC1.USER_ID = UC2.USER_ID 
        AND UC1.CATEGORY < UC2.CATEGORY
)
SELECT 
    CATEGORY1,
    CATEGORY2,
    COUNT(DISTINCT USER_ID) AS CUSTOMER_COUNT
FROM CATEGORYPAIRS
GROUP BY CATEGORY1, CATEGORY2
HAVING COUNT(DISTINCT USER_ID) >= 3
ORDER BY CUSTOMER_COUNT DESC, CATEGORY1 ASC, CATEGORY2 ASC;
```

# [3617. Find Students with Study Spiral Pattern](https://leetcode.com/problems/find-students-with-study-spiral-pattern/)
```sql
WITH STUDENT_SESSION_COUNTS AS (
    SELECT STUDENT_ID, SUBJECT, COUNT(*) AS CNT
    FROM STUDY_SESSIONS
    GROUP BY STUDENT_ID, SUBJECT
),
STUDENTS_WHO_STUDIED_ATLEAST_3_SUBJECTS_ATLEAST_2TIMES AS (
    SELECT STUDENT_ID
    FROM STUDENT_SESSION_COUNTS
    GROUP BY STUDENT_ID
    HAVING COUNT(DISTINCT SUBJECT) > 2
       AND MIN(CNT) > 1
),
IDENTIFY_THE_DAYGAPS AS (
    SELECT STUDENT_ID, SUBJECT, HOURS_STUDIED, SESSION_DATE,
           DATEDIFF(DAY, LAG(SESSION_DATE) OVER (PARTITION BY STUDENT_ID ORDER BY SESSION_DATE), SESSION_DATE) AS DAY_GAP
    FROM STUDY_SESSIONS
),
FINDING_CONSECUTIVE_GAP_MINIMUM_2DAYS_OR_LESS AS (
    SELECT STUDENT_ID
    FROM IDENTIFY_THE_DAYGAPS
    GROUP BY STUDENT_ID
    HAVING MAX(DAY_GAP) < 3
),
STUDENT_WHO_STUDYSPIRAL_PATTERN AS (
    SELECT S.STUDENT_ID, S.STUDENT_NAME, S.MAJOR,
           COUNT(DISTINCT SS.SUBJECT) AS CYCLE_LENGTH,
           SUM(SS.HOURS_STUDIED) AS TOTAL_STUDY_HOURS,
           COUNT(*) OVER () AS UNIQUE_STUDENT_ID_SHOULDATLEAST_MORETHAN_1_STUDENTS_IS_THE_KEY
    FROM STUDENTS S
    JOIN STUDY_SESSIONS SS ON S.STUDENT_ID = SS.STUDENT_ID
    JOIN STUDENTS_WHO_STUDIED_ATLEAST_3_SUBJECTS_ATLEAST_2TIMES SWS ON S.STUDENT_ID = SWS.STUDENT_ID
    JOIN FINDING_CONSECUTIVE_GAP_MINIMUM_2DAYS_OR_LESS FG ON S.STUDENT_ID = FG.STUDENT_ID
    GROUP BY S.STUDENT_ID, S.STUDENT_NAME, S.MAJOR
)
SELECT STUDENT_ID, STUDENT_NAME, MAJOR, CYCLE_LENGTH, TOTAL_STUDY_HOURS
FROM STUDENT_WHO_STUDYSPIRAL_PATTERN
WHERE UNIQUE_STUDENT_ID_SHOULDATLEAST_MORETHAN_1_STUDENTS_IS_THE_KEY > 1
ORDER BY CYCLE_LENGTH DESC, TOTAL_STUDY_HOURS DESC;
```

# [569. Median Employee Salary](https://leetcode.com/problems/median-employee-salary/)
```sql
WITH T AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY COMPANY ORDER BY SALARY ASC) AS RK,
           COUNT(ID) OVER (PARTITION BY COMPANY) AS N
    FROM EMPLOYEE
)
SELECT ID, COMPANY, SALARY
FROM T
WHERE RK >= N / 2 AND RK <= N / 2 + 1;
```

# [571. Find Median Given Frequency of Numbers](https://leetcode.com/problems/find-median-given-frequency-of-numbers/)
```sql
WITH
    T AS (
        SELECT
            *,
            SUM(FREQUENCY) OVER (ORDER BY NUM ASC) AS RK1,
            SUM(FREQUENCY) OVER (ORDER BY NUM DESC) AS RK2,
            SUM(FREQUENCY) OVER () AS S
        FROM NUMBERS
    )
SELECT
    ROUND(AVG(NUM), 1) AS MEDIAN
FROM T
WHERE RK1 >= S / 2 AND RK2 >= S / 2;
```

# [579. Find Cumulative Salary of an Employee](https://leetcode.com/problems/find-cumulative-salary-of-an-employee/)
```sql
WITH T AS (
    SELECT 
        ID, 
        MONTH, 
        SUM(SALARY) OVER (
            PARTITION BY ID 
            ORDER BY MONTH 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS SALARY,
        RANK() OVER (
            PARTITION BY ID 
            ORDER BY MONTH DESC
        ) AS RK
    FROM EMPLOYEE
)
SELECT ID, MONTH, SALARY
FROM T
WHERE RK > 1
ORDER BY ID, MONTH DESC;
```

# [601. Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/)
```sql
WITH S AS (
    SELECT *,
           ID - ROW_NUMBER() OVER (ORDER BY ID) AS RK
    FROM STADIUM
    WHERE PEOPLE >= 100
),
T AS (
    SELECT *,
           COUNT(1) OVER (PARTITION BY RK) AS CNT
    FROM S
)
SELECT ID, VISIT_DATE, PEOPLE
FROM T
WHERE CNT >= 3
```

# [615. Average Salary: Departments VS Company](https://leetcode.com/problems/average-salary-departments-vs-company/)
```sql
WITH T AS (
    SELECT
        FORMAT(PAY_DATE, 'yyyy-MM') AS PAY_MONTH,
        DEPARTMENT_ID,
        AVG(AMOUNT) OVER (PARTITION BY PAY_DATE) AS COMPANY_AVG_AMOUNT,
        AVG(AMOUNT) OVER (PARTITION BY PAY_DATE, DEPARTMENT_ID) AS DEPARTMENT_AVG_AMOUNT
    FROM
        SALARY AS S
        JOIN EMPLOYEE AS E ON S.EMPLOYEE_ID = E.EMPLOYEE_ID
)
SELECT DISTINCT
    PAY_MONTH,
    DEPARTMENT_ID,
    CASE
        WHEN COMPANY_AVG_AMOUNT = DEPARTMENT_AVG_AMOUNT THEN 'same'
        WHEN COMPANY_AVG_AMOUNT < DEPARTMENT_AVG_AMOUNT THEN 'higher'
        ELSE 'lower'
    END AS COMPARISON
FROM T;
```

# [618. Students Report By Geography](https://leetcode.com/problems/students-report-by-geography/)

#### Schema

Table: Student

| Column Name | Type    |
|-------------|---------|
| name        | varchar |
| continent   | varchar |

This table may contain duplicate rows.

#### Description

Each row in the Student table indicates a student’s name and the continent they came from (America, Asia or Europe). Pivot the continent column into three output columns—America, Asia and Europe—so that each student’s name appears under its corresponding continent. Within each continent, sort names alphabetically, and align them by their rank (first, second, etc.), showing `null` when a continent has no student at a given position. It is guaranteed that America has at least as many students as Asia or Europe.

#### Sample Input

Student table:

| name   | continent |
|--------|-----------|
| Jane   | America   |
| Pascal | Europe    |
| Xi     | Asia      |
| Jack   | America   |

#### Sample Output

| America | Asia | Europe |
|---------|------|--------|
| Jack    | Xi   | Pascal |
| Jane    | null | null   |

```sql
WITH
    T AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY CONTINENT
                ORDER BY NAME
            ) AS RK
        FROM STUDENT
    )
SELECT
    MAX(CASE WHEN CONTINENT = 'america' THEN NAME ELSE NULL END) AS 'AMERICA',
    MAX(CASE WHEN CONTINENT = 'asia' THEN NAME ELSE NULL END) AS 'ASIA',
    MAX(CASE WHEN CONTINENT = 'europe' THEN NAME ELSE NULL END) AS 'EUROPE'
FROM T
GROUP BY RK
ORDER BY RK;

```





















