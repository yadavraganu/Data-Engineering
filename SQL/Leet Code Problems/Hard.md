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
```sql
```

# [1194. Tournament Winners](https://leetcode.com/problems/tournament-winners/)
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
```sql
```

# [1384. Total Sales Amount by Year](https://leetcode.com/problems/total-sales-amount-by-year/)
```sql
```

# [1412. Find the Quiet Students in All Exams](https://leetcode.com/problems/find-the-quiet-students-in-all-exams/)
```sql
```

# [1479. Sales by Day of the Week](https://leetcode.com/problems/sales-by-day-of-the-week/)
```sql
```

# [1635. Hopper Company Queries I](https://leetcode.com/problems/hopper-company-queries-i/)
```sql
```

# [1645. Hopper Company Queries II](https://leetcode.com/problems/hopper-company-queries-ii/)
```sql
```

# [1651. Hopper Company Queries III](https://leetcode.com/problems/hopper-company-queries-iii/)
```sql
```

# [1767. Find the Subtasks That Did Not Execute](https://leetcode.com/problems/find-the-subtasks-that-did-not-execute/)
```sql
```

# [185. Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/)
```sql
```

# [1892. Page Recommendations II](https://leetcode.com/problems/page-recommendations-ii/)
```sql
```

# [1917. Leetcodify Friends Recommendations](https://leetcode.com/problems/leetcodify-friends-recommendations/)
```sql
```

# [1919. Leetcodify Similar Friends](https://leetcode.com/problems/leetcodify-similar-friends/)
```sql
```

# [1972. First and Last Call On the Same Day](https://leetcode.com/problems/first-and-last-call-on-the-same-day/)
```sql
```

# [2004. The Number of Seniors and Juniors to Join the Company](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company/)
```sql
```

# [2010. The Number of Seniors and Juniors to Join the Company II](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company-ii/)
```sql
```

# [2118. Build the Equation](https://leetcode.com/problems/build-the-equation/)
```sql
```

# [2153. The Number of Passengers in Each Bus II](https://leetcode.com/problems/the-number-of-passengers-in-each-bus-ii/)
```sql
```

# [2173. Longest Winning Streak](https://leetcode.com/problems/longest-winning-streak/)
```sql
```

# [2199. Finding the Topic of Each Post](https://leetcode.com/problems/finding-the-topic-of-each-post/)
```sql
```

# [2252. Dynamic Pivoting of a Table](https://leetcode.com/problems/dynamic-pivoting-of-a-table/)
```sql
```

# [2253. Dynamic Unpivoting of a Table](https://leetcode.com/problems/dynamic-unpivoting-of-a-table/)
```sql
```

# [2362. Generate the Invoice](https://leetcode.com/problems/generate-the-invoice/)
```sql
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
```

# [2793. Status of Flight Tickets](https://leetcode.com/problems/status-of-flight-tickets/)
```sql
```

# [2991. Top Three Wineries](https://leetcode.com/problems/top-three-wineries/)
```sql
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


