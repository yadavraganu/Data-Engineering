# Easy
### 1050. Actors and Directors Who Cooperated At Least Three Times
```sql
SELECT ACTOR_ID, DIRECTOR_ID FROM ACTORDIRECTOR GROUP BY ACTOR_ID, DIRECTOR_ID HAVING COUNT(*) >= 3
```
---
### 1068. Product Sales Analysis I
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
### 1069. Product Sales Analysis II
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
### 1075. Project Employees I
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
### 1076. Project Employees II
```sql
SELECT
    PROJECT_ID
FROM
    PROJECT
GROUP BY
    PROJECT_ID
HAVING
    COUNT(EMPLOYEE_ID) = (SELECT MAX(EMPLOYEE_COUNT) FROM (SELECT COUNT(EMPLOYEE_ID) AS EMPLOYEE_COUNT FROM PROJECT GROUP BY PROJECT_ID) AS COUNTS);
```
---
### 1082. Sales Analysis I
```sql
SELECT SELLER_ID
FROM SALES
GROUP BY SELLER_ID
HAVING
    SUM(PRICE) >= ALL (
        SELECT SUM(PRICE)
        FROM SALES
        GROUP BY SELLER_ID
    );
-----------------------
WITH
  SELLERTOPRICE AS (
    SELECT SELLER_ID, SUM(PRICE) AS PRICE
    FROM SALES
    GROUP BY 1
  )
SELECT SELLER_ID
FROM SELLERTOPRICE
WHERE PRICE = (
    SELECT MAX(PRICE)
    FROM SELLERTOPRICE
  );
```
---
### 1083. Sales Analysis II
```sql
SELECT SALES.BUYER_ID
FROM SALES
INNER JOIN PRODUCT
  USING (PRODUCT_ID)
GROUP BY 1
HAVING
  SUM(PRODUCT.PRODUCT_NAME = 's8') > 0
  AND SUM(PRODUCT.PRODUCT_NAME = 'iphone') = 0;
```
---
### 1084. Sales Analysis III
```sql
SELECT
    P.PRODUCT_ID,
    P.PRODUCT_NAME
FROM
    PRODUCT P
JOIN
    SALES S ON P.PRODUCT_ID = S.PRODUCT_ID
GROUP BY
    P.PRODUCT_ID, P.PRODUCT_NAME
HAVING
    MIN(S.SALE_DATE) >= '2019-01-01' AND MAX(S.SALE_DATE) <= '2019-03-31';
```
---
### 1113. Reported Posts
```sql
SELECT
  EXTRA AS REPORT_REASON,
  COUNT(DISTINCT POST_ID) AS REPORT_COUNT
FROM ACTIONS
WHERE
  ACTION = 'report'
  AND DATEDIFF('2019-07-05', ACTION_DATE) = 1
GROUP BY 1;
```
---
### 1141. User Activity for the Past 30 Days I
```sql
SELECT
    ACTIVITY_DATE AS DAY,
    COUNT(DISTINCT USER_ID) AS ACTIVE_USERS
FROM
    ACTIVITY
WHERE
    ACTIVITY_DATE BETWEEN DATEADD(DAY, -29, '2019-07-27') AND '2019-07-27'
GROUP BY
    ACTIVITY_DATE
ORDER BY
    DAY;
```
---
### 1142. User Activity for the Past 30 Days II
```sql
SELECT
  IFNULL(
    ROUND(
      COUNT(DISTINCT SESSION_ID) / COUNT(DISTINCT USER_ID),
      2
    ),
    0.00
  ) AS AVERAGE_SESSIONS_PER_USER
FROM ACTIVITY
WHERE ACTIVITY_DATE BETWEEN '2019-06-28' AND  '2019-07-27';
```
---
### 1148. Article Views I
```sql
SELECT DISTINCT AUTHOR_ID AS ID
FROM VIEWS
WHERE AUTHOR_ID = VIEWER_ID
ORDER BY ID ASC;
```
---
### 1173. Immediate Food Delivery I
```sql
SELECT 
  CAST(
    SUM(
      CASE WHEN ORDER_DATE = CUSTOMER_PREF_DELIVERY_DATE THEN 1 ELSE 0 END
    ) * 100.0 AS DECIMAL(5, 2)
  ) / COUNT(*) AS IMMEDIATE_PERCENTAGE 
FROM 
  DELIVERY;
```
---
### 1179. Reformat Department Table
```sql
SELECT
    ID,
    SUM(CASE WHEN MONTH = 'Jan' THEN REVENUE ELSE NULL END) AS JAN_REVENUE,
    SUM(CASE WHEN MONTH = 'Feb' THEN REVENUE ELSE NULL END) AS FEB_REVENUE,
    SUM(CASE WHEN MONTH = 'Mar' THEN REVENUE ELSE NULL END) AS MAR_REVENUE,
    SUM(CASE WHEN MONTH = 'Apr' THEN REVENUE ELSE NULL END) AS APR_REVENUE,
    SUM(CASE WHEN MONTH = 'May' THEN REVENUE ELSE NULL END) AS MAY_REVENUE,
    SUM(CASE WHEN MONTH = 'Jun' THEN REVENUE ELSE NULL END) AS JUN_REVENUE,
    SUM(CASE WHEN MONTH = 'Jul' THEN REVENUE ELSE NULL END) AS JUL_REVENUE,
    SUM(CASE WHEN MONTH = 'Aug' THEN REVENUE ELSE NULL END) AS AUG_REVENUE,
    SUM(CASE WHEN MONTH = 'Sep' THEN REVENUE ELSE NULL END) AS SEP_REVENUE,
    SUM(CASE WHEN MONTH = 'Oct' THEN REVENUE ELSE NULL END) AS OCT_REVENUE,
    SUM(CASE WHEN MONTH = 'Nov' THEN REVENUE ELSE NULL END) AS NOV_REVENUE,
    SUM(CASE WHEN MONTH = 'Dec' THEN REVENUE ELSE NULL END) AS DEC_REVENUE
FROM DEPARTMENT
--------------------------------
SELECT
    ID,
    [Jan] AS Jan_Revenue,
    [Feb] AS Feb_Revenue,
    [Mar] AS Mar_Revenue,
    [Apr] AS Apr_Revenue,
    [May] AS May_Revenue,
    [Jun] AS Jun_Revenue,
    [Jul] AS Jul_Revenue,
    [Aug] AS Aug_Revenue,
    [Sep] AS Sep_Revenue,
    [Oct] AS Oct_Revenue,
    [Nov] AS Nov_Revenue,
    [Dec] AS Dec_Revenue
FROM (
    SELECT ID, REVENUE, MONTH FROM DEPARTMENT
) S
PIVOT (
    SUM(REVENUE)
    FOR MONTH IN (
        [Jan],[Feb],[Mar],[Apr],[May],[Jun],
        [Jul],[Aug],[Sep],[Oct],[Nov],[Dec] )
) P;
```
---
### 1211. Queries Quality and Percentage
```sql
SELECT QUERY_NAME,
       ROUND(SUM(RATING*1.0/POSITION)*1.0/COUNT(*),2) AS QUALITY,
       ROUND(COUNT(CASE WHEN RATING<3 THEN 1 ELSE NULL END)*100.00/COUNT(*), 2) AS POOR_QUERY_PERCENTAGE 
FROM QUERIES
GROUP BY QUERY_NAME
```
---
### 1241. Number of Comments per Post
```sql
WITH POSTS AS (
  SELECT 
    DISTINCT SUB_ID AS POST_ID 
  FROM 
    SUBMISSIONS 
  WHERE 
    PARENT_ID IS NULL
) 
SELECT 
  POSTS.POST_ID, 
  COUNT(DISTINCT COMMENTS.SUB_ID) AS NUMBER_OF_COMMENTS 
FROM 
  POSTS 
  LEFT JOIN SUBMISSIONS AS COMMENTS ON (
    POSTS.POST_ID = COMMENTS.PARENT_ID
  ) 
GROUP BY 
  1;
```
---
### 1251. Average Selling Price
```sql
SELECT 
  P.PRODUCT_ID, 
  ISNULL(
    ROUND(SUM(P.PRICE * U.UNITS * 1.0) / SUM(U.UNITS),2),0
  ) AS AVERAGE_PRICE 
FROM 
  PRICES P 
  LEFT JOIN UNITSSOLD U ON P.PRODUCT_ID = U.PRODUCT_ID 
  AND U.PURCHASE_DATE BETWEEN P.START_DATE 
  AND P.END_DATE 
GROUP BY 
  P.PRODUCT_ID;
```
---
### 1280. Students and Examinations
```sql
SELECT 
  STUDENTS.STUDENT_ID, 
  STUDENTS.STUDENT_NAME, 
  SUBJECTS.SUBJECT_NAME, 
  COUNT(EXAMINATIONS.STUDENT_ID) AS ATTENDED_EXAMS 
FROM 
  STUDENTS CROSS 
  JOIN SUBJECTS 
  LEFT JOIN EXAMINATIONS ON (
    STUDENTS.STUDENT_ID = EXAMINATIONS.STUDENT_ID 
    AND SUBJECTS.SUBJECT_NAME = EXAMINATIONS.SUBJECT_NAME
  ) 
GROUP BY 
  STUDENTS.STUDENT_ID, STUDENTS.STUDENT_NAME, SUBJECTS.SUBJECT_NAME 
ORDER BY 
  1, 2, 3
```
---
### 1294. Weather Type in Each Country
```sql
SELECT
  COUNTRY_NAME,
  (
    CASE
      WHEN AVG(WEATHER.WEATHER_STATE * 1.0) <= 15.0 THEN 'COLD'
      WHEN AVG(WEATHER.WEATHER_STATE * 1.0) >= 25.0 THEN 'HOT'
      ELSE 'WARM'
    END
  ) AS WEATHER_TYPE
FROM COUNTRIES
INNER JOIN WEATHER
  USING (COUNTRY_ID)
WHERE DAY BETWEEN '2019-11-01' AND '2019-11-30'
GROUP BY 1;
```
---
### 1303. Find the Team Size
```sql
SELECT
  EMPLOYEE_ID,
  COUNT(*) OVER(PARTITION BY TEAM_ID) AS TEAM_SIZE
FROM EMPLOYEE;
```
---
### 1322. Ads Performance
```sql
SELECT
    AD_ID,
    ROUND(IFNULL(SUM(ACTION = 'Clicked') / SUM(ACTION IN ('Clicked', 'Viewed')) * 100, 0), 2) AS CTR
FROM ADS
GROUP BY 1
ORDER BY 2 DESC, 1;
```
---
### 1327. List the Products Ordered in a Period
```sql
SELECT
  P.PRODUCT_NAME,
  SUM(O.UNIT) AS UNIT
FROM PRODUCTS P
INNER JOIN ORDERS O
ON P.PRODUCT_ID = O.PRODUCT_ID
WHERE FORMAT(O.ORDER_DATE, 'yyyy-MM') = '2020-02'
GROUP BY P.PRODUCT_NAME
HAVING SUM(O.UNIT) >= 100;
```
---
### 1350. Students With Invalid Departments
```sql
SELECT
  STUDENTS.ID,
  STUDENTS.NAME
FROM STUDENTS
LEFT JOIN DEPARTMENTS
  ON STUDENTS.DEPARTMENT_ID = DEPARTMENTS.ID
WHERE DEPARTMENTS.ID IS NULL;
```
---
### 1378. Replace Employee ID With The Unique Identifier
```sql
SELECT
  EU.UNIQUE_ID,
  E.NAME
FROM EMPLOYEES E
LEFT JOIN EMPLOYEEUNI EU
ON E.ID = EU.ID;
```
---
### 1407. Top Travellers
```sql
SELECT 
  NAME, TRAVELLED_DISTANCE 
FROM 
  (
    SELECT 
      U.ID, U.NAME, ISNULL(SUM(R.DISTANCE), 0) AS TRAVELLED_DISTANCE 
    FROM 
      USERS U 
      LEFT JOIN RIDES R ON (U.ID = R.USER_ID) 
    GROUP BY 
      U.ID, U.NAME
  ) D 
ORDER BY 2 DESC, 1;
```
---
### 1421. NPV Queries
```sql
SELECT
  Q.ID,
  Q.YEAR,
  ISNULL(N.NPV, 0) AS NPV
FROM QUERIES Q
LEFT JOIN NPV N
ON Q.ID = N.ID AND Q.YEAR = N.YEAR;
```
---
### 1435. Create a Session Bar Chart
```sql
SELECT 
  '[0-5>' AS BIN, 
  COUNT(1) AS TOTAL 
FROM SESSIONS WHERE DURATION < 300 
UNION 
SELECT 
  '[5-10>' AS BIN, 
  COUNT(1) AS TOTAL 
FROM SESSIONS WHERE 300 <= DURATION AND DURATION < 600 
UNION 
SELECT 
  '[10-15>' AS BIN, 
  COUNT(1) AS TOTAL 
FROM SESSIONS WHERE 600 <= DURATION AND DURATION < 900 
UNION 
SELECT 
  '15 OR MORE' AS BIN, 
  COUNT(1) AS TOTAL 
FROM SESSIONS WHERE 900 <= DURATION;
```
---
### 1484. Group Sold Products By The Date
```sql
WITH T AS (
    SELECT DISTINCT * FROM ACTIVITIES
    )
SELECT 
     SELL_DATE
    ,COUNT(1) AS NUM_SOLD
    ,STRING_AGG(PRODUCT,',') WITHIN GROUP (ORDER BY PRODUCT) AS PRODUCTS
FROM T
GROUP BY SELL_DATE
ORDER BY SELL_DATE
```
---
### 1495. Friendly Movies Streamed Last Month
```sql
SELECT DISTINCT CONTENT.TITLE
FROM CONTENT
INNER JOIN TVPROGRAM  USING (CONTENT_ID)
WHERE
    CONTENT.KIDS_CONTENT = 'Y'
    AND CONTENT.CONTENT_TYPE = 'Movies'
    AND DATE_FORMAT(TVPROGRAM.PROGRAM_DATE, '%Y-%M') = '2020-06';
```
---
### 1511. Customer Order Frequency
```sql
SELECT 
  C.CUSTOMER_ID, 
  C.NAME 
FROM 
  ORDERS AS O 
  JOIN PRODUCT AS P ON O.PRODUCT_ID = P.PRODUCT_ID 
  JOIN CUSTOMERS AS C ON O.CUSTOMER_ID = C.CUSTOMER_ID 
WHERE 
  YEAR(O.ORDER_DATE) = 2020 
GROUP BY 
  C.CUSTOMER_ID, 
  C.NAME 
HAVING 
  SUM(
    CASE WHEN MONTH(O.ORDER_DATE) = 6 THEN O.QUANTITY * P.PRICE ELSE 0 END
  ) >= 100 
  AND SUM(
    CASE WHEN MONTH(O.ORDER_DATE) = 7 THEN O.QUANTITY * P.PRICE ELSE 0 END
  ) >= 100;

```
---
### 1517. Find Users With Valid E-Mails
```sql
SELECT 
    *
FROM
    USERS
WHERE
    -- last 13 digits should be '@leetcode.com'
    RIGHT(MAIL,13) = '@leetcode.com' COLLATE Latin1_General_CS_AS
    -- before the '@leetcode.com', there should not be any digit which are not a-z , A-Z , 0-9 , - , . , _
    AND LEFT(MAIL, LEN(MAIL) - 13) NOT LIKE '%[^a-zA-Z0-9_.-]%'
    -- 1st digit should be any digit of a-z or A-Z
    AND LEFT(MAIL,1) LIKE '[a-zA-Z]%';
```
---
### 1527. Patients With a Condition
```sql
SELECT *
FROM PATIENTS
WHERE
    CONDITIONS LIKE 'DIAB1%' OR
    CONDITIONS LIKE '% DIAB1%';
```
---
### 1543. Fix Product Name Format
```sql
WITH
    T AS (
        SELECT
            LOWER(TRIM(PRODUCT_NAME)) AS PRODUCT_NAME,
            DATE_FORMAT(SALE_DATE, '%Y-%M') AS SALE_DATE
        FROM SALES
    )
SELECT PRODUCT_NAME, SALE_DATE, COUNT(1) AS TOTAL
FROM T
GROUP BY 1, 2
ORDER BY 1, 2;
```
---
### 1565. Unique Orders and Customers Per Month
```sql
SELECT
    FORMAT(ORDER_DATE, 'yyyy-MM') AS MONTH,
    COUNT(DISTINCT ORDER_ID) AS ORDER_COUNT,
    COUNT(DISTINCT CUSTOMER_ID) AS CUSTOMER_COUNT
FROM
    ORDERS
WHERE
    INVOICE > 20
GROUP BY
    FORMAT(ORDER_DATE, 'yyyy-MM')
ORDER BY
    MONTH;
```
---
### 1571. Warehouse Manager
```sql
SELECT
    W.NAME AS WAREHOUSE_NAME,
    SUM(W.UNITS * P.WIDTH * P.LENGTH * P.HEIGHT) AS VOLUME
FROM
    WAREHOUSE W
JOIN
    PRODUCTS P ON W.PRODUCT_ID = P.PRODUCT_ID
GROUP BY
    W.NAME;
```
---
### 1581. Customer Who Visited but Did Not Make Any Transactions
```sql
SELECT
    V.CUSTOMER_ID,
    COUNT(V.VISIT_ID) AS COUNT_NO_TRANS
FROM
    VISITS V
LEFT JOIN
    TRANSACTIONS T ON V.VISIT_ID = T.VISIT_ID
WHERE
    T.VISIT_ID IS NULL
GROUP BY
    V.CUSTOMER_ID;
```
---
### 1587. Bank Account Summary II
```sql
SELECT
    U.NAME,
    SUM(T.AMOUNT) AS BALANCE
FROM
    USERS U
JOIN
    TRANSACTIONS T ON U.ACCOUNT = T.ACCOUNT
GROUP BY
    U.NAME
HAVING
    SUM(T.AMOUNT) > 10000;
```
---
### 1607. Sellers With No Sales
```sql
SELECT
    S.SELLER_NAME
FROM
    SELLER S
LEFT JOIN
    ORDERS O ON S.SELLER_ID = O.SELLER_ID AND YEAR(O.SALE_DATE) = 2020
WHERE
    O.ORDER_ID IS NULL;
```
---
### 1623. All Valid Triplets That Can Represent a Country
```sql
SELECT
    SA.STUDENT_NAME AS MEMBER_A,
    SB.STUDENT_NAME AS MEMBER_B,
    SC.STUDENT_NAME AS MEMBER_C
FROM
    SCHOOLA SA
CROSS JOIN
    SCHOOLB SB
CROSS JOIN
    SCHOOLC SC
WHERE
    SA.STUDENT_NAME != SB.STUDENT_NAME
    AND SA.STUDENT_NAME != SC.STUDENT_NAME
    AND SB.STUDENT_NAME != SC.STUDENT_NAME
    AND SA.STUDENT_ID != SB.STUDENT_ID
    AND SA.STUDENT_ID != SC.STUDENT_ID
    AND SB.STUDENT_ID != SC.STUDENT_ID;
--------------------------------
SELECT
    S1.STUDENT_ID AS STUDENT_ID1,
    S2.STUDENT_ID AS STUDENT_ID2,
    S3.STUDENT_ID AS STUDENT_ID3
FROM
    SCHOOLA S1
JOIN
    SCHOOLB S2 ON S1.STUDENT_NAME != S2.STUDENT_NAME AND S1.STUDENT_ID != S2.STUDENT_ID
JOIN
    SCHOOLC S3 ON S2.STUDENT_NAME != S3.STUDENT_NAME AND S1.STUDENT_NAME != S3.STUDENT_NAME AND S1.STUDENT_ID != S3.STUDENT_ID AND S2.STUDENT_ID != S3.STUDENT_ID
ORDER BY
    STUDENT_ID1, STUDENT_ID2, STUDENT_ID3;
```
---
### 1633. Percentage of Users Attended a Contest
```sql
SELECT
    CONTEST_ID,
    ROUND(COUNT(USER_ID) * 100.0 / (SELECT COUNT(*) FROM USERS), 2) AS PERCENTAGE
FROM
    REGISTER
GROUP BY
    CONTEST_ID
ORDER BY
    PERCENTAGE DESC, CONTEST_ID;
```
---
### 1661. Average Time of Process per Machine
```sql
SELECT
    A1.MACHINE_ID,
    ROUND(AVG(CAST(A2.TIMESTAMP AS DECIMAL(10, 3)) - CAST(A1.TIMESTAMP AS DECIMAL(10, 3))), 3) AS PROCESSING_TIME
FROM
    ACTIVITY A1
JOIN
    ACTIVITY A2 ON A1.MACHINE_ID = A2.MACHINE_ID
    AND A1.PROCESS_ID = A2.PROCESS_ID
    AND A1.ACTIVITY_TYPE = 'START'
    AND A2.ACTIVITY_TYPE = 'END'
GROUP BY
    A1.MACHINE_ID;
```
---
### 1667. Fix Names in a Table
```sql
SELECT
    USER_ID,
    UPPER(LEFT(NAME, 1)) + LOWER(SUBSTRING(NAME, 2, LEN(NAME))) AS NAME
FROM
    USERS
ORDER BY
    USER_ID;
```
---
### 1677. Product's Worth Over Invoices
```sql
SELECT
  PRODUCT.NAME,
  ISNULL(SUM(I.REST), 0) AS REST,
  ISNULL(SUM(I.PAID), 0) AS PAID,
  ISNULL(SUM(I.CANCELED), 0) AS CANCELED,
  ISNULL(SUM(I.REFUNDED), 0) AS REFUNDED
FROM PRODUCT P
LEFT JOIN INVOICE I
ON I.PRODUCT_ID = P.PRODUCT_ID
GROUP BY 1
ORDER BY 1;
```
---
### 1683. Invalid Tweets
```sql
SELECT
    TWEET_ID
FROM
    TWEETS
WHERE
    LEN(CONTENT) > 15;
```
---
### 1693. Daily Leads and Partners
```sql
SELECT
    DATE_ID,
    MAKE_NAME,
    COUNT(DISTINCT LEAD_ID) AS UNIQUE_LEADS,
    COUNT(DISTINCT PARTNER_ID) AS UNIQUE_PARTNERS
FROM
    DAILYSALES
GROUP BY
    DATE_ID,
    MAKE_NAME;
```
---
### 1729. Find Followers Count
```sql
SELECT
    USER_ID,
    COUNT(FOLLOWER_ID) AS FOLLOWERS_COUNT
FROM
    FOLLOWERS
GROUP BY
    USER_ID
ORDER BY
    USER_ID;
```
---
### 1731. The Number of Employees Which Report to Each Employee
```sql
SELECT
    M.EMPLOYEE_ID,
    M.NAME,
    COUNT(R.EMPLOYEE_ID) AS REPORTS_COUNT,
    ROUND(AVG(CAST(R.AGE AS DECIMAL)), 0) AS AVERAGE_AGE
FROM
    EMPLOYEES M -- M FOR MANAGER
JOIN
    EMPLOYEES R ON M.EMPLOYEE_ID = R.REPORTS_TO -- R FOR REPORT
GROUP BY
    M.EMPLOYEE_ID,
    M.NAME
ORDER BY
    M.EMPLOYEE_ID;
```
---
### 1741. Find Total Time Spent by Each Employee
```sql
SELECT
    EVENT_DAY AS DAY,
    EMP_ID,
    SUM(OUT_TIME - IN_TIME) AS TOTAL_TIME
FROM
    EMPLOYEES
GROUP BY
    EVENT_DAY,
    EMP_ID;
```
---
### 175. Combine Two Tables
```sql
SELECT
    P.FIRSTNAME,
    P.LASTNAME,
    A.CITY,
    A.STATE
FROM
    PERSON P
LEFT JOIN
    ADDRESS A ON P.PERSONID = A.PERSONID;
```
---
### 1757. Recyclable and Low Fat Products
```sql
SELECT PRODUCT_ID
FROM PRODUCTS
WHERE LOW_FATS = 'Y' AND RECYCLABLE = 'Y';
```
---
### 1777. Product's Price for Each Store
```sql
SELECT
    PRODUCT_ID,
    MAX(CASE WHEN STORE = 'store1' THEN PRICE END) AS STORE1,
    MAX(CASE WHEN STORE = 'store2' THEN PRICE END) AS STORE2,
    MAX(CASE WHEN STORE = 'store3' THEN PRICE END) AS STORE3
FROM
    PRODUCTS
GROUP BY
    PRODUCT_ID;
```
---
### 1789. Primary Department for Each Employee
```sql
SELECT EMPLOYEE_ID, DEPARTMENT_ID
FROM EMPLOYEE
WHERE PRIMARY_FLAG = 'Y'
UNION
SELECT EMPLOYEE_ID, MIN(DEPARTMENT_ID) AS DEPARTMENT_ID 
FROM EMPLOYEE
GROUP BY EMPLOYEE_ID
HAVING COUNT(EMPLOYEE_ID) = 1;
-------------------------
SELECT E.EMPLOYEE_ID, 
COALESCE(
MAX(CASE WHEN E.PRIMARY_FLAG = 'Y' THEN E.DEPARTMENT_ID ELSE NULL END),
MIN(CASE WHEN E.PRIMARY_FLAG = 'N' THEN E.DEPARTMENT_ID ELSE NULL END)
) 
DEPARTMENT_ID 
FROM EMPLOYEE E
GROUP BY E.EMPLOYEE_ID
HAVING 
COUNT(CASE WHEN E.PRIMARY_FLAG = 'Y' THEN E.DEPARTMENT_ID ELSE NULL END) = 1 
OR COUNT(CASE WHEN E.PRIMARY_FLAG = 'N' THEN E.DEPARTMENT_ID ELSE NULL END) = 1
```
---
### 1795. Rearrange Products Table
```sql
SELECT PRODUCT_ID, 'store1' AS STORE, STORE1 AS PRICE
FROM PRODUCTS
WHERE STORE1 IS NOT NULL
UNION ALL
SELECT PRODUCT_ID, 'store2' AS STORE, STORE2 AS PRICE
FROM PRODUCTS
WHERE STORE2 IS NOT NULL
UNION ALL
SELECT PRODUCT_ID, 'store3' AS STORE, STORE3 AS PRICE
FROM PRODUCTS
WHERE STORE3 IS NOT NULL;
```
---
### 1809. Ad-Free Sessions
```sql
SELECT DISTINCT
    P.SESSION_ID
FROM
    PLAYBACK P
LEFT JOIN
    ADS A ON P.CUSTOMER_ID = A.CUSTOMER_ID
    AND A.TIMESTAMP BETWEEN P.START_TIME AND P.END_TIME
WHERE
    A.AD_ID IS NULL;
```
---
### 181. Employees Earning More Than Their Managers
```sql
SELECT
    E1.NAME AS EMPLOYEE
FROM
    EMPLOYEE E1
JOIN
    EMPLOYEE E2 ON E1.MANAGERID = E2.ID
WHERE
    E1.SALARY > E2.SALARY;
```
---
### 182. Duplicate Emails
```sql
SELECT
    EMAIL
FROM
    PERSON
GROUP BY
    EMAIL
HAVING
    COUNT(EMAIL) > 1;
```
---
### 1821. Find Customers With Positive Revenue this Year
```sql
SELECT
    CUSTOMER_ID
FROM
    CUSTOMERS
WHERE
    YEAR = 2021 AND REVENUE > 0;
```
---
### 183. Customers Who Never Order
```sql
SELECT
    C.NAME AS CUSTOMERS
FROM
    CUSTOMERS C
LEFT JOIN
    ORDERS O ON C.ID = O.CUSTOMERID
WHERE
    O.ID IS NULL;
```
---
### 1853. Convert Date Format
```sql
SELECT
    FORMAT(DAY, 'dddd, MMMM d, yyyy') AS DAY
FROM
    DAYS;
```
---
### 1873. Calculate Special Bonus
```sql
SELECT 
    EMPLOYEE_ID, 
    CASE 
        WHEN NAME LIKE 'M%' OR EMPLOYEE_ID % 2 = 0 THEN 0 
        ELSE SALARY 
    END AS BONUS
FROM EMPLOYEES
ORDER BY EMPLOYEE_ID;
```
---
### 1890. The Latest Login in
```sql
SELECT USER_ID, MAX(TIME_STAMP) LAST_STAMP
FROM LOGINS
WHERE YEAR(TIME_STAMP)=2020
GROUP BY USER_ID
```
---
### 1939. Users That Actively Request Confirmation Messages
```sql
SELECT DISTINCT C1.USER_ID
    FROM CONFIRMATIONS C1
    INNER JOIN CONFIRMATIONS C2
    WHERE C1.USER_ID = C2.USER_ID
    AND C1.TIME_STAMP < C2.TIME_STAMP
    AND TIMESTAMPDIFF(SECOND, C1.TIME_STAMP, C2.TIME_STAMP) <= 86400;
---------------
WITH
  USERTOTIMESTAMPDIFF AS (
    SELECT USER_ID,
      TIMESTAMPDIFF(
        SECOND,
        TIME_STAMP,
        LEAD(TIME_STAMP) OVER(
          PARTITION BY USER_ID
          ORDER BY TIME_STAMP
        )
      ) AS TIMESTAMP_DIFF
    FROM CONFIRMATIONS
  )
SELECT DISTINCT USER_ID
FROM USERTOTIMESTAMPDIFF
WHERE TIMESTAMP_DIFF <= 24 * 60 * 60;
```
---
### 196. Delete Duplicate Emails
```sql
DELETE P1 
FROM PERSON P1, PERSON P2
WHERE P1.EMAIL = P2.EMAIL 
AND P1.ID>P2.ID;
--------------
DELETE FROM PERSON 
WHERE ID NOT IN (
  SELECT MIN(ID)
  FROM PERSON 
  GROUP BY EMAIL 
);
```
---
### 1965. Employees With Missing Information
```sql
SELECT EMPLOYEE_ID 
FROM EMPLOYEES 
WHERE EMPLOYEE_ID NOT IN(SELECT EMPLOYEE_ID FROM SALARIES) 
UNION ALL 
SELECT EMPLOYEE_ID
FROM SALARIES 
WHERE EMPLOYEE_ID NOT IN (SELECT EMPLOYEE_ID FROM EMPLOYEES) 
ORDER BY EMPLOYEE_ID ASC
-----------------------------------------------
SELECT ISNULL(E.EMPLOYEE_ID,S.EMPLOYEE_ID) AS EMPLOYEE_ID
FROM EMPLOYEES E FULL JOIN SALARIES S
ON E.EMPLOYEE_ID  =S.EMPLOYEE_ID 
WHERE S.EMPLOYEE_ID IS NULL OR E.EMPLOYEE_ID IS NULL 
ORDER BY  EMPLOYEE_ID ASC 
```
---
### 197. Rising Temperature
```sql
WITH CTE AS (
  SELECT 
    *, 
    LAG(TEMPERATURE) OVER (ORDER BY RECORDDATE ASC) AS PREV_TEMP, 
    LAG(RECORDDATE) OVER (ORDER BY RECORDDATE ASC) AS PREV_DATE 
  FROM 
    WEATHER
) 
SELECT 
  ID 
FROM 
  CTE 
WHERE 
  TEMPERATURE > PREV_TEMP 
  AND DATEDIFF(DAY, PREV_DATE, RECORDDATE)= 1
```
---
### 1978. Employees Whose Manager Left the Company
```sql
SELECT E.EMPLOYEE_ID
FROM EMPLOYEES E
LEFT JOIN EMPLOYEES M
ON M.EMPLOYEE_ID =E.MANAGER_ID
WHERE E.SALARY < 30000 AND M.EMPLOYEE_ID IS NULL AND E.MANAGER_ID IS NOT NULL
ORDER BY EMPLOYEE_ID
```
---
### 2026. Low-Quality Problems
```sql
SELECT PROBLEM_ID
FROM PROBLEMS
WHERE LIKES / (LIKES + DISLIKES) < 0.6
ORDER BY PROBLEM_ID;
```
---
### 2072. The Winner University
```sql
WITH NYU_CTE AS (
    SELECT COUNT(*) AS CNT FROM NEWYORK WHERE SCORE >= 90
), CU_CTE AS (
    SELECT COUNT(*) AS CNT FROM CALIFORNIA WHERE SCORE >= 90
)
SELECT
    (CASE
     WHEN N.CNT > C.CNT THEN 'NEW YORK UNIVERSITY'
     WHEN N.CNT < C.CNT THEN 'CALIFORNIA UNIVERSITY'
     ELSE 'NO WINNER'
     END) AS WINNER
FROM NYU_CTE N, CU_CTE C;
```
---
### 2082. The Number of Rich Customers
```sql
SELECT
    COUNT(DISTINCT(CUSTOMER_ID)) AS RICH_COUNT
FROM
    STORE
WHERE
    AMOUNT > 500;
```
---
### 2205. The Number of Users That Are Eligible for Discount
```sql
SELECT 
  COUNT(DISTINCT USER_ID) AS USER_CNT 
FROM 
  PURCHASES 
WHERE 
  TIME_STAMP BETWEEN STARTDATE 
  AND ENDDATE 
  AND AMOUNT >= MINAMOUNT
```
---
### 2230. The Users That Are Eligible for Discount
```sql
CREATE PROCEDURE getUserIDs(startDate DATE, endDate DATE, minAmount INT)
BEGIN
  SELECT DISTINCT user_id
  FROM Purchases
  WHERE
    time_stamp BETWEEN startDate AND endDate
    AND amount >= minAmount
  ORDER BY 1;
END
```
---
### 2329. Product Sales Analysis V
```sql
SELECT
    S.USER_ID,
    SUM(S.QUANTITY * P.PRICE) AS SPENDING
FROM
    SALES AS S
JOIN
    PRODUCT AS P ON S.PRODUCT_ID = P.PRODUCT_ID
GROUP BY
    S.USER_ID
ORDER BY
    SPENDING DESC, S.USER_ID;
```
---
### 2339. All the Matches of the League
```sql
SELECT
    T1.TEAM_NAME AS HOME_TEAM,
    T2.TEAM_NAME AS AWAY_TEAM
FROM
    TEAMS AS T1
CROSS JOIN
    TEAMS AS T2
WHERE
    T1.TEAM_NAME != T2.TEAM_NAME;
```
---
### 2356. Number of Unique Subjects Taught by Each Teacher
```sql
SELECT
    TEACHER_ID,
    COUNT(DISTINCT SUBJECT_ID) AS CNT
FROM
    TEACHER
GROUP BY
    TEACHER_ID;
```
---
### 2377. Sort the Olympic Table
```sql
SELECT
  COUNTRY,
  GOLD_MEDALS,
  SILVER_MEDALS,
  BRONZE_MEDALS
FROM OLYMPIC
ORDER BY
  GOLD_MEDALS DESC,
  SILVER_MEDALS DESC,
  BRONZE_MEDALS DESC,
  COUNTRY;
```
---
### 2480. Form a Chemical Bond
```sql
SELECT
    A.SYMBOL AS METAL,
    B.SYMBOL AS NONMETAL
FROM
    ELEMENTS AS A
CROSS JOIN
    ELEMENTS AS B
WHERE
    A.TYPE = 'Metal' AND B.TYPE = 'Nonmetal';
```
---
### 2504. Concatenate the Name and the Profession
```sql
SELECT
    PERSON_ID,
    CONCAT(NAME, '(', SUBSTRING(PROFESSION, 1, 1), ')') AS NAME
FROM
    PERSON
ORDER BY
    PERSON_ID DESC;
```
---
### 2668. Find Latest Salaries
```sql
SELECT
    EMP_ID,
    FIRSTNAME,
    LASTNAME,
    MAX(SALARY) AS SALARY,
    DEPARTMENT_ID
FROM
    SALARY
GROUP BY
    EMP_ID,
    FIRSTNAME,
    LASTNAME,
    DEPARTMENT_ID
ORDER BY
    EMP_ID;
```
---
### 2669. Count Artist Occurrences On Spotify Ranking List
```sql
SELECT
    ARTIST,
    COUNT(1) AS OCCURRENCES
FROM SPOTIFY
GROUP BY ARTIST
ORDER BY OCCURRENCES DESC, ARTIST;
```
---
### 2687. Bikes Last Time Used
```sql
SELECT
    BIKE_NUMBER,
    MAX(END_TIME) AS END_TIME
FROM BIKES
GROUP BY BIKE_NUMBER
ORDER BY END_TIME DESC;
```
---
### 2837. Total Traveled Distance
```sql
SELECT
  U.USER_ID,
  U.NAME,
  SUM(ISNULL(R.DISTANCE, 0)) AS TOTAL_TRAVELED_DISTANCE
FROM
  USERS U
  LEFT JOIN RIDES R ON U.USER_ID = R.USER_ID
GROUP BY
  U.USER_ID,
  U.NAME
ORDER BY
  U.USER_ID;
```
---
### 2853. Highest Salaries Difference
```sql
SELECT
  MAX(CASE WHEN DEPARTMENT = 'Engineering' THEN SALARY ELSE 0 END) - MAX(CASE WHEN DEPARTMENT = 'Marketing' THEN SALARY ELSE 0 END) AS SALARY_DIFFERENCE
FROM
  SALARIES;
```
---
### 2985. Calculate Compressed Mean
```sql
SELECT
    ROUND(
        SUM(ITEM_COUNT * ORDER_OCCURRENCES) / SUM(ORDER_OCCURRENCES),
        2
    ) AS AVERAGE_ITEMS_PER_ORDER
FROM ORDERS;
```
---
### 2987. Find Expensive Cities
```sql
SELECT CITY
FROM LISTINGS
GROUP BY CITY
HAVING AVG(PRICE) > (SELECT AVG(PRICE) FROM LISTINGS)
ORDER BY 1
```
---
### 2990. Loan Types
```sql
SELECT
  USER_ID
FROM
  LOANS
GROUP BY
  USER_ID
HAVING
  SUM(CASE WHEN LOAN_TYPE = 'REFINANCE' THEN 1 ELSE 0 END) > 0
  AND SUM(CASE WHEN LOAN_TYPE = 'MORTGAGE' THEN 1 ELSE 0 END) > 0
ORDER BY
  USER_ID;
```
---
### 3051. Find Candidates for Data Scientist Position
```sql
SELECT CANDIDATE_ID
FROM CANDIDATES
WHERE SKILL IN ('Python', 'Tableau', 'PostgreSQL')
GROUP BY 1
HAVING COUNT(1) = 3
ORDER BY 1;
```
---
### 3053. Classifying Triangles by Lengths
```sql
SELECT
  CASE
    WHEN A + B <= C OR A + C <= B OR B + C <= A THEN 'Not a Triangle'
    WHEN A = B AND B = C THEN 'Equilateral'
    WHEN A = B OR B = C OR A = C THEN 'Isosceles'
    ELSE 'Scalene'
  END AS TRIANGLE_TYPE
FROM
  TRIANGLES;
```
---
### 3059. Find All Unique Email Domains
```sql
SELECT
  SUBSTRING(EMAIL, CHARINDEX('@', EMAIL) + 1, LEN(EMAIL)) AS EMAIL_DOMAIN,
  COUNT(*) AS COUNT
FROM
  EMAILS
WHERE
  EMAIL LIKE '%.com'
GROUP BY
  SUBSTRING(EMAIL, CHARINDEX('@', EMAIL) + 1, LEN(EMAIL))
ORDER BY
  EMAIL_DOMAIN;
```
---
### 3150. Invalid Tweets II
```sql
SELECT
  TWEET_ID
FROM
  TWEETS
WHERE
  LEN(CONTENT) > 140
  OR (LEN(CONTENT) - LEN(REPLACE(CONTENT, '@', ''))) > 3
  OR (LEN(CONTENT) - LEN(REPLACE(CONTENT, '#', ''))) > 3
ORDER BY
  TWEET_ID;
```
---
### 3172. Second Day Verification
```sql
SELECT
  E.USER_ID
FROM
  EMAILS E
  INNER JOIN TEXTS T ON E.EMAIL_ID = T.EMAIL_ID
WHERE
  T.SIGNUP_ACTION = 'Verified'
  AND DATEDIFF(DAY, E.SIGNUP_DATE, T.ACTION_DATE) = 1
ORDER BY
  E.USER_ID;
```
---
### 3198. Find Cities in Each State
```sql
SELECT
    STATE,
    STRING_AGG(CITY, ', ') WITHIN GROUP (ORDER BY CITY) AS CITIES
FROM CITIES
GROUP BY STATE
ORDER BY STATE;
```
---
### 3246. Premier League Table Ranking
```sql
SELECT
    TEAM_ID,
    TEAM_NAME,
    WINS * 3 + DRAWS AS POINTS,
    RANK() OVER (ORDER BY (WINS * 3 + DRAWS) DESC) AS POSITION
FROM TEAMSTATS
ORDER BY POINTS DESC, TEAM_NAME;
```
---
### 3358. Books with NULL Ratings
```sql
SELECT BOOK_ID, TITLE, AUTHOR, PUBLISHED_YEAR
FROM BOOKS
WHERE RATING IS NULL
ORDER BY 1;
```
---
### 3415. Find Products with Three Consecutive Digits
```sql
SELECT PRODUCT_ID, NAME
FROM PRODUCTS
WHERE
    (NAME LIKE '%[0-9][0-9][0-9]%'  -- CONTAINS AT LEAST THREE CONSECUTIVE DIGITS
    AND NAME NOT LIKE '%[0-9][0-9][0-9][0-9]%') -- BUT NOT FOUR OR MORE CONSECUTIVE DIGITS
    OR NAME LIKE '[0-9][0-9][0-9]%' -- STARTS WITH EXACTLY THREE DIGITS
    OR NAME LIKE '%[0-9][0-9][0-9]' -- ENDS WITH EXACTLY THREE DIGITS
ORDER BY PRODUCT_ID;
```
---
### 3436. Find Valid Emails
```sql
SELECT * FROM USERS
WHERE UPPER(EMAIL) LIKE '%@%.COM' AND UPPER(EMAIL) NOT LIKE '%[^0-9A-Z_]%@%.COM' AND UPPER(EMAIL) NOT LIKE '%@%[^A-Z]%.COM'
ORDER BY USER_ID
```
---
### 3465. Find Products with Valid Serial Numbers
```sql
SELECT *
FROM PRODUCTS
WHERE
    -- Condition 1: Matches serial numbers at the beginning of the string, followed by a space.
    -- Example: 'SN1234-5678 Some other text'
    DESCRIPTION LIKE 'SN[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9] %' COLLATE Latin1_General_BIN
    OR 
    -- Condition 2: Matches serial numbers that are in the middle of the string, with a space on either side.
    -- Example: 'Some other text SN1234-5678 Some other text'
    DESCRIPTION LIKE '% SN[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9] %' COLLATE Latin1_General_BIN
    OR 
    -- Condition 3: Matches serial numbers at the very end of the string, preceded by a space.
    -- Example: 'Some other text SN1234-5678'
    DESCRIPTION LIKE '% SN[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]' COLLATE Latin1_General_BIN
ORDER BY 1 ASC;
```
---
### 3570. Find Books with No Available Copies
```sql
WITH BORROWED_BOOK AS (
  SELECT 
    BOOK_ID, COUNT(*) AS CURRENT_BORROWERS 
  FROM 
    BORROWING_RECORDS 
  WHERE 
    RETURN_DATE IS NULL 
  GROUP BY 
    BOOK_ID
) 
SELECT 
  LB.BOOK_ID, TITLE, AUTHOR, GENRE, PUBLICATION_YEAR, CURRENT_BORROWERS 
FROM 
  LIBRARY_BOOKS LB 
  INNER JOIN BORROWED_BOOK BR ON LB.BOOK_ID = BR.BOOK_ID 
  AND (
    BR.CURRENT_BORROWERS - LB.TOTAL_COPIES
  ) = 0 
ORDER BY 
  6 DESC, 2 ASC
```
---
### 511. Game Play Analysis I
```sql
SELECT PLAYER_ID , MIN(EVENT_DATE) AS FIRST_LOGIN FROM ACTIVITY GROUP BY PLAYER_ID
```
---
### 512. Game Play Analysis II
```sql
SELECT
    PLAYER_ID,
    DEVICE_ID
FROM ACTIVITY
WHERE
    (PLAYER_ID, EVENT_DATE) IN (
        SELECT
            PLAYER_ID,
            MIN(EVENT_DATE) AS EVENT_DATE
        FROM ACTIVITY
        GROUP BY 1
    );
--------
WITH
    T AS (
        SELECT
            *,
            RANK() OVER (
                PARTITION BY PLAYER_ID
                ORDER BY EVENT_DATE
            ) AS RK
        FROM ACTIVITY
    )
SELECT PLAYER_ID, DEVICE_ID
FROM T
WHERE RK = 1;
```
---
### 577. Employee Bonus
```sql
SELECT NAME, BONUS FROM EMPLOYEE E LEFT JOIN BONUS B ON E.EMPID = B.EMPID WHERE B.BONUS < 1000 OR B.BONUS IS NULL
```
---
### 584. Find Customer Referee
```sql
SELECT NAME FROM CUSTOMER WHERE REFEREE_ID <> '2' OR REFEREE_ID IS NULL
```
---
### 586. Customer Placing the Largest Number of Orders
```sql
SELECT TOP 1 CUSTOMER_NUMBER
FROM ORDERS
GROUP BY CUSTOMER_NUMBER
ORDER BY COUNT(*) DESC;
```
---
### 595. Big Countries
```sql
SELECT NAME,POPULATION,AREA FROM WORLD WHERE POPULATION>=25000000 OR AREA>=3000000 
```
---
### 596. Classes With at Least 5 Students
```sql
SELECT CLASS
FROM COURSES
GROUP BY CLASS
HAVING COUNT(STUDENT) >= 5;
```
---
### 597. Friend Requests I: Overall Acceptance Rate
```sql
SELECT
    ROUND(
        ISNULL(
            (SELECT COUNT(*) FROM (SELECT DISTINCT ACCEPTER_ID, REQUESTER_ID FROM REQUESTACCEPTED) AS T1)
            * 1.0 / NULLIF((SELECT COUNT(*) FROM (SELECT DISTINCT SEND_TO_ID, SENDER_ID FROM FRIENDREQUEST) AS T2), 0),
            0
        ),
        2
    ) AS ACCEPT_RATE;
```
---
### 603. Consecutive Available Seats
```sql
WITH CINEMANEIGHBORS AS (
  SELECT
    *,
    LAG(FREE) OVER(ORDER BY SEAT_ID) AS PREV_FREE,
    LEAD(FREE) OVER(ORDER BY SEAT_ID) AS NEXT_FREE
  FROM CINEMA
)
SELECT SEAT_ID
FROM CINEMANEIGHBORS
WHERE FREE = 1
  AND (PREV_FREE = 1 OR NEXT_FREE = 1)
ORDER BY 1;
-----------------
WITH FREESEATSWITHGAP AS (
  SELECT
    SEAT_ID,
    SEAT_ID - ROW_NUMBER() OVER (ORDER BY SEAT_ID) AS GAP_KEY
  FROM CINEMA
  WHERE FREE = 1
)
, FREESEATCOUNTS AS (
  SELECT
    SEAT_ID,
    COUNT(*) OVER (PARTITION BY GAP_KEY) AS GROUP_COUNT
  FROM FREESEATSWITHGAP
)
SELECT
  SEAT_ID
FROM FREESEATCOUNTS
WHERE GROUP_COUNT >= 2
ORDER BY SEAT_ID;
```
---
### 607. Sales Person
```sql
SELECT S.NAME
FROM ORDERS O
INNER JOIN COMPANY C
  ON (O.COM_ID = C.COM_ID AND C.NAME = 'RED')
RIGHT JOIN SALESPERSON S
  ON S.SALES_ID = O.SALES_ID
WHERE O.SALES_ID IS NULL;
```
---
### 610. Triangle Judgement
```sql
SELECT
    *,
    CASE
        WHEN X + Y > Z AND X + Z > Y AND Y + Z > X THEN 'Yes'
        ELSE 'No'
    END AS TRIANGLE
FROM
    TRIANGLE;
```
---
### 613. Shortest Distance in a Line
```sql
SELECT MIN(P2.X - P1.X) AS SHORTEST
FROM
    POINT AS P1
    JOIN POINT AS P2 ON P1.X < P2.X;SELECT MIN(P2.X - P1.X) AS SHORTEST
FROM
    POINT AS P1
    JOIN POINT AS P2 ON P1.X < P2.X;
```
---
### 619. Biggest Single Number
```sql
WITH CTE AS (
  SELECT 
    NUM,COUNT(NUM) COUNTED 
  FROM 
    MYNUMBERS 
  GROUP BY 
    NUM 
  HAVING 
    COUNT(NUM) = 1
) 
SELECT 
  ISNULL(MAX(NUM), NULL) NUM 
FROM 
  CTE
```
---
### 620. Not Boring Movies
```sql
SELECT ID, MOVIE, DESCRIPTION, RATING FROM CINEMA WHERE DESCRIPTION <> 'boring' AND ID % 2 = 1 ORDER BY RATING DESC
```
---
# Medium
### 1045. Customers Who Bought All Products
```sql
WITH PRD_CNT AS (
    SELECT COUNT(DISTINCT PRODUCT_KEY) AS PC FROM PRODUCT
),
CST_CNT AS (
    SELECT CUSTOMER_ID ,COUNT(DISTINCT PRODUCT_KEY) AS CPC FROM CUSTOMER GROUP BY CUSTOMER_ID
)
SELECT CUSTOMER_ID FROM CST_CNT A INNER JOIN PRD_CNT B ON A.CPC = B.PC
```
---
### 1070. Product Sales Analysis III
```sql
```
---
### 1077. Project Employees III
```sql
```
---
### 1098. Unpopular Books
```sql
```
---
### 1107. New Users Daily Count
```sql
```
---
### 1112. Highest Grade For Each Student
```sql
```
---
### 1126. Active Businesses
```sql
```
---
### 1132. Reported Posts II
```sql
```
---
### 1149. Article Views II
```sql
```
---
### 1158. Market Analysis I
```sql
```
---
### 1164. Product Price at a Given Date
```sql
```
---
### 1174. Immediate Food Delivery II
```sql
```
---
### 1193. Monthly Transactions I
```sql
```
---
### 1204. Last Person to Fit in the Bus
```sql
```
---
### 1205. Monthly Transactions II
```sql
```
---
### 1212. Team Scores in Football Tournament
```sql
```
---
### 1264. Page Recommendations
```sql
```
---
### 1270. All People Report to the Given Manager
```sql
```
---
### 1285. Find the Start and End Number of Continuous Ranges
```sql
```
---
### 1308. Running Total for Different Genders
```sql
```
---
### 1321. Restaurant Growth
```sql
```
---
### 1341. Movie Rating
```sql
```
---
### 1355. Activity Participants
```sql
```
---
### 1364. Number of Trusted Contacts of a Customer
```sql
```
---
### 1393. Capital Gain/Loss
```sql
```
---
### 1398. Customers Who Bought Products A and B but Not C
```sql
```
---
### 1440. Evaluate Boolean Expression
```sql
```
---
### 1445. Apples & Oranges
```sql
```
---
### 1454. Active Users
```sql
```
---
### 1459. Rectangles Area
```sql
```
---
### 1468. Calculate Salaries
```sql
```
---
### 1501. Countries You Can Safely Invest In
```sql
```
---
### 1532. The Most Recent Three Orders
```sql
```
---
### 1549. The Most Recent Orders for Each Product
```sql
```
---
### 1555. Bank Account Summary
```sql
```
---
### 1596. The Most Frequently Ordered Products for Each Customer
```sql
```
---
### 1613. Find the Missing IDs
```sql
```
---
### 1699. Number of Calls Between Two Persons
```sql
```
---
### 1709. Biggest Window Between Visits
```sql
```
---
### 1715. Count Apples and Oranges
```sql
```
---
### 1747. Leetflex Banned Accounts
```sql
```
---
### 176. Second Highest Salary
```sql
```
---
### 177. Nth Highest Salary
```sql
```
---
### 178. Rank Scores
```sql
```
---
### 1783. Grand Slam Titles
```sql
```
---
### 180. Consecutive Numbers
```sql
```
---
### 1811. Find Interview Candidates
```sql
```
---
### 1831. Maximum Transaction Each Day
```sql
```
---
### 184. Department Highest Salary
```sql
```
---
### 1841. League Statistics
```sql
```
---
### 1843. Suspicious Bank Accounts
```sql
```
---
### 1867. Orders With Maximum Quantity Above Average
```sql
```
---
### 1875. Group Employees of the Same Salary
```sql
```
---
### 1907. Count Salary Categories
```sql
```
---
### 1934. Confirmation Rate
```sql
```
---
### 1949. Strong Friendship
```sql
```
---
### 1951. All the Pairs With the Maximum Number of Common Followers
```sql
```
---
### 1988. Find Cutoff Score for Each School
```sql
```
---
### 1990. Count the Number of Experiments
```sql
```
---
### 2020. Number of Accounts That Did Not Stream
```sql
```
---
### 2041. Accepted Candidates From the Interviews
```sql
```
---
### 2051. The Category of Each Member in the Store
```sql
```
---
### 2066. Account Balance
```sql
```
---
### 2084. Drop Type 1 Orders for Customers With Type 0 Orders
```sql
```
---
### 2112. The Airport With the Most Traffic
```sql
```
---
### 2142. The Number of Passengers in Each Bus I
```sql
```
---
### 2159. Order Two Columns Independently
```sql
```
---
### 2175. The Change in Global Rankings
```sql
```
---
### 2228. Users With Two Purchases Within Seven Days
```sql
```
---
### 2238. Number of Times a Driver Was a Passenger
```sql
```
---
### 2292. Products With Three or More Orders in Two Consecutive Years
```sql
```
---
### 2298. Tasks Count in the Weekend
```sql
```
---
### 2308. Arrange Table by Gender
```sql
```
---
### 2314. The First Day of the Maximum Recorded Degree in Each City
```sql
```
---
### 2324. Product Sales Analysis IV
```sql
```
---
### 2346. Compute the Rank as a Percentage
```sql
```
---
### 2372. Calculate the Influence of Each Salesperson
```sql
```
---
### 2388. Change Null Values in a Table to the Previous Value
```sql
```
---
### 2394. Employees With Deductions
```sql
```
---
### 2686. Immediate Food Delivery III
```sql
```
---
### 2688. Find Active Users
```sql
```
---
### 2738. Count Occurrences in Text
```sql
```
---
### 2783. Flight Occupancy and Waitlist Analysis
```sql
```
---
### 2820. Election Results
```sql
```
---
### 2854. Rolling Average Steps
```sql
```
---
### 2893. Calculate Orders Within Each Interval
```sql
```
---
### 2922. Market Analysis III
```sql
```
---
### 2978. Symmetric Coordinates
```sql
```
---
### 2984. Find Peak Calling Hours for Each City
```sql
```
---
### 2986. Find Third Transaction
```sql
```
---
### 2988. Manager of the Largest Department
```sql
```
---
### 2989. Class Performance
```sql
```
---
### 2993. Friday Purchases I
```sql
```
---
### 3050. Pizza Toppings Cost Analysis
```sql
```
---
### 3054. Binary Tree Nodes
```sql
```
---
### 3055. Top Percentile Fraud
```sql
```
---
### 3056. Snaps Analysis
```sql
```
---
### 3058. Friends With No Mutual Friends
```sql
```
---
### 3087. Find Trending Hashtags
```sql
```
---
### 3089. Find Bursty Behavior
```sql
```
---
### 3118. Friday Purchase III
```sql
```
---
### 3124. Find Longest Calls
```sql
```
---
### 3126. Server Utilization Time
```sql
```
---
### 3140. Consecutive Available Seats II
```sql
```
---
### 3166. Calculate Parking Fees and Duration
```sql
```
---
### 3182. Find Top Scoring Students
```sql
```
---
### 3204. Bitwise User Permissions Analysis
```sql
```
---
### 3220. Odd and Even Transactions
```sql
```
---
### 3230. Customer Purchasing Behavior Analysis
```sql
```
---
### 3252. Premier League Table Ranking II
```sql
```
---
### 3262. Find Overlapping Shifts
```sql
```
---
### 3278. Find Candidates for Data Scientist Position II
```sql
```
---
### 3293. Calculate Product Final Price
```sql
```
---
### 3308. Find Top Performing Driver
```sql
```
---
### 3322. Premier League Table Ranking III
```sql
```
---
### 3328. Find Cities in Each State II
```sql
```
---
### 3338. Second Highest Salary II
```sql
```
---
### 3421. Find Students Who Improved
```sql
```
---
### 3475. DNA Pattern Recognition
```sql
```
---
### 3497. Analyze Subscription Conversion
```sql
```
---
### 3521. Find Product Recommendation Pairs
```sql
```
---
### 3564. Seasonal Sales Analysis
```sql
```
---
### 3580. Find Consistently Improving Employees
```sql
```
---
### 3586. Find COVID Recovery Patients
```sql
```
---
### 3601. Find Drivers with Improved Fuel Efficiency
```sql
```
---
### 3611. Find Overbooked Employees
```sql
```
---
### 3626. Find Stores with Inventory Imbalance
```sql
```
---
### 534. Game Play Analysis III
```sql
```
---
### 550. Game Play Analysis IV
```sql
```
---
### 570. Managers with at Least 5 Direct Reports
```sql
```
---
### 574. Winning Candidate
```sql
```
---
### 578. Get Highest Answer Rate Question
```sql
```
---
### 580. Count Student Number in Departments
```sql
```
---
### 585. Investments in
```sql
```
---
### 602. Friend Requests II: Who Has the Most Friends
```sql
```
---
### 608. Tree Node
```sql
```
---
### 612. Shortest Distance in a Plane
```sql
```
---
### 614. Second Degree Follower
```sql
```
---
### 626. Exchange Seats
```sql
```
---
### 627. Swap Salary
```sql
UPDATE SALARY SET SEX = CASE WHEN SEX = 'm' THEN 'f' ELSE 'm' END;
```
---
# Hard
### 1097. Game Play Analysis V
```sql
```
---
### 1127. User Purchase Platform
```sql
```
---
### 1159. Market Analysis II
```sql
```
---
### 1194. Tournament Winners
```sql
```
---
### 1225. Report Contiguous Dates
```sql
```
---
### 1336. Number of Transactions per Visit
```sql
```
---
### 1369. Get the Second Most Recent Activity
```sql
```
---
### 1384. Total Sales Amount by Year
```sql
```
---
### 1412. Find the Quiet Students in All Exams
```sql
```
---
### 1479. Sales by Day of the Week
```sql
```
---
### 1635. Hopper Company Queries I
```sql
```
---
### 1645. Hopper Company Queries II
```sql
```
---
### 1651. Hopper Company Queries III
```sql
```
---
### 1767. Find the Subtasks That Did Not Execute
```sql
```
---
### 185. Department Top Three Salaries
```sql
```
---
### 1892. Page Recommendations II
```sql
```
---
### 1917. Leetcodify Friends Recommendations
```sql
```
---
### 1919. Leetcodify Similar Friends
```sql
```
---
### 1972. First and Last Call On the Same Day
```sql
```
---
### 2004. The Number of Seniors and Juniors to Join the Company
```sql
```
---
### 2010. The Number of Seniors and Juniors to Join the Company II
```sql
```
---
### 2118. Build the Equation
```sql
```
---
### 2153. The Number of Passengers in Each Bus II
```sql
```
---
### 2173. Longest Winning Streak
```sql
```
---
### 2199. Finding the Topic of Each Post
```sql
```
---
### 2252. Dynamic Pivoting of a Table
```sql
```
---
### 2253. Dynamic Unpivoting of a Table
```sql
```
---
### 2362. Generate the Invoice
```sql
```
---
### 2474. Customers With Strictly Increasing Purchases
```sql
```
---
### 2494. Merge Overlapping Events in the Same Hall
```sql
```
---
### 262. Trips and Users
```sql
```
---
### 2701. Consecutive Transactions with Increasing Amounts
```sql
```
---
### 2720. Popularity Percentage
```sql
```
---
### 2752. Customers with Maximum Number of Transactions on Consecutive Days
```sql
```
---
### 2793. Status of Flight Tickets
```sql
```
---
### 2991. Top Three Wineries
```sql
```
---
### 2994. Friday Purchases II
```sql
```
---
### 2995. Viewers Turned Streamers
```sql
```
---
### 3052. Maximize Items
```sql
```
---
### 3057. Employees Project Allocation
```sql
```
---
### 3060. User Activities within Time Bounds
```sql
```
---
### 3061. Calculate Trapping Rain Water
```sql
```
---
### 3103. Find Trending Hashtags II
```sql
```
---
### 3156. Employee Task Duration and Concurrent Tasks
```sql
```
---
### 3188. Find Top Scoring Students II
```sql
```
---
### 3214. Year on Year Growth Rate
```sql
```
---
### 3236. CEO Subordinate Hierarchy
```sql
```
---
### 3268. Find Overlapping Shifts II
```sql
```
---
### 3368. First Letter Capitalization
```sql
```
---
### 3374. First Letter Capitalization II
```sql
```
---
### 3384. Team Dominance by Pass Success
```sql
```
---
### 3390. Longest Team Pass Streak
```sql
```
---
### 3401. Find Circular Gift Exchange Chains
```sql
```
---
### 3451. Find Invalid IP Addresses
```sql
```
---
### 3482. Analyze Organization Hierarchy
```sql
```
---
### 3554. Find Category Recommendation Pairs
```sql
```
---
### 3617. Find Students with Study Spiral Pattern
```sql
```
---
### 569. Median Employee Salary
```sql
```
---
### 571. Find Median Given Frequency of Numbers
```sql
```
---
### 579. Find Cumulative Salary of an Employee
```sql
```
---
### 601. Human Traffic of Stadium
```sql
```
---
### 615. Average Salary: Departments VS Company
```sql
```
---
### 618. Students Report By Geography
```sql
```
---
