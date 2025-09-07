# [1045. Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/)
```sql
WITH PRD_CNT AS (
    SELECT COUNT(DISTINCT PRODUCT_KEY) AS PC FROM PRODUCT
),
CST_CNT AS (
    SELECT CUSTOMER_ID ,COUNT(DISTINCT PRODUCT_KEY) AS CPC FROM CUSTOMER GROUP BY CUSTOMER_ID
)
SELECT CUSTOMER_ID FROM CST_CNT A INNER JOIN PRD_CNT B ON A.CPC = B.PC
```

# [1070. Product Sales Analysis III](https://leetcode.com/problems/product-sales-analysis-iii/)
```sql
WITH EARLY_YR AS (
  SELECT 
    PRODUCT_ID, 
    MIN(YEAR) OVER (PARTITION BY PRODUCT_ID) AS FIRST_YEAR, 
    QUANTITY, 
    PRICE, 
    YEAR 
  FROM 
    SALES
) 
SELECT 
  PRODUCT_ID, FIRST_YEAR, QUANTITY, PRICE 
FROM 
  EARLY_YR 
WHERE 
  FIRST_YEAR = YEAR
```

# [1077. Project Employees III](https://leetcode.com/problems/project-employees-iii/)
```sql
SELECT
    PROJECT_ID,
    EMPLOYEE_ID
FROM (
    SELECT
        P.PROJECT_ID,
        P.EMPLOYEE_ID,
        DENSE_RANK() OVER(PARTITION BY P.PROJECT_ID ORDER BY E.EXPERIENCE_YEARS DESC) 
        AS MAXEXP
    FROM PROJECT AS P JOIN EMPLOYEE AS E
    ON P.EMPLOYEE_ID = E.EMPLOYEE_ID
    ) 
WHERE MAXEXP = 1
```

# [1098. Unpopular Books](https://leetcode.com/problems/unpopular-books/)
```sql
SELECT
  B.BOOK_ID,
  ANY_VALUE(B.NAME) AS NAME
FROM BOOKS B
LEFT JOIN ORDERS O
  ON (
    B.BOOK_ID = O.BOOK_ID
    AND O.DISPATCH_DATE BETWEEN '2018-06-23' AND '2019-06-23'
  )
WHERE
  DATEDIFF(DAY, B.AVAILABLE_FROM, '2019-06-23') > 30
GROUP BY
  B.BOOK_ID
HAVING
  ISNULL(SUM(O.QUANTITY), 0) < 10;
```

# [1107. New Users Daily Count](https://leetcode.com/problems/new-users-daily-count/)
```sql
WITH T AS (
  SELECT
    USER_ID,
    MIN(ACTIVITY_DATE) OVER (PARTITION BY USER_ID) AS LOGIN_DATE
  FROM TRAFFIC
  WHERE
    ACTIVITY = 'LOGIN'
)
SELECT
  LOGIN_DATE,
  COUNT(DISTINCT USER_ID) AS USER_COUNT
FROM T
WHERE
  DATEDIFF(DAY, LOGIN_DATE, '2019-06-30') <= 90
GROUP BY
  LOGIN_DATE;
```

# [1112. Highest Grade For Each Student](https://leetcode.com/problems/highest-grade-for-each-student/)
```sql
WITH T AS (
    SELECT
        STUDENT_ID,
        COURSE_ID,
        GRADE,
        RANK() OVER (
            PARTITION BY STUDENT_ID
            ORDER BY GRADE DESC, COURSE_ID
        ) AS RK
    FROM ENROLLMENTS
)
SELECT
    STUDENT_ID,
    COURSE_ID,
    GRADE
FROM T
WHERE
    RK = 1
ORDER BY
    STUDENT_ID;
```

# [1126. Active Businesses](https://leetcode.com/problems/active-businesses/)
```sql
SELECT
  T1.BUSINESS_ID
FROM
  EVENTS AS T1
  JOIN (
    SELECT
      EVENT_TYPE,
      AVG(OCCURENCES) AS OCCURENCES
    FROM EVENTS
    GROUP BY
      EVENT_TYPE
  ) AS T2
    ON T1.EVENT_TYPE = T2.EVENT_TYPE
WHERE
  T1.OCCURENCES > T2.OCCURENCES
GROUP BY
  T1.BUSINESS_ID
HAVING
  COUNT(*) > 1;
```

# [1132. Reported Posts II](https://leetcode.com/problems/reported-posts-ii/)
```sql
WITH T AS (
    SELECT
        CAST(COUNT(DISTINCT T2.POST_ID) AS FLOAT) / NULLIF(COUNT(DISTINCT T1.POST_ID), 0) * 100 AS PERCENT
    FROM
        ACTIONS AS T1
        LEFT JOIN REMOVALS AS T2
            ON T1.POST_ID = T2.POST_ID
    WHERE
        T1.EXTRA = 'spam'
    GROUP BY
        T1.ACTION_DATE
)
SELECT
    ROUND(AVG(PERCENT), 2) AS AVERAGE_DAILY_PERCENT
FROM
    T;
```

# [1149. Article Views II](https://leetcode.com/problems/article-views-ii/)
```sql
SELECT
  DISTINCT VIEWER_ID AS ID
FROM VIEWS
GROUP BY
  VIEWER_ID,
  VIEW_DATE
HAVING
  COUNT(DISTINCT ARTICLE_ID) > 1
ORDER BY
  VIEWER_ID;
```

# [1158. Market Analysis I](https://leetcode.com/problems/market-analysis-i/)
```sql
SELECT 
  USER_ID AS BUYER_ID, 
  JOIN_DATE, 
  COUNT(ORDER_ID) AS ORDERS_IN_2019 
FROM 
  USERS U 
  LEFT JOIN ORDERS O ON U.USER_ID = O.BUYER_ID 
  AND YEAR(O.ORDER_DATE) = 2019 
GROUP BY 
  USER_ID, 
  JOIN_DATE
ORDER BY 1
```

# [1164. Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/)
```sql
WITH LATESTPRICES AS (
    SELECT
        PRODUCT_ID,
        NEW_PRICE AS PRICE,
        ROW_NUMBER() OVER (PARTITION BY PRODUCT_ID ORDER BY CHANGE_DATE DESC) AS RN
    FROM
        PRODUCTS
    WHERE
        CHANGE_DATE <= '2019-08-16'
),
ALLPRODUCTS AS (
    SELECT DISTINCT PRODUCT_ID
    FROM PRODUCTS
)
SELECT
    AP.PRODUCT_ID,
    COALESCE(LP.PRICE, 10) AS PRICE
FROM
    ALLPRODUCTS AP
LEFT JOIN
    LATESTPRICES LP ON AP.PRODUCT_ID = LP.PRODUCT_ID AND LP.RN = 1;
```

# [1174. Immediate Food Delivery II](https://leetcode.com/problems/immediate-food-delivery-ii/)
```sql
WITH FIRSTORDERS AS (
    SELECT
        CUSTOMER_ID,
        ORDER_DATE,
        CUSTOMER_PREF_DELIVERY_DATE,
        ROW_NUMBER() OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE) AS RN
    FROM
        DELIVERY
)
SELECT
    ROUND(SUM(CASE WHEN ORDER_DATE = CUSTOMER_PREF_DELIVERY_DATE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS IMMEDIATE_PERCENTAGE
FROM
    FIRSTORDERS
WHERE
    RN = 1;
```

# [1193. Monthly Transactions I](https://leetcode.com/problems/monthly-transactions-i/)
```sql
SELECT
    FORMAT(TRANS_DATE, 'yyyy-MM') AS MONTH,
    COUNTRY,
    COUNT(ID) AS TRANS_COUNT,
    SUM(CASE WHEN STATE = 'approved' THEN 1 ELSE 0 END) AS APPROVED_COUNT,
    SUM(AMOUNT) AS TRANS_TOTAL_AMOUNT,
    SUM(CASE WHEN STATE = 'approved' THEN AMOUNT ELSE 0 END) AS APPROVED_TOTAL_AMOUNT
FROM
    TRANSACTIONS
GROUP BY
    FORMAT(TRANS_DATE, 'yyyy-MM'),
    COUNTRY;
```

# [1204. Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/)
```sql
WITH RN_SM AS (
  SELECT 
    *, 
    SUM(WEIGHT) OVER (ORDER BY TURN ASC) AS RUN_SUM 
  FROM 
    QUEUE
) 
SELECT 
  TOP 1 PERSON_NAME 
FROM 
  RN_SM 
WHERE 
  RUN_SUM <= 1000 
ORDER BY 
  RUN_SUM DESC
```

# [1205. Monthly Transactions II](https://leetcode.com/problems/monthly-transactions-ii/)
```sql
WITH T AS (
    SELECT ID, COUNTRY, STATE, AMOUNT, TRANS_DATE
    FROM TRANSACTIONS
    UNION ALL
    SELECT T.ID, T.COUNTRY, 'chargeback' AS STATE, T.AMOUNT, C.TRANS_DATE
    FROM
        TRANSACTIONS AS T
        JOIN CHARGEBACKS AS C ON T.ID = C.TRANS_ID
)
SELECT
    FORMAT(TRANS_DATE, 'yyyy-MM') AS MONTH,
    COUNTRY,
    SUM(CASE WHEN STATE = 'approved' THEN 1 ELSE 0 END) AS APPROVED_COUNT,
    SUM(CASE WHEN STATE = 'approved' THEN AMOUNT ELSE 0 END) AS APPROVED_AMOUNT,
    SUM(CASE WHEN STATE = 'chargeback' THEN 1 ELSE 0 END) AS CHARGEBACK_COUNT,
    SUM(CASE WHEN STATE = 'chargeback' THEN AMOUNT ELSE 0 END) AS CHARGEBACK_AMOUNT
FROM T
GROUP BY
    FORMAT(TRANS_DATE, 'yyyy-MM'),
    COUNTRY
HAVING
    SUM(CASE WHEN STATE = 'approved' THEN AMOUNT ELSE 0 END) > 0 OR
    SUM(CASE WHEN STATE = 'chargeback' THEN AMOUNT ELSE 0 END) > 0;
```

# [1212. Team Scores in Football Tournament](https://leetcode.com/problems/team-scores-in-football-tournament/)
```sql
WITH TWOWAYMATCHES AS (
    SELECT
        HOST_TEAM AS TEAM_ID,
        HOST_GOALS AS GOALS,
        GUEST_GOALS AS OPPONENT_GOALS
    FROM
        MATCHES
    UNION ALL
    SELECT
        GUEST_TEAM AS TEAM_ID,
        GUEST_GOALS AS GOALS,
        HOST_GOALS AS OPPONENT_GOALS
    FROM
        MATCHES
)
SELECT
    T.TEAM_ID,
    T.TEAM_NAME,
    SUM(
        CASE
            WHEN M.GOALS > M.OPPONENT_GOALS THEN 3
            WHEN M.GOALS = M.OPPONENT_GOALS THEN 1
            ELSE 0
        END
    ) AS NUM_POINTS
FROM
    TEAMS AS T
LEFT JOIN
    TWOWAYMATCHES AS M ON T.TEAM_ID = M.TEAM_ID
GROUP BY
    T.TEAM_ID,
    T.TEAM_NAME
ORDER BY
    NUM_POINTS DESC,
    T.TEAM_ID;
```

# [1264. Page Recommendations](https://leetcode.com/problems/page-recommendations/)
```sql
WITH
  USERTOFRIENDS AS (
    SELECT USER1_ID AS USER_ID, USER2_ID AS FRIEND_ID FROM FRIENDSHIP
    UNION ALL
    SELECT USER2_ID AS USER_ID, USER1_ID AS FRIEND_ID FROM FRIENDSHIP
  )
SELECT FRIENDLIKES.PAGE_ID AS RECOMMENDED_PAGE
FROM USERTOFRIENDS
LEFT JOIN LIKES AS FRIENDLIKES
  ON (USERTOFRIENDS.FRIEND_ID = FRIENDLIKES.USER_ID)
LEFT JOIN LIKES AS USERLIKES
  ON (
    USERTOFRIENDS.USER_ID = USERLIKES.USER_ID
    AND FRIENDLIKES.PAGE_ID = USERLIKES.PAGE_ID)
WHERE
  USERTOFRIENDS.USER_ID = 1
  AND USERLIKES.PAGE_ID IS NULL
  AND FRIENDLIKES.PAGE_ID IS NOT NULL
GROUP BY 1;
```

# [1270. All People Report to the Given Manager](https://leetcode.com/problems/all-people-report-to-the-given-manager/)
```sql
SELECT
    EMPLOYEE.EMPLOYEE_ID
FROM
    EMPLOYEES AS EMPLOYEE
INNER JOIN
    EMPLOYEES AS DIRECTMANAGER ON (EMPLOYEE.MANAGER_ID = DIRECTMANAGER.EMPLOYEE_ID)
INNER JOIN
    EMPLOYEES AS SKIPMANAGER ON (DIRECTMANAGER.MANAGER_ID = SKIPMANAGER.EMPLOYEE_ID)
WHERE
    SKIPMANAGER.MANAGER_ID = 1 AND EMPLOYEE.EMPLOYEE_ID != 1;
```

# [1285. Find the Start and End Number of Continuous Ranges](https://leetcode.com/problems/find-the-start-and-end-number-of-continuous-ranges/)
```sql
WITH LOGTOROWNUMBER AS (
    SELECT
        LOG_ID,
        ROW_NUMBER() OVER(ORDER BY LOG_ID) AS ROW_NUMBER
    FROM LOGS
)
SELECT
    MIN(LOG_ID) AS START_ID,
    MAX(LOG_ID) AS END_ID
FROM LOGTOROWNUMBER
GROUP BY LOG_ID - ROW_NUMBER;
```

# [1308. Running Total for Different Genders](https://leetcode.com/problems/running-total-for-different-genders/)
```sql
SELECT
    GENDER,
    DAY,
    SUM(SCORE_POINTS) OVER(
        PARTITION BY GENDER
        ORDER BY DAY
    ) AS TOTAL
FROM SCORES
ORDER BY 1, 2;
```

# [1321. Restaurant Growth](https://leetcode.com/problems/restaurant-growth/)
```sql
SELECT 
	VISITED_ON, 
    SUM(SUM(AMOUNT)) OVER(ORDER BY VISITED_ON ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)   AS'AMOUNT',
    ROUND(CAST(SUM(SUM(AMOUNT)) OVER(ORDER BY VISITED_ON ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS FLOAT)/7.0 ,2) AS'AVERAGE_AMOUNT' 
FROM CUSTOMER 
GROUP BY VISITED_ON
ORDER BY VISITED_ON
OFFSET 6 ROWS  
```

# [1341. Movie Rating](https://leetcode.com/problems/movie-rating/)
```sql
WITH THEMOSTACTIVEUSER AS (
    SELECT TOP 1
        U.NAME
    FROM
        USERS AS U
        INNER JOIN MOVIERATING AS MR ON U.USER_ID = MR.USER_ID
    GROUP BY
        U.USER_ID,
        U.NAME
    ORDER BY
        COUNT(*) DESC,
        U.NAME
),
THEBESTMOVIEFEBRUARY AS (
    SELECT TOP 1
        M.TITLE
    FROM
        MOVIES AS M
        INNER JOIN MOVIERATING AS MR ON M.MOVIE_ID = MR.MOVIE_ID
    WHERE
        MR.CREATED_AT >= '2020-02-01' AND MR.CREATED_AT < '2020-03-01'
    GROUP BY
        M.MOVIE_ID,
        M.TITLE
    ORDER BY
        AVG(CAST(MR.RATING AS DECIMAL(10,2))) DESC,
        M.TITLE
)
SELECT NAME AS RESULTS FROM THEMOSTACTIVEUSER
UNION ALL
SELECT TITLE FROM THEBESTMOVIEFEBRUARY;
```

# [1355. Activity Participants](https://leetcode.com/problems/activity-participants/)
```sql
WITH
    T AS (
        SELECT ACTIVITY, COUNT(1) AS CNT
        FROM FRIENDS
        GROUP BY ACTIVITY
    )
SELECT ACTIVITY
FROM T
WHERE CNT > (SELECT MIN(CNT) FROM T) AND CNT < (SELECT MAX(CNT) FROM T);
```

# [1364. Number of Trusted Contacts of a Customer](https://leetcode.com/problems/number-of-trusted-contacts-of-a-customer/)
```sql
SELECT
    T1.INVOICE_ID,
    T2.CUSTOMER_NAME,
    T1.PRICE,
    COUNT(DISTINCT T3.CONTACT_EMAIL) AS CONTACTS_CNT,
    COUNT(DISTINCT T4.EMAIL) AS TRUSTED_CONTACTS_CNT
FROM
    INVOICES AS T1
    LEFT JOIN CUSTOMERS AS T2 ON T1.USER_ID = T2.CUSTOMER_ID
    LEFT JOIN CONTACTS AS T3 ON T1.USER_ID = T3.USER_ID
    LEFT JOIN CUSTOMERS AS T4 ON T3.CONTACT_EMAIL = T4.EMAIL
GROUP BY
    T1.INVOICE_ID,
    T2.CUSTOMER_NAME,
    T1.PRICE
ORDER BY
    T1.INVOICE_ID;
```

# [1393. Capital Gain/Loss](https://leetcode.com/problems/capital-gainloss/)
```sql
SELECT STOCK_NAME, SUM(
    CASE
        WHEN OPERATION = 'buy' THEN -PRICE
        ELSE PRICE
    END
) AS CAPITAL_GAIN_LOSS
FROM STOCKS
GROUP BY STOCK_NAME
```

# [1398. Customers Who Bought Products A and B but Not C](https://leetcode.com/problems/customers-who-bought-products-a-and-b-but-not-c/)
```sql
SELECT
    C.CUSTOMER_ID,
    C.CUSTOMER_NAME
FROM
    CUSTOMERS AS C
    INNER JOIN ORDERS AS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
GROUP BY
    C.CUSTOMER_ID,
    C.CUSTOMER_NAME
HAVING
    SUM(CASE WHEN O.PRODUCT_NAME = 'A' THEN 1 ELSE 0 END) > 0
    AND SUM(CASE WHEN O.PRODUCT_NAME = 'B' THEN 1 ELSE 0 END) > 0
    AND SUM(CASE WHEN O.PRODUCT_NAME = 'C' THEN 1 ELSE 0 END) = 0;
```

# [1440. Evaluate Boolean Expression](https://leetcode.com/problems/evaluate-boolean-expression/)
```sql
SELECT
    LEFT_OPERAND,
    OPERATOR,
    RIGHT_OPERAND,
    CASE
        WHEN (
            (OPERATOR = '=' AND V1.VALUE = V2.VALUE)
            OR (OPERATOR = '>' AND V1.VALUE > V2.VALUE)
            OR (OPERATOR = '<' AND V1.VALUE < V2.VALUE)
        ) THEN 'true'
        ELSE 'false'
    END AS VALUE
FROM
    EXPRESSIONS AS E
    JOIN VARIABLES AS V1 ON E.LEFT_OPERAND = V1.NAME
    JOIN VARIABLES AS V2 ON E.RIGHT_OPERAND = V2.NAME;
```

# [1445. Apples & Oranges](https://leetcode.com/problems/apples-oranges/)
```sql
SELECT
    SALE_DATE,
    SUM(CASE
        WHEN FRUIT = 'apples' THEN SOLD_NUM
        ELSE -SOLD_NUM
    END) AS DIFF
FROM SALES
GROUP BY SALE_DATE
ORDER BY SALE_DATE;
```

# [1454. Active Users](https://leetcode.com/problems/active-users/)
```sql
WITH RANKCTE AS (
    SELECT
    ID, LOGIN_DATE,
    RANK() OVER (PARTITION BY ID ORDER BY LOGIN_DATE) AS RK
    FROM (SELECT DISTINCT ID, CONVERT(DATE, LOGIN_DATE) AS LOGIN_DATE FROM LOGINS) L
),
GROUPINGCTE AS (
    SELECT *,
    DATEADD(DAY, -RK, LOGIN_DATE) AS GRP_DATE
    FROM RANKCTE
),
FINALIDS AS (
    SELECT ID 
    FROM GROUPINGCTE
    GROUP BY ID, GRP_DATE
    HAVING COUNT(*)>=5
)
SELECT F.ID, A.NAME
FROM FINALIDS F
JOIN ACCOUNTS A 
ON F.ID = A.ID
ORDER BY F.ID;
```

# [1459. Rectangles Area](https://leetcode.com/problems/rectangles-area/)
```sql
SELECT
    P1.ID AS P1,
    P2.ID AS P2,
    ABS(P1.X_VALUE - P2.X_VALUE) * ABS(P1.Y_VALUE - P2.Y_VALUE) AS AREA
FROM
    POINTS AS P1
    JOIN POINTS AS P2 ON P1.ID < P2.ID
WHERE P1.X_VALUE != P2.X_VALUE AND P1.Y_VALUE != P2.Y_VALUE
ORDER BY AREA DESC, P1, P2;
```

# [1468. Calculate Salaries](https://leetcode.com/problems/calculate-salaries/)
```sql
SELECT
    S.COMPANY_ID,
    EMPLOYEE_ID,
    EMPLOYEE_NAME,
    ROUND(
        CASE
            WHEN TOP < 1000 THEN SALARY
            WHEN TOP >= 1000
            AND TOP <= 10000 THEN SALARY * 0.76
            ELSE SALARY * 0.51
        END
    ) AS SALARY
FROM
    SALARIES AS S
    JOIN (
        SELECT COMPANY_ID, MAX(SALARY) AS TOP
        FROM SALARIES
        GROUP BY COMPANY_ID
    ) AS T
        ON S.COMPANY_ID = T.COMPANY_ID;
```

# [1501. Countries You Can Safely Invest In](https://leetcode.com/problems/countries-you-can-safely-invest-in/)
```sql
SELECT
    COUNTRY.NAME AS COUNTRY
FROM
    PERSON
    INNER JOIN COUNTRY ON (SUBSTRING(PERSON.PHONE_NUMBER, 1, 3) = COUNTRY.COUNTRY_CODE)
    INNER JOIN CALLS ON (PERSON.ID IN (CALLS.CALLER_ID, CALLS.CALLEE_ID))
GROUP BY
    COUNTRY.NAME
HAVING
    AVG(CALLS.DURATION) > (
        SELECT
            AVG(DURATION)
        FROM
            CALLS
    );
```

# [1532. The Most Recent Three Orders](https://leetcode.com/problems/the-most-recent-three-orders/)
```sql
    SELECT
      ORDER_ID,
      ORDER_DATE,
      CUSTOMER_ID,
      ROW_NUMBER() OVER(
        PARTITION BY CUSTOMER_ID
        ORDER BY ORDER_DATE DESC
      ) AS ROW_NUMBER
    FROM ORDERS
  )
SELECT
  CUSTOMERS.NAME AS CUSTOMER_NAME,
  CUSTOMERS.CUSTOMER_ID,
  ORDERSWITHROWNUMBER.ORDER_ID,
  ORDERSWITHROWNUMBER.ORDER_DATE
FROM ORDERSWITHROWNUMBER
INNER JOIN CUSTOMERS
  ON ORDERSWITHROWNUMBER.CUSTOMER_ID = CUSTOMERS.CUSTOMER_ID
WHERE ORDERSWITHROWNUMBER.ROW_NUMBER <= 3
ORDER BY CUSTOMER_NAME, CUSTOMER_ID, ORDER_DATE DESC;
```

# [1549. The Most Recent Orders for Each Product](https://leetcode.com/problems/the-most-recent-orders-for-each-product/)
```sql
WITH RANKEDPRODUCTS AS (
    SELECT
      PRODUCTS.PRODUCT_NAME,
      PRODUCTS.PRODUCT_ID,
      ORDERS.ORDER_ID,
      ORDERS.ORDER_DATE,
      RANK() OVER(
        PARTITION BY PRODUCTS.PRODUCT_NAME
        ORDER BY ORDERS.ORDER_DATE DESC
      ) AS RNK
    FROM PRODUCTS
    INNER JOIN ORDERS
      ON PRODUCTS.PRODUCT_ID = ORDERS.PRODUCT_ID
)
SELECT
  RANKEDPRODUCTS.PRODUCT_NAME,
  RANKEDPRODUCTS.PRODUCT_ID,
  RANKEDPRODUCTS.ORDER_ID,
  RANKEDPRODUCTS.ORDER_DATE
FROM RANKEDPRODUCTS
WHERE RANKEDPRODUCTS.RNK = 1;
```

# [1555. Bank Account Summary](https://leetcode.com/problems/bank-account-summary/)
```sql
WITH UPDATEDUSERS AS (
    SELECT
      USERS.USER_ID,
      USERS.USER_NAME,
      USERS.CREDIT + ISNULL(SUM(
        CASE
          WHEN USERS.USER_ID = TRANSACTIONS.PAID_BY THEN -TRANSACTIONS.AMOUNT
          WHEN USERS.USER_ID = TRANSACTIONS.PAID_TO THEN TRANSACTIONS.AMOUNT
          ELSE 0
        END
      ), 0) AS CREDIT
    FROM USERS
    LEFT JOIN TRANSACTIONS
      ON (USERS.USER_ID IN (TRANSACTIONS.PAID_BY, TRANSACTIONS.PAID_TO))
    GROUP BY
      USERS.USER_ID,
      USERS.USER_NAME,
      USERS.CREDIT
)
SELECT
  *,
  CASE
    WHEN CREDIT < 0 THEN 'yes'
    ELSE 'no'
  END AS CREDIT_LIMIT_BREACHED
FROM UPDATEDUSERS;
```

# [1596. The Most Frequently Ordered Products for Each Customer](https://leetcode.com/problems/the-most-frequently-ordered-products-for-each-customer/)
```sql
WITH TMP AS (
    SELECT
        A.CUSTOMER_ID,
        B.PRODUCT_ID,
        C.PRODUCT_NAME,
        COUNT(B.ORDER_ID) OVER(PARTITION BY A.CUSTOMER_ID, B.PRODUCT_ID) AS FREQ
    FROM CUSTOMERS AS A
    JOIN ORDERS AS B
        ON A.CUSTOMER_ID = B.CUSTOMER_ID
    JOIN PRODUCTS AS C
        ON B.PRODUCT_ID = C.PRODUCT_ID
),
TMP1 AS (
    SELECT
        CUSTOMER_ID,
        PRODUCT_ID,
        PRODUCT_NAME,
        FREQ,
        DENSE_RANK() OVER(PARTITION BY CUSTOMER_ID ORDER BY FREQ DESC) AS RNK
    FROM TMP
)
SELECT DISTINCT
    CUSTOMER_ID,
    PRODUCT_ID,
    PRODUCT_NAME
FROM TMP1
WHERE
    RNK = 1;
```

# [1613. Find the Missing IDs](https://leetcode.com/problems/find-the-missing-ids/)
```sql
WITH CTE AS (
    -- ANCHOR MEMBER
    SELECT 1 AS ID, MAX(C.CUSTOMER_ID) AS MAX_ID
    FROM CUSTOMERS AS C

    UNION ALL

    -- RECURSIVE MEMBER
    SELECT ID + 1, MAX_ID
    FROM CTE
    WHERE ID < MAX_ID
)
SELECT ID AS IDS
FROM CTE AS C
WHERE C.ID NOT IN (
    SELECT CUSTOMER_ID
    FROM CUSTOMERS
)
ORDER BY 1 ASC;
```

# [1699. Number of Calls Between Two Persons](https://leetcode.com/problems/number-of-calls-between-two-persons/)
```sql
SELECT
  LEAST(FROM_ID, TO_ID) AS PERSON1,
  GREATEST(FROM_ID, TO_ID) AS PERSON2,
  COUNT(*) AS CALL_COUNT,
  SUM(DURATION) AS TOTAL_DURATION
FROM CALLS
GROUP BY 1, 2;
```

# [1709. Biggest Window Between Visits](https://leetcode.com/problems/biggest-window-between-visits/)
```sql
SELECT 
  USER_ID, 
  MAX(DIFF) AS BIGGEST_WINDOW 
FROM 
  (
    SELECT 
      USER_ID, 
      DATEDIFF(
        COALESCE(
          LEAD(VISIT_DATE) OVER (
            PARTITION BY USER_ID 
            ORDER BY 
              VISIT_DATE
          ), 
          '2021-01-01'
        ), 
        VISIT_DATE
      ) AS DIFF 
    FROM 
      USERVISITS
  ) A 
GROUP BY 
  USER_ID 
ORDER BY 
  USER_ID;
```

# [1715. Count Apples and Oranges](https://leetcode.com/problems/count-apples-and-oranges/)
```sql
SELECT SUM(ISNULL(BOX.APPLE_COUNT, 0) + ISNULL(CHEST.APPLE_COUNT, 0)) AS APPLE_COUNT,
       SUM(ISNULL(BOX.ORANGE_COUNT, 0) + ISNULL(CHEST.ORANGE_COUNT, 0)) AS ORANGE_COUNT
FROM BOXES AS BOX
LEFT JOIN CHESTS AS CHEST ON BOX.CHEST_ID = CHEST.CHEST_ID;
```

# [1747. Leetflex Banned Accounts](https://leetcode.com/problems/leetflex-banned-accounts/)
```sql
SELECT DISTINCT L1.ACCOUNT_ID
FROM LOGINFO AS L1
INNER JOIN LOGINFO AS L2
  ON L1.ACCOUNT_ID = L2.ACCOUNT_ID
  AND L1.IP_ADDRESS <> L2.IP_ADDRESS
  AND (L1.LOGIN BETWEEN L2.LOGIN AND L2.LOGOUT OR L1.LOGOUT BETWEEN L2.LOGIN AND L2.LOGOUT);
```

# [176. Second Highest Salary](https://leetcode.com/problems/second-highest-salary/)
```sql
WITH
  RANKEDEMPLOYEES AS (
    SELECT *, DENSE_RANK() OVER(ORDER BY SALARY DESC) AS RNK
    FROM EMPLOYEE
  )
SELECT MAX(SALARY) AS SECONDHIGHESTSALARY
FROM RANKEDEMPLOYEES
WHERE RNK = 2;
```

# [177. Nth Highest Salary](https://leetcode.com/problems/nth-highest-salary/)
```sql
CREATE FUNCTION getNthHighestSalary(@N INT) RETURNS INT AS BEGIN RETURN (
  SELECT 
    MAX(SALARY) AS SALARY 
  FROM 
    (
      SELECT 
        *, 
        DENSE_RANK() OVER(
          ORDER BY 
            SALARY DESC
        ) AS RNK 
      FROM 
        EMPLOYEE
    ) A 
  WHERE 
    RNK = @N
);
END
```

# [178. Rank Scores](https://leetcode.com/problems/rank-scores/)
```sql
SELECT
  SCORE,
  DENSE_RANK() OVER(ORDER BY SCORE DESC) AS RANK
FROM SCORES
```

# [1783. Grand Slam Titles](https://leetcode.com/problems/grand-slam-titles/)
```sql
SELECT 
    T.PLAYER_ID, 
    PLAYERS.PLAYER_NAME, 
    COUNT(1) AS GRAND_SLAMS_COUNT
FROM 
(
    SELECT YEAR, 'Wimbledon' AS TOURNAMENT, WIMBLEDON AS PLAYER_ID FROM CHAMPIONSHIPS
    UNION ALL
    SELECT YEAR, 'Fr_open' AS TOURNAMENT, FR_OPEN AS PLAYER_ID FROM CHAMPIONSHIPS
    UNION ALL
    SELECT YEAR, 'US_open' AS TOURNAMENT, US_OPEN AS PLAYER_ID FROM CHAMPIONSHIPS
    UNION ALL
    SELECT YEAR, 'Au_open' AS TOURNAMENT, AU_OPEN AS PLAYER_ID FROM CHAMPIONSHIPS
) T
INNER JOIN PLAYERS ON T.PLAYER_ID = PLAYERS.PLAYER_ID
GROUP BY T.PLAYER_ID, PLAYERS.PLAYER_NAME
ORDER BY GRAND_SLAMS_COUNT DESC;
-----------------------------
SELECT 
    P.PLAYER_ID, 
    P.PLAYER_NAME,
    SUM(CASE WHEN C.WIMBLEDON = P.PLAYER_ID THEN 1 ELSE 0 END) +
    SUM(CASE WHEN C.FR_OPEN = P.PLAYER_ID THEN 1 ELSE 0 END) +
    SUM(CASE WHEN C.US_OPEN = P.PLAYER_ID THEN 1 ELSE 0 END) +
    SUM(CASE WHEN C.AU_OPEN = P.PLAYER_ID THEN 1 ELSE 0 END) AS GRAND_SLAMS_COUNT
FROM 
    PLAYERS AS P
CROSS JOIN 
    CHAMPIONSHIPS AS C
GROUP BY 
    P.PLAYER_ID, 
    P.PLAYER_NAME
HAVING 
    SUM(CASE WHEN C.WIMBLEDON = P.PLAYER_ID THEN 1 ELSE 0 END) +
    SUM(CASE WHEN C.FR_OPEN = P.PLAYER_ID THEN 1 ELSE 0 END) +
    SUM(CASE WHEN C.US_OPEN = P.PLAYER_ID THEN 1 ELSE 0 END) +
    SUM(CASE WHEN C.AU_OPEN = P.PLAYER_ID THEN 1 ELSE 0 END) > 0
ORDER BY 
    GRAND_SLAMS_COUNT DESC;
```

# [180. Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/)
```sql
WITH
  LOGSNEIGHBORS AS (
    SELECT
      *,
      LAG(NUM) OVER(ORDER BY ID) AS PREV_NUM,
      LEAD(NUM) OVER(ORDER BY ID) AS NEXT_NUM
    FROM LOGS
  )
SELECT DISTINCT NUM AS CONSECUTIVENUMS
FROM LOGSNEIGHBORS
WHERE
  NUM = PREV_NUM
  AND NUM = NEXT_NUM;
```

# [1811. Find Interview Candidates](https://leetcode.com/problems/find-interview-candidates/)
```sql
WITH USERTOCONTEST AS (
  SELECT GOLD_MEDAL AS USER_ID, CONTEST_ID FROM CONTESTS 
  UNION ALL 
  SELECT SILVER_MEDAL AS USER_ID, CONTEST_ID FROM CONTESTS 
  UNION ALL 
  SELECT BRONZE_MEDAL AS USER_ID, CONTEST_ID FROM CONTESTS
), 
USERTOCONTESTWITHGROUPID AS (
  SELECT 
    USER_ID, 
    CONTEST_ID - ROW_NUMBER() OVER(PARTITION BY USER_ID ORDER BY CONTEST_ID) AS GROUP_ID 
  FROM 
    USERTOCONTEST
), 
CANDIDATEUSERIDS AS (
  SELECT USER_ID FROM USERTOCONTESTWITHGROUPID 
  GROUP BY USER_ID, GROUP_ID 
  HAVING COUNT(*) >= 3 
  UNION 
  SELECT GOLD_MEDAL AS USER_ID FROM CONTESTS 
  GROUP BY GOLD_MEDAL 
  HAVING COUNT(*) >= 3
) 
SELECT 
  USERS.NAME, 
  USERS.MAIL
  FROM CANDIDATEUSERIDSINNER 
  JOIN USERS ON CANDIDATEUSERIDS.USER_ID = USERS.USER_ID;
```

# [1831. Maximum Transaction Each Day](https://leetcode.com/problems/maximum-transaction-each-day/)
```sql
SELECT 
  TRANSACTION_ID 
FROM 
  (
    SELECT 
      TRANSACTION_ID, DATE(DAY) AS DATE1, AMOUNT, RANK() OVER(PARTITION BY DATE(DAY) ORDER BY AMOUNT DESC) AS RK 
    FROM 
      TRANSACTIONS
  ) AS TEMP 
WHERE 
  RK = 1 
ORDER BY 
  TRANSACTION_ID;
```

# [184. Department Highest Salary](https://leetcode.com/problems/department-highest-salary/)
```sql
WITH
  EMPLOYEESWITHMAXSALARYINDEPARTMENT AS (
    SELECT
      DEPARTMENT.NAME AS DEPARTMENT,
      EMPLOYEE.NAME AS EMPLOYEE,
      EMPLOYEE.SALARY,
      MAX(EMPLOYEE.SALARY) OVER(PARTITION BY EMPLOYEE.DEPARTMENTID) AS MAX_SALARY
    FROM EMPLOYEE
    LEFT JOIN DEPARTMENT
      ON (EMPLOYEE.DEPARTMENTID = DEPARTMENT.ID)
  )
SELECT
  DEPARTMENT AS DEPARTMENT,
  EMPLOYEE AS EMPLOYEE,
  SALARY AS SALARY
FROM EMPLOYEESWITHMAXSALARYINDEPARTMENT
WHERE SALARY = MAX_SALARY;
```

# [1841. League Statistics](https://leetcode.com/problems/league-statistics/)
```sql
SELECT
  T.TEAM_NAME,
  COUNT(*) AS MATCHES_PLAYED,
  SUM(CASE WHEN COMBINED.NUM_GOALS > COMBINED.NUM_CONCEDED_GOALS THEN 3 WHEN COMBINED.NUM_GOALS = COMBINED.NUM_CONCEDED_GOALS THEN 1 ELSE 0 END) AS POINTS,
  SUM(COMBINED.NUM_GOALS) AS GOAL_FOR,
  SUM(COMBINED.NUM_CONCEDED_GOALS) AS GOAL_AGAINST,
  SUM(COMBINED.NUM_GOALS) - SUM(COMBINED.NUM_CONCEDED_GOALS) AS GOAL_DIFF
FROM (
  SELECT
    HOST_TEAM AS TEAM_ID,
    HOST_GOALS AS NUM_GOALS,
    GUEST_GOALS AS NUM_CONCEDED_GOALS
  FROM MATCHES
  UNION ALL
  SELECT
    GUEST_TEAM AS TEAM_ID,
    GUEST_GOALS AS NUM_GOALS,
    HOST_GOALS AS NUM_CONCEDED_GOALS
  FROM MATCHES
) AS COMBINED
JOIN TEAMS AS T
  ON COMBINED.TEAM_ID = T.TEAM_ID
GROUP BY
  T.TEAM_NAME
ORDER BY
  POINTS DESC,
  GOAL_DIFF DESC,
  T.TEAM_NAME ASC;
```

# [1843. Suspicious Bank Accounts](https://leetcode.com/problems/suspicious-bank-accounts/)
```sql
WITH SUSPICIOUSACCOUNTTOMONTH AS (
    -- 1. IDENTIFY MONTHS WITH SUSPICIOUS INCOME
    SELECT
        T.ACCOUNT_ID,
        FORMAT(T.DAY, 'YYYYMM') AS MONTH_STR
    FROM
        TRANSACTIONS AS T
    INNER JOIN
        ACCOUNTS AS A ON T.ACCOUNT_ID = A.ACCOUNT_ID
    WHERE
        T.TYPE = 'Creditor'
    GROUP BY
        T.ACCOUNT_ID,
        FORMAT(T.DAY, 'YYYYMM')
    HAVING
        SUM(T.AMOUNT) > A.MAX_INCOME
)
-- 2. FIND ACCOUNTS WITH CONSECUTIVE SUSPICIOUS MONTHS USING A SELF-JOIN
SELECT DISTINCT
    CURRMONTH.ACCOUNT_ID
FROM
    SUSPICIOUSACCOUNTTOMONTH AS CURRMONTH
INNER JOIN
    SUSPICIOUSACCOUNTTOMONTH AS NEXTMONTH ON CURRMONTH.ACCOUNT_ID = NEXTMONTH.ACCOUNT_ID
WHERE
    DATEDIFF(MONTH, CONVERT(DATE, CURRMONTH.MONTH_STR + '01'), CONVERT(DATE, NEXTMONTH.MONTH_STR + '01')) = 1;
```

# [1867. Orders With Maximum Quantity Above Average](https://leetcode.com/problems/orders-with-maximum-quantity-above-average/)
```sql
SELECT 
  ORDER_ID 
FROM 
  ORDERSDETAILS 
GROUP BY 
  ORDER_ID 
HAVING 
  MAX(QUANTITY) > (
    SELECT 
      MAX(AVG_QUANTITY) 
    FROM 
      (
        SELECT 
          ORDER_ID, 
          SUM(QUANTITY) / COUNT(PRODUCT_ID) AS AVG_QUANTITY 
        FROM 
          ORDERSDETAILS 
        GROUP BY 
          ORDER_ID
      ) T
  );
```

# [1875. Group Employees of the Same Salary](https://leetcode.com/problems/group-employees-of-the-same-salary/)
```sql
WITH
  EMPLOYEESWITHCOUNTPERSALARY AS (
    SELECT
      *,
      COUNT(EMPLOYEE_ID) OVER(PARTITION BY SALARY) AS COUNT_PER_SALARY
    FROM EMPLOYEES
  )
SELECT
  EMPLOYEE_ID,
  NAME,
  SALARY,
  DENSE_RANK() OVER(ORDER BY SALARY) AS TEAM_ID
FROM EMPLOYEESWITHCOUNTPERSALARY
WHERE COUNT_PER_SALARY > 1
ORDER BY TEAM_ID, EMPLOYEE_ID;
```

# [1907. Count Salary Categories](https://leetcode.com/problems/count-salary-categories/)
```sql
SELECT
  'Low Salary' AS CATEGORY,
  SUM(CASE WHEN INCOME < 20000 THEN 1 ELSE 0 END) AS ACCOUNTS_COUNT
FROM ACCOUNTS
UNION ALL
SELECT
  'Average Salary' AS CATEGORY,
  SUM(CASE WHEN INCOME >= 20000 AND INCOME <= 50000 THEN 1 ELSE 0 END) AS ACCOUNTS_COUNT
FROM ACCOUNTS
UNION ALL
SELECT
  'High Salary' AS CATEGORY,
  SUM(CASE WHEN INCOME > 50000 THEN 1 ELSE 0 END) AS ACCOUNTS_COUNT
FROM ACCOUNTS;
```

# [1934. Confirmation Rate](https://leetcode.com/problems/confirmation-rate/)
```sql
SELECT
    S.USER_ID,
    ISNULL(CAST(AVG(CAST(CASE WHEN C.ACTION = 'confirmed' THEN 1 ELSE 0 END AS FLOAT)) AS NUMERIC(10, 2)), 0) AS CONFIRMATION_RATE
FROM
    SIGNUPS AS S
LEFT JOIN
    CONFIRMATIONS AS C ON S.USER_ID = C.USER_ID
GROUP BY
    S.USER_ID;
```

# [1949. Strong Friendship](https://leetcode.com/problems/strong-friendship/)
```sql
WITH BIDIRECTIONALFRIENDSHIPS AS (
    -- STEP 1: CREATE A TEMPORARY TABLE OF ALL FRIENDSHIPS IN BOTH DIRECTIONS.
    SELECT USER1_ID, USER2_ID FROM FRIENDSHIP
    UNION ALL
    SELECT USER2_ID, USER1_ID FROM FRIENDSHIP
),
COMMONFRIENDS AS (
    -- STEP 2: FIND PAIRS WITH AT LEAST 3 COMMON FRIENDS.
    SELECT
        T1.USER1_ID AS USER1,
        T2.USER1_ID AS USER2,
        COUNT(T1.USER2_ID) AS COMMON_FRIEND_COUNT
    FROM BIDIRECTIONALFRIENDSHIPS AS T1
    JOIN BIDIRECTIONALFRIENDSHIPS AS T2
        -- THE JOIN CONDITION MATCHES USERS WITH A COMMON FRIEND.
        ON T1.USER2_ID = T2.USER2_ID
    -- THIS CONDITION ENSURES EACH UNIQUE PAIR IS COUNTED ONLY ONCE.
    WHERE T1.USER1_ID < T2.USER1_ID
    GROUP BY T1.USER1_ID, T2.USER1_ID
    -- THE HAVING CLAUSE FILTERS FOR AT LEAST 3 COMMON FRIENDS.
    HAVING COUNT(T1.USER2_ID) >= 3
)
-- STEP 3: SELECT ONLY THE PAIRS THAT ARE ALREADY FRIENDS.
SELECT
    CF.USER1,
    CF.USER2
FROM COMMONFRIENDS CF
JOIN FRIENDSHIP F
    -- A JOIN IS USED TO CHECK FOR EXISTING FRIENDSHIPS IN A STANDARD WAY.
    ON (CF.USER1 = F.USER1_ID AND CF.USER2 = F.USER2_ID)
    OR (CF.USER1 = F.USER2_ID AND CF.USER2 = F.USER1_ID);
```

# [1951. All the Pairs With the Maximum Number of Common Followers](https://leetcode.com/problems/all-the-pairs-with-the-maximum-number-of-common-followers/)
```sql
WITH R AS (
    SELECT R1.USER_ID AS USER1_ID, R2.USER_ID AS USER2_ID, COUNT(*) AS CNT
    FROM RELATIONS R1
    JOIN RELATIONS R2 ON R1.FOLLOWER_ID = R2.FOLLOWER_ID
    WHERE R1.USER_ID < R2.USER_ID
    GROUP BY R1.USER_ID, R2.USER_ID
)
SELECT USER1_ID, USER2_ID
FROM R
WHERE CNT = (SELECT MAX(CNT) FROM R);
```

# [1988. Find Cutoff Score for Each School](https://leetcode.com/problems/find-cutoff-score-for-each-school/)
```sql
SELECT SCHOOL_ID, IFNULL(MIN(SCORE), -1) AS SCORE
    FROM SCHOOLS LEFT JOIN EXAM
    ON CAPACITY >= STUDENT_COUNT
    GROUP BY SCHOOL_ID;
```

# [1990. Count the Number of Experiments](https://leetcode.com/problems/count-the-number-of-experiments/)
```sql
WITH P AS (
    SELECT 'Android' AS PLATFORM
    UNION
    SELECT 'IOS'
    UNION
    SELECT 'Web'
),
EXP AS (
    SELECT 'Reading' AS EXPERIMENT_NAME
    UNION
    SELECT 'Sports'
    UNION
    SELECT 'Programming'
),
T AS (
    SELECT *
    FROM
        P
        CROSS JOIN EXP
)
SELECT
    T.PLATFORM,
    T.EXPERIMENT_NAME,
    COUNT(E.EXPERIMENT_ID) AS NUM_EXPERIMENTS
FROM
    T AS T
    LEFT JOIN EXPERIMENTS AS E
        ON T.PLATFORM = E.PLATFORM
        AND T.EXPERIMENT_NAME = E.EXPERIMENT_NAME
GROUP BY
    T.PLATFORM,
    T.EXPERIMENT_NAME
ORDER BY
    T.PLATFORM, T.EXPERIMENT_NAME;
```

# [2020. Number of Accounts That Did Not Stream](https://leetcode.com/problems/number-of-accounts-that-did-not-stream/)
```sql
SELECT COUNT(DISTINCT SUB.ACCOUNT_ID) AS ACCOUNTS_COUNT
FROM
    SUBSCRIPTIONS AS SUB
    LEFT JOIN STREAMS AS SS ON SUB.ACCOUNT_ID = SS.ACCOUNT_ID
WHERE
    YEAR(START_DATE) <= 2021
    AND YEAR(END_DATE) >= 2021
    AND (YEAR(STREAM_DATE) != 2021 OR STREAM_DATE > END_DATE);
```

# [2041. Accepted Candidates From the Interviews](https://leetcode.com/problems/accepted-candidates-from-the-interviews/)
```sql
SELECT
    CANDIDATES.CANDIDATE_ID
FROM
    CANDIDATES
INNER JOIN
    ROUNDS ON CANDIDATES.INTERVIEW_ID = ROUNDS.INTERVIEW_ID
WHERE
    CANDIDATES.YEARS_OF_EXP >= 2
GROUP BY
    CANDIDATES.CANDIDATE_ID
HAVING
    SUM(ROUNDS.SCORE) > 15;
```

# [2051. The Category of Each Member in the Store](https://leetcode.com/problems/the-category-of-each-member-in-the-store/)
```sql
SELECT
    M.MEMBER_ID,
    NAME,
    CASE
        WHEN COUNT(V.VISIT_ID) = 0 THEN 'BRONZE'
        WHEN 100 * COUNT(CHARGED_AMOUNT) / COUNT(
            V.VISIT_ID
        ) >= 80 THEN 'DIAMOND'
        WHEN 100 * COUNT(CHARGED_AMOUNT) / COUNT(V.VISIT_ID) >= 50 THEN 'GOLD'
        ELSE 'SILVER'
    END AS CATEGORY
FROM
    MEMBERS AS M
    LEFT JOIN VISITS AS V ON M.MEMBER_ID = V.MEMBER_ID
    LEFT JOIN PURCHASES AS P ON V.VISIT_ID = P.VISIT_ID
GROUP BY MEMBER_ID;
```

# [2066. Account Balance](https://leetcode.com/problems/account-balance/)
```sql
SELECT
    ACCOUNT_ID,
    DAY,
    SUM(CASE
        WHEN TYPE = 'Deposit' THEN AMOUNT
        ELSE -AMOUNT
    END) OVER (
        PARTITION BY ACCOUNT_ID
        ORDER BY DAY
    ) AS BALANCE
FROM
    TRANSACTIONS
ORDER BY
    ACCOUNT_ID,
    DAY;
```

# [2084. Drop Type 1 Orders for Customers With Type 0 Orders](https://leetcode.com/problems/drop-type-1-orders-for-customers-with-type-0-orders/)
```sql
SELECT
    ORDER_ID,
    CUSTOMER_ID,
    ORDER_TYPE
FROM
    ORDERS
WHERE
    ORDER_TYPE = 0
    OR CUSTOMER_ID NOT IN (
        SELECT
            CUSTOMER_ID
        FROM
            ORDERS
        WHERE
            ORDER_TYPE = 0
    );
-------------
WITH
  RANKEDORDERS AS (
    SELECT
      *,
      RANK() OVER(PARTITION BY CUSTOMER_ID ORDER BY ORDER_TYPE) AS RNK
    FROM ORDERS
  )
SELECT
  ORDER_ID,
  CUSTOMER_ID,
  ORDER_TYPE
FROM RANKEDORDERS
WHERE RNK = 1
```

# [2112. The Airport With the Most Traffic](https://leetcode.com/problems/the-airport-with-the-most-traffic/)
```sql
WITH
    AIRPORTTOCOUNT AS (
        SELECT
            DEPARTURE_AIRPORT AS AIRPORT_ID,
            FLIGHTS_COUNT
        FROM
            FLIGHTS
        UNION ALL
        SELECT
            ARRIVAL_AIRPORT AS AIRPORT_ID,
            FLIGHTS_COUNT
        FROM
            FLIGHTS
    ),
    RANKEDAIRPORTS AS (
        SELECT
            AIRPORT_ID,
            RANK() OVER (ORDER BY SUM(FLIGHTS_COUNT) DESC) AS RANK
        FROM
            AIRPORTTOCOUNT
        GROUP BY
            AIRPORT_ID
    )
SELECT
    AIRPORT_ID
FROM
    RANKEDAIRPORTS
WHERE
    RANK = 1;
```

# [2142. The Number of Passengers in Each Bus I](https://leetcode.com/problems/the-number-of-passengers-in-each-bus-i/)
```sql
SELECT
    B.BUS_ID,
    -- CALCULATE PASSENGERS ON THE CURRENT BUS
    -- BY SUBTRACTING THE CUMULATIVE COUNT OF THE PREVIOUS BUS
    -- FROM THE CUMULATIVE COUNT OF THE CURRENT BUS.
    -- THE ISNULL HANDLES THE FIRST BUS, SETTING THE LAG RESULT TO 0.
    COUNT(P.PASSENGER_ID) - ISNULL(LAG(COUNT(P.PASSENGER_ID), 1, 0) OVER (
        ORDER BY
            B.ARRIVAL_TIME
    ), 0) AS PASSENGERS_CNT
FROM
    BUSES AS B
    -- JOIN EACH BUS WITH ALL PASSENGERS WHO HAVE ARRIVED UP TO THAT BUS'S ARRIVAL TIME.
    LEFT JOIN PASSENGERS AS P ON P.ARRIVAL_TIME <= B.ARRIVAL_TIME
GROUP BY
    B.BUS_ID,
    B.ARRIVAL_TIME
ORDER BY
    B.BUS_ID;
```

# [2159. Order Two Columns Independently](https://leetcode.com/problems/order-two-columns-independently/)
```sql
WITH
    S AS (
        SELECT
            FIRST_COL,
            ROW_NUMBER() OVER (ORDER BY FIRST_COL) AS RK
        FROM
            DATA
    ),
    T AS (
        SELECT
            SECOND_COL,
            ROW_NUMBER() OVER (ORDER BY SECOND_COL DESC) AS RK
        FROM
            DATA
    )
SELECT
    S.FIRST_COL,
    T.SECOND_COL
FROM
    S
JOIN
    T ON S.RK = T.RK;
```

# [2175. The Change in Global Rankings](https://leetcode.com/problems/the-change-in-global-rankings/)
```sql
SELECT
    TEAMPOINTS.TEAM_ID,
    TEAMPOINTS.NAME,
    CAST(
        RANK() OVER (
            ORDER BY TEAMPOINTS.POINTS DESC,
            TEAMPOINTS.NAME
        ) AS INT
    ) - CAST(
        RANK() OVER (
            ORDER BY TEAMPOINTS.POINTS + POINTSCHANGE.POINTS_CHANGE DESC,
            TEAMPOINTS.NAME
        ) AS INT
    ) AS RANK_DIFF
FROM
    TEAMPOINTS
INNER JOIN
    POINTSCHANGE ON TEAMPOINTS.TEAM_ID = POINTSCHANGE.TEAM_ID;
```

# [2228. Users With Two Purchases Within Seven Days](https://leetcode.com/problems/users-with-two-purchases-within-seven-days/)
```sql
WITH
    T AS (
        SELECT
            USER_ID,
            DATEDIFF(
                DAY,
                LAG(PURCHASE_DATE, 1) OVER (
                    PARTITION BY USER_ID
                    ORDER BY PURCHASE_DATE
                ),
                PURCHASE_DATE
            ) AS D
        FROM
            PURCHASES
    )
SELECT DISTINCT
    USER_ID
FROM
    T
WHERE
    D <= 7
ORDER BY
    USER_ID;
```

# [2238. Number of Times a Driver Was a Passenger](https://leetcode.com/problems/number-of-times-a-driver-was-a-passenger/)
```sql
WITH T AS (SELECT DISTINCT DRIVER_ID FROM RIDES)
SELECT T.DRIVER_ID, COUNT(PASSENGER_ID) AS CNT
FROM
    T AS T
    LEFT JOIN RIDES AS R ON T.DRIVER_ID = R.PASSENGER_ID
GROUP BY 1;
```

# [2292. Products With Three or More Orders in Two Consecutive Years](https://leetcode.com/problems/products-with-three-or-more-orders-in-two-consecutive-years/)
```sql
WITH P AS (
    SELECT 
        PRODUCT_ID, 
        YEAR(PURCHASE_DATE) AS Y, 
        CASE 
            WHEN COUNT(*) >= 3 THEN 1 
            ELSE 0 
        END AS MARK
    FROM ORDERS
    GROUP BY PRODUCT_ID, YEAR(PURCHASE_DATE)
)
SELECT DISTINCT P1.PRODUCT_ID
FROM P AS P1
JOIN P AS P2 
    ON P1.PRODUCT_ID = P2.PRODUCT_ID 
    AND P1.Y = P2.Y - 1
WHERE P1.MARK = 1 AND P2.MARK = 1
ORDER BY P1.PRODUCT_ID;
-----------------
WITH PRODUCTYEARSTATS AS (
    SELECT 
        PRODUCT_ID,
        YEAR(PURCHASE_DATE) AS Y,
        COUNT(*) AS PURCHASE_COUNT
    FROM ORDERS
    GROUP BY PRODUCT_ID, YEAR(PURCHASE_DATE)
),
WITHLAG AS (
    SELECT 
        PRODUCT_ID,
        Y,
        PURCHASE_COUNT,
        LAG(PURCHASE_COUNT) OVER (
            PARTITION BY PRODUCT_ID 
            ORDER BY Y
        ) AS PREV_YEAR_COUNT
    FROM PRODUCTYEARSTATS
)
SELECT DISTINCT PRODUCT_ID
FROM WITHLAG
WHERE PURCHASE_COUNT >= 3 AND PREV_YEAR_COUNT >= 3
ORDER BY PRODUCT_ID;
```

# [2298. Tasks Count in the Weekend](https://leetcode.com/problems/tasks-count-in-the-weekend/)
```sql
SELECT
    SUM(CASE WHEN DATEPART(WEEKDAY, SUBMIT_DATE) IN (1, 7) THEN 1 ELSE 0 END) AS WEEKEND_CNT,
    SUM(CASE WHEN DATEPART(WEEKDAY, SUBMIT_DATE) NOT IN (1, 7) THEN 1 ELSE 0 END) AS WORKING_CNT
FROM TASKS;
```

# [2308. Arrange Table by Gender](https://leetcode.com/problems/arrange-table-by-gender/)
```sql
WITH T AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY GENDER
            ORDER BY USER_ID
        ) AS RK1,
        CASE
            WHEN GENDER = 'female' THEN 0
            WHEN GENDER = 'other' THEN 1
            ELSE 2
        END AS RK2
    FROM GENDERS
)
SELECT USER_ID, GENDER
FROM T
ORDER BY RK1, RK2;
```

# [2314. The First Day of the Maximum Recorded Degree in Each City](https://leetcode.com/problems/the-first-day-of-the-maximum-recorded-degree-in-each-city/)
```sql
WITH T AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY CITY_ID
            ORDER BY DEGREE DESC, DAY
        ) AS RK
    FROM WEATHER
)
SELECT CITY_ID, DAY, DEGREE
FROM T
WHERE RK = 1
ORDER BY CITY_ID;
```

# [2324. Product Sales Analysis IV](https://leetcode.com/problems/product-sales-analysis-iv/)
```sql
WITH SALESTOTAL AS (
    SELECT 
        S.USER_ID,
        S.PRODUCT_ID,
        SUM(S.QUANTITY * P.PRICE) AS TOTAL_SPENT
    FROM SALES S
    JOIN PRODUCT P ON S.PRODUCT_ID = P.PRODUCT_ID
    GROUP BY S.USER_ID, S.PRODUCT_ID
),
RANKED AS (
    SELECT 
        USER_ID,
        PRODUCT_ID,
        RANK() OVER (
            PARTITION BY USER_ID
            ORDER BY TOTAL_SPENT DESC
        ) AS RK
    FROM SALESTOTAL
)
SELECT USER_ID, PRODUCT_ID
FROM RANKED
WHERE RK = 1;
```

# [2346. Compute the Rank as a Percentage](https://leetcode.com/problems/compute-the-rank-as-a-percentage/)
```sql
SELECT
    STUDENT_ID,
    DEPARTMENT_ID,
    ISNULL(
        ROUND(
            CAST((RANK() OVER (
                PARTITION BY DEPARTMENT_ID
                ORDER BY MARK DESC
            ) - 1) * 100.0 / 
            NULLIF(COUNT(*) OVER (PARTITION BY DEPARTMENT_ID) - 1, 0)
            AS FLOAT),
            2
        ),
        0
    ) AS PERCENTAGE
FROM STUDENTS;
```

# [2372. Calculate the Influence of Each Salesperson](https://leetcode.com/problems/calculate-the-influence-of-each-salesperson/)
```sql
SELECT
    SP.SALESPERSON_ID,
    NAME,
    COALESCE(SUM(PRICE), 0) AS TOTAL
FROM
    SALESPERSON AS SP
    LEFT JOIN CUSTOMER AS C ON SP.SALESPERSON_ID = C.SALESPERSON_ID
    LEFT JOIN SALES AS S ON S.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY
    SP.SALESPERSON_ID, NAME;
```

# [2388. Change Null Values in a Table to the Previous Value](https://leetcode.com/problems/change-null-values-in-a-table-to-the-previous-value/)
```sql
WITH RN_CTE AS (
    SELECT ID, DRINK, ROW_NUMBER() OVER () AS RN
    FROM COFFEESHOP
),
GROUP_CTE AS (
    SELECT ID, DRINK, RN, SUM(NOT ISNULL(DRINK)) OVER (ORDER BY RN) AS GROUP_ID
    FROM RN_CTE
)
SELECT ID, MAX(DRINK) OVER (PARTITION BY GROUP_ID) AS DRINK
FROM GROUP_CTE
ORDER BY RN;
```

# [2394. Employees With Deductions](https://leetcode.com/problems/employees-with-deductions/)
```sql
WITH T AS (
    SELECT
        EMPLOYEE_ID,
        SUM(
            CEILING(
                DATEDIFF(SECOND, IN_TIME, OUT_TIME) / 60.0
            )
        ) / 60.0 AS TOT
    FROM
        LOGS
    GROUP BY
        EMPLOYEE_ID
)
SELECT
    E.EMPLOYEE_ID
FROM
    EMPLOYEES AS E
LEFT JOIN
    T ON E.EMPLOYEE_ID = T.EMPLOYEE_ID
WHERE
    ISNULL(T.TOT, 0) < E.NEEDED_HOURS;
```

# [2686. Immediate Food Delivery III](https://leetcode.com/problems/immediate-food-delivery-iii/)
```sql
SELECT
    ORDER_DATE,
    ROUND(100.0 * SUM(
        CASE
            WHEN CUSTOMER_PREF_DELIVERY_DATE = ORDER_DATE THEN 1
            ELSE 0
        END
    ) / COUNT(*), 2) AS IMMEDIATE_PERCENTAGE
FROM
    DELIVERY
GROUP BY
    ORDER_DATE
ORDER BY
    ORDER_DATE;
```

# [2688. Find Active Users](https://leetcode.com/problems/find-active-users/)
```sql
SELECT DISTINCT USER_ID
FROM USERS
WHERE USER_ID IN (
    SELECT USER_ID
    FROM (
        SELECT
            USER_ID,
            CREATED_AT,
            LAG(CREATED_AT, 1) OVER (
                PARTITION BY USER_ID
                ORDER BY CREATED_AT
            ) AS PREV_CREATED_AT
        FROM USERS
    ) AS T
    WHERE DATEDIFF(DAY, PREV_CREATED_AT, CREATED_AT) <= 7
);
```

# [2738. Count Occurrences in Text](https://leetcode.com/problems/count-occurrences-in-text/)
```sql
SELECT 'bull' AS WORD, COUNT(*) AS COUNT
FROM FILES
WHERE CONTENT LIKE '% bull %'
UNION
SELECT 'bear' AS WORD, COUNT(*) AS COUNT
FROM FILES
WHERE CONTENT LIKE '% bear %';
```

# [2783. Flight Occupancy and Waitlist Analysis](https://leetcode.com/problems/flight-occupancy-and-waitlist-analysis/)
```sql
SELECT
    F.FLIGHT_ID,
    CASE 
        WHEN COUNT(P.PASSENGER_ID) < F.CAPACITY THEN COUNT(P.PASSENGER_ID)
        ELSE F.CAPACITY
    END AS BOOKED_CNT,
    CASE 
        WHEN COUNT(P.PASSENGER_ID) > F.CAPACITY THEN COUNT(P.PASSENGER_ID) - F.CAPACITY
        ELSE 0
    END AS WAITLIST_CNT
FROM FLIGHTS F
LEFT JOIN PASSENGERS P ON F.FLIGHT_ID = P.FLIGHT_ID
GROUP BY F.FLIGHT_ID, F.CAPACITY
ORDER BY F.FLIGHT_ID;
```

# [2820. Election Results](https://leetcode.com/problems/election-results/)
```sql
WITH T AS (
    SELECT 
        CANDIDATE, 
        SUM(VOTE) AS TOT
    FROM (
        SELECT 
            CANDIDATE,
            1.0 / COUNT(*) OVER (PARTITION BY VOTER) AS VOTE
        FROM VOTES
        WHERE CANDIDATE IS NOT NULL
    ) AS Sub
    GROUP BY CANDIDATE
),
P AS (
    SELECT 
        CANDIDATE,
        RANK() OVER (ORDER BY TOT DESC) AS RK
    FROM T
)
SELECT CANDIDATE
FROM P
WHERE RK = 1
ORDER BY CANDIDATE;
```

# [2854. Rolling Average Steps](https://leetcode.com/problems/rolling-average-steps/)
```sql
WITH T AS (
    SELECT
        USER_ID,
        STEPS_DATE,
        ROUND(
            AVG(STEPS_COUNT) OVER (
                PARTITION BY USER_ID
                ORDER BY STEPS_DATE
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ),
            2
        ) AS ROLLING_AVERAGE,
        DATEDIFF(
            DAY,
            LAG(STEPS_DATE, 2) OVER (
                PARTITION BY USER_ID
                ORDER BY STEPS_DATE
            ),
            STEPS_DATE
        ) AS DATE_DIFF
    FROM STEPS
)
SELECT
    USER_ID,
    STEPS_DATE,
    ROLLING_AVERAGE
FROM T
WHERE DATE_DIFF = 2
ORDER BY USER_ID, STEPS_DATE;
```

# [2893. Calculate Orders Within Each Interval](https://leetcode.com/problems/calculate-orders-within-each-interval/)
```sql
SELECT
    CEILING(CAST([MINUTE] AS FLOAT) / 6) AS INTERVAL_NO,
    SUM(ORDER_COUNT) AS TOTAL_ORDERS
FROM
    ORDERS
GROUP BY
    CEILING(CAST([MINUTE] AS FLOAT) / 6)
ORDER BY
    INTERVAL_NO;
```

# [2922. Market Analysis III](https://leetcode.com/problems/market-analysis-iii/)
```sql
WITH T AS (
    SELECT
        U.SELLER_ID,
        COUNT(DISTINCT O.ITEM_ID) AS NUM_ITEMS
    FROM ORDERS AS O
    JOIN USERS AS U
        ON O.SELLER_ID = U.SELLER_ID
    JOIN ITEMS AS I
        ON O.ITEM_ID = I.ITEM_ID
    WHERE
        I.ITEM_BRAND <> U.FAVORITE_BRAND
    GROUP BY
        U.SELLER_ID
)
SELECT
    SELLER_ID,
    NUM_ITEMS
FROM T
WHERE
    NUM_ITEMS = (SELECT MAX(NUM_ITEMS) FROM T)
ORDER BY
    SELLER_ID;
```

# [2978. Symmetric Coordinates](https://leetcode.com/problems/symmetric-coordinates/)
```sql
WITH SYMMETRICCOORDINATES AS (
    SELECT DISTINCT C1.X, C1.Y
    FROM COORDINATES AS C1
    INNER JOIN COORDINATES AS C2
        ON C1.X = C2.Y AND C1.Y = C2.X
    WHERE C1.X < C1.Y
    UNION ALL
    SELECT X, Y
    FROM COORDINATES
    WHERE X = Y
    GROUP BY X, Y
    HAVING COUNT(*) > 1
)
SELECT X, Y
FROM SYMMETRICCOORDINATES
ORDER BY 1, 2;
```

# [2984. Find Peak Calling Hours for Each City](https://leetcode.com/problems/find-peak-calling-hours-for-each-city/)
```sql
WITH T AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY CITYORDER BY CNT DESC) AS RK
    FROM
        (
         SELECT
			CITY,
            DATEPART(HOUR, CALL_TIME) AS H,
            COUNT(1) AS CNT
            FROM CALLS
            GROUP BY CITY, DATEPART(HOUR, CALL_TIME)
        ) AS T
)
SELECT
    CITY,
    H AS PEAK_CALLING_HOUR,
    CNT AS NUMBER_OF_CALLS
FROM T
WHERE RK = 1
ORDER BY PEAK_CALLING_HOUR DESC, CITY DESC;
```

# [2986. Find Third Transaction](https://leetcode.com/problems/find-third-transaction/)
```sql
WITH TRANSACTIONNEIGHBORS AS (
  SELECT
    USER_ID,
    SPEND,
    TRANSACTION_DATE,
    RANK() OVER( PARTITION BY USER_IDORDER BYTRANSACTION_DATE ) AS DATE_RANK,
    FIRST_VALUE(SPEND) OVER( PARTITION BY USER_ID ORDER BY TRANSACTION_DATE ) AS FIRST_SPEND,
    LAG(SPEND) OVER( PARTITION BY USER_ID ORDER BY TRANSACTION_DATE ) AS SECOND_SPEND
  FROM
    TRANSACTIONS
)
SELECT
  USER_ID,
  SPEND AS THIRD_TRANSACTION_SPEND,
  TRANSACTION_DATE AS THIRD_TRANSACTION_DATE
FROM
  TRANSACTIONNEIGHBORS
WHERE
  DATE_RANK = 3 AND SPEND > FIRST_SPEND AND SPEND > SECOND_SPEND
ORDER BY 1;
```

# [2988. Manager of the Largest Department](https://leetcode.com/problems/manager-of-the-largest-department/)
```sql
WITH RANKEDDEPARTMENTS AS (
    -- THIS CTE RANKS DEPARTMENTS BASED ON THE NUMBER OF EMPLOYEES THEY HAVE.
    SELECT
        DEP_ID,
        DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS RNK
    FROM
        EMPLOYEES
    GROUP BY
        DEP_ID
)
SELECT
    -- SELECTS THE EMPLOYEE'S NAME (ALIASED AS MANAGER_NAME) AND THEIR DEPARTMENT ID.
    E.EMP_NAME AS MANAGER_NAME,
    E.DEP_ID
FROM
    EMPLOYEES AS E
-- JOINS THE EMPLOYEES TABLE WITH THE RANKEDDEPARTMENTS CTE ON THE DEPARTMENT ID.
INNER JOIN
    RANKEDDEPARTMENTS AS RD
    ON E.DEP_ID = RD.DEP_ID
WHERE
    -- FILTERS FOR EMPLOYEES WHO ARE MANAGERS AND BELONG TO A DEPARTMENT WITH A RANK OF 1 (THE LARGEST DEPARTMENT).
    E.POSITION = 'Manager'
    AND RD.RNK = 1
-- ORDERS THE RESULTS BY DEPARTMENT ID.
ORDER BY
    E.DEP_ID;
```

# [2989. Class Performance](https://leetcode.com/problems/class-performance/)
```sql
SELECT 
  MAX(
    ASSIGNMENT1 + ASSIGNMENT2 + ASSIGNMENT3
  ) - MIN(
    ASSIGNMENT1 + ASSIGNMENT2 + ASSIGNMENT3
  ) AS DIFFERENCE_IN_SCORE 
FROM 
  SCORES;
```

# [2993. Friday Purchases I](https://leetcode.com/problems/friday-purchases-i/)
```sql
SELECT
  -- CALCULATES THE WEEK NUMBER FOR THE PURCHASE DATE RELATIVE TO NOVEMBER 1, 2023.
  DATEDIFF(WEEK, '2023-11-01', PURCHASE_DATE) + 1 AS WEEK_OF_MONTH,
  PURCHASE_DATE,
  -- SUMS THE TOTAL SPENDING FOR EACH SPECIFIC PURCHASE DATE.
  SUM(AMOUNT_SPEND) AS TOTAL_AMOUNT
FROM
  PURCHASES
WHERE
  -- FILTERS FOR RECORDS IN NOVEMBER 2023.
  MONTH(PURCHASE_DATE) = 11
  AND YEAR(PURCHASE_DATE) = 2023
  -- FILTERS FOR FRIDAYS.
  AND DATENAME(WEEKDAY, PURCHASE_DATE) = 'Friday'
GROUP BY
  -- GROUPS BY DATE TO AGGREGATE SPENDING FOR EACH FRIDAY.
  PURCHASE_DATE
ORDER BY
  -- ORDERS THE RESULTS CHRONOLOGICALLY BY THE CALCULATED WEEK NUMBER.
  WEEK_OF_MONTH;
```

# [3050. Pizza Toppings Cost Analysis](https://leetcode.com/problems/pizza-toppings-cost-analysis/)
```sql
WITH T AS (
    -- Ranks each topping alphabetically. The rank is used to ensure unique combinations.
    SELECT
        *,
        RANK() OVER (ORDER BY TOPPING_NAME) AS RK
    FROM
        TOPPINGS
)
SELECT
    -- Concatenates the names of the three toppings to form a pizza name.
    CONCAT(T1.TOPPING_NAME, ',', T2.TOPPING_NAME, ',', T3.TOPPING_NAME) AS PIZZA,
    -- Sums the costs of the three toppings.
    T1.COST + T2.COST + T3.COST AS TOTAL_COST
FROM
    T AS T1
    JOIN T AS T2
        ON T1.RK < T2.RK -- Ensures T2's topping comes after T1's to avoid duplicates
    JOIN T AS T3
        ON T2.RK < T3.RK -- Ensures T3's topping comes after T2's
ORDER BY
    -- Orders by total cost descending (most expensive first) and then by pizza name ascending for ties.
    TOTAL_COST DESC,
    PIZZA ASC;
```

# [3054. Binary Tree Nodes](https://leetcode.com/problems/binary-tree-nodes/)
```sql
SELECT DISTINCT
    T1.N AS N,
    CASE
        -- A node is a 'ROOT' if it has no parent (its parent column 'P' is NULL).
        WHEN T1.P IS NULL THEN 'Root'
        -- A node is a 'LEAF' if it has a parent but no children (no matching 'N' in the T2 parent column).
        WHEN T2.P IS NULL THEN 'Leaf'
        -- A node is an 'INNER' node if it has both a parent and at least one child.
        ELSE 'Inner'
    END AS TYPE
FROM
    TREE AS T1
    -- Performs a LEFT JOIN to check if each node (T1.N) exists as a parent (T2.P) to another node.
    -- This allows us to identify nodes that have children.
    LEFT JOIN TREE AS T2 ON T1.N = T2.P
ORDER BY
    N;
```

# [3055. Top Percentile Fraud](https://leetcode.com/problems/top-percentile-fraud/)
```sql
WITH
  FRAUDPERCENTILE AS (
    SELECT
      POLICY_ID,
      STATE,
      FRAUD_SCORE,
      PERCENT_RANK() OVER(
        PARTITION BY STATE
        ORDER BY FRAUD_SCORE DESC
      ) AS PCT_RNK
    FROM FRAUD
  )
SELECT POLICY_ID, STATE, FRAUD_SCORE
FROM FRAUDPERCENTILE
WHERE PCT_RNK < 0.05
ORDER BY STATE, FRAUD_SCORE DESC, POLICY_ID;
```

# [3056. Snaps Analysis](https://leetcode.com/problems/snaps-analysis/)
```sql
SELECT
    AGE_BUCKET,
    ROUND(100.0 * SUM(CASE WHEN ACTIVITY_TYPE = 'send' THEN TIME_SPENT ELSE 0 END) / SUM(TIME_SPENT), 2) AS SEND_PERC,
    ROUND(100.0 * SUM(CASE WHEN ACTIVITY_TYPE = 'open' THEN TIME_SPENT ELSE 0 END) / SUM(TIME_SPENT), 2) AS OPEN_PERC
FROM
    ACTIVITIES
JOIN
    AGE ON ACTIVITIES.USER_ID = AGE.USER_ID
GROUP BY
    AGE_BUCKET;
```

# [3058. Friends With No Mutual Friends](https://leetcode.com/problems/friends-with-no-mutual-friends/)
```sql
WITH TWOWAYFRIENDS AS (
    -- Creates a list of all friendships in both directions (e.g., A -> B and B -> A)
    SELECT
        USER_ID1 AS USER_ID,
        USER_ID2 AS FRIEND_ID
    FROM
        FRIENDS
    UNION ALL
    SELECT
        USER_ID2,
        USER_ID1
    FROM
        FRIENDS
),
USERTOMUTUALFRIEND AS (
    -- Finds all pairs of users who have at least one mutual friend by self-joining the TWOWAYFRIENDS CTE
    SELECT
        USER1.USER_ID,
        USER2.USER_ID AS FRIEND_ID
    FROM
        TWOWAYFRIENDS AS USER1
    JOIN
        TWOWAYFRIENDS AS USER2
        ON USER1.FRIEND_ID = USER2.FRIEND_ID
    WHERE
        USER1.USER_ID != USER2.USER_ID
)
SELECT
    -- Selects the original friendship pairs
    FRIENDS.*
FROM
    FRIENDS
    -- Performs a LEFT JOIN to find friendships that do not exist in the mutual friends list
    LEFT JOIN USERTOMUTUALFRIEND
        ON (
            FRIENDS.USER_ID1 = USERTOMUTUALFRIEND.USER_ID
            AND FRIENDS.USER_ID2 = USERTOMUTUALFRIEND.FRIEND_ID
        )
-- Filters for rows where there was no match, meaning the friends have no mutual friends
WHERE
    USERTOMUTUALFRIEND.FRIEND_ID IS NULL
ORDER BY 1, 2;
```

# [3087. Find Trending Hashtags](https://leetcode.com/problems/find-trending-hashtags/)
```sql
SELECT 
  TOP 3 CONCAT(
    '#', 
    SUBSTRING(
      SUBSTRING(
        TWEET, 
        CHARINDEX('#', TWEET) + 1, 
        LEN(TWEET)
      ), 
      1, 
      CHARINDEX(
        ' ', 
        SUBSTRING(
          TWEET, 
          CHARINDEX('#', TWEET) + 1, 
          LEN(TWEET) + 1
        )
      ) -1
    )
  ) AS HASHTAG, 
  COUNT(*) AS HASHTAG_COUNT 
FROM 
  TWEETS 
WHERE 
  FORMAT(TWEET_DATE, 'yyyyMM') = '202402' 
GROUP BY 
  CONCAT(
    '#', 
    SUBSTRING(
      SUBSTRING(
        TWEET, 
        CHARINDEX('#', TWEET) + 1, 
        LEN(TWEET)
      ), 
      1, 
      CHARINDEX(
        ' ', 
        SUBSTRING(
          TWEET, 
          CHARINDEX('#', TWEET) + 1, 
          LEN(TWEET) + 1
        )
      ) -1
    )
  ) 
ORDER BY 
  HASHTAG_COUNT DESC, 
  HASHTAG DESC;
```

# [3089. Find Bursty Behavior](https://leetcode.com/problems/find-bursty-behavior/)
```sql
WITH SEVENDAYPOSTCOUNTS AS (
  SELECT 
    POST1.USER_ID, 
    COUNT(*) AS POST_COUNT 
  FROM 
    POSTS AS POST1 
    INNER JOIN POSTS AS POST2 ON POST1.USER_ID = POST2.USER_ID 
  WHERE 
    POST2.POST_DATE BETWEEN POST1.POST_DATE 
    AND DATEADD(DAY, 6, POST1.POST_DATE) 
  GROUP BY 
    POST1.USER_ID, 
    POST1.POST_ID
), 
AVERAGEWEEKLYPOSTS AS (
  SELECT 
    USER_ID, 
    COUNT(*) / 4 AS AVG_WEEKLY_POSTS 
  FROM 
    POSTS 
  WHERE 
    POST_DATE BETWEEN '2024-02-01' 
    AND '2024-02-28' 
  GROUP BY 
    USER_ID
) 
SELECT 
  SEVENDAYPOSTCOUNTS.USER_ID, 
  MAX(SEVENDAYPOSTCOUNTS.POST_COUNT) AS MAX_7DAY_POSTS, 
  AVERAGEWEEKLYPOSTS.AVG_WEEKLY_POSTS 
FROM 
  SEVENDAYPOSTCOUNTS 
  INNER JOIN AVERAGEWEEKLYPOSTS ON SEVENDAYPOSTCOUNTS.USER_ID = AVERAGEWEEKLYPOSTS.USER_ID 
GROUP BY 
  SEVENDAYPOSTCOUNTS.USER_ID, 
  AVERAGEWEEKLYPOSTS.AVG_WEEKLY_POSTS 
HAVING 
  MAX(SEVENDAYPOSTCOUNTS.POST_COUNT) >= AVERAGEWEEKLYPOSTS.AVG_WEEKLY_POSTS * 2 
ORDER BY 
  SEVENDAYPOSTCOUNTS.USER_ID;
```

# [3118. Friday Purchase III](https://leetcode.com/problems/friday-purchase-iii/)
```sql
WITH FRIDAYS AS (
    SELECT
        1 AS WEEK_OF_MONTH,
        CAST('2023-11-03' AS DATE) AS PURCHASE_DATE
    UNION ALL
    SELECT
        WEEK_OF_MONTH + 1,
        DATEADD(day, 7, PURCHASE_DATE)
    FROM FRIDAYS
    WHERE WEEK_OF_MONTH < 4
),
MEMBERSHIPS AS (
    SELECT 'Premium' AS MEMBERSHIP
    UNION ALL
    SELECT 'VIP'
)
SELECT
    f.WEEK_OF_MONTH,
    m.MEMBERSHIP,
    ISNULL(SUM(p.AMOUNT_SPEND), 0) AS TOTAL_AMOUNT
FROM FRIDAYS f
CROSS JOIN MEMBERSHIPS m
LEFT JOIN USERS u ON m.MEMBERSHIP = u.MEMBERSHIP
LEFT JOIN PURCHASES p ON f.PURCHASE_DATE = p.PURCHASE_DATE AND u.USER_ID = p.USER_ID
GROUP BY
    f.WEEK_OF_MONTH,
    m.MEMBERSHIP
ORDER BY
    f.WEEK_OF_MONTH,
    m.MEMBERSHIP;
```

# [3124. Find Longest Calls](https://leetcode.com/problems/find-longest-calls/)
```sql
WITH T AS (
    SELECT
        C2.FIRST_NAME,
        C1.TYPE,
        C1.DURATION,
        FORMAT(DATEADD(second, C1.DURATION, 0), 'HH:mm:ss') AS DURATION_FORMATTED,
        RANK() OVER (
            PARTITION BY C1.TYPE
            ORDER BY C1.DURATION DESC
        ) AS RK
    FROM
        CALLS AS C1
        JOIN CONTACTS AS C2 ON C1.CONTACT_ID = C2.ID
)
SELECT
    FIRST_NAME,
    TYPE,
    DURATION_FORMATTED
FROM T
WHERE RK <= 3
ORDER BY
    TYPE,
    DURATION DESC,
    FIRST_NAME DESC;
```

# [3126. Server Utilization Time](https://leetcode.com/problems/server-utilization-time/)
```sql
WITH
  SERVERNEIGHBORS AS (
    SELECT
      STATUS_TIME,
      SESSION_STATUS,
      LEAD(STATUS_TIME) OVER(
        PARTITION BY SERVER_ID
        ORDER BY STATUS_TIME
      ) AS NEXT_STATUS_TIME
    FROM SERVERS
  )
SELECT
  FLOOR(
    SUM(
      TIMESTAMPDIFF(SECOND, STATUS_TIME, NEXT_STATUS_TIME)
    ) / 86400
  ) AS TOTAL_UPTIME_DAYS
FROM SERVERNEIGHBORS
WHERE SERVERNEIGHBORS.SESSION_STATUS = 'start';
```

# [3140. Consecutive Available Seats II](https://leetcode.com/problems/consecutive-available-seats-ii/)
```sql
WITH
    T AS (
        SELECT
            *,
            SEAT_ID - (RANK() OVER (ORDER BY SEAT_ID)) AS GID
        FROM CINEMA
        WHERE FREE = 1
    ),
    P AS (
        SELECT
            MIN(SEAT_ID) AS FIRST_SEAT_ID,
            MAX(SEAT_ID) AS LAST_SEAT_ID,
            COUNT(1) AS CONSECUTIVE_SEATS_LEN,
            RANK() OVER (ORDER BY COUNT(1) DESC) AS RK
        FROM T
        GROUP BY GID
    )
SELECT FIRST_SEAT_ID, LAST_SEAT_ID, CONSECUTIVE_SEATS_LEN
FROM P
WHERE RK = 1
ORDER BY 1;
```

# [3166. Calculate Parking Fees and Duration](https://leetcode.com/problems/calculate-parking-fees-and-duration/)
```sql
WITH
    T AS (
        SELECT
            CAR_ID,
            LOT_ID,
            SUM(DATEDIFF(SECOND, ENTRY_TIME, EXIT_TIME)) AS DURATION
        FROM PARKINGTRANSACTIONS
        GROUP BY CAR_ID, LOT_ID
    ),
    P AS (
        SELECT
            *,
            RANK() OVER (
                PARTITION BY CAR_ID
                ORDER BY DURATION DESC
            ) AS RK
        FROM T
    )
SELECT
    T1.CAR_ID,
    SUM(T1.FEE_PAID) AS TOTAL_FEE_PAID,
    ROUND(
        SUM(CAST(T1.FEE_PAID AS FLOAT)) / (SUM(DATEDIFF(SECOND, T1.ENTRY_TIME, T1.EXIT_TIME)) / 3600.0),
        2
    ) AS AVG_HOURLY_FEE,
    T2.LOT_ID AS MOST_TIME_LOT
FROM
    PARKINGTRANSACTIONS AS T1
    LEFT JOIN P AS T2 ON T1.CAR_ID = T2.CAR_ID AND T2.RK = 1
GROUP BY
    T1.CAR_ID,
    T2.LOT_ID
ORDER BY T1.CAR_ID;
```

# [3182. Find Top Scoring Students](https://leetcode.com/problems/find-top-scoring-students/)
```sql
SELECT
    STUDENT_ID
FROM
    STUDENTS S
    JOIN COURSES C ON S.MAJOR = C.MAJOR
    LEFT JOIN ENROLLMENTS E ON S.STUDENT_ID = E.STUDENT_ID AND C.COURSE_ID = E.COURSE_ID
GROUP BY
    S.STUDENT_ID
HAVING
    SUM(CASE WHEN E.GRADE = 'A' THEN 1 ELSE 0 END) = COUNT(C.MAJOR)
ORDER BY
    S.STUDENT_ID;
```

# [3204. Bitwise User Permissions Analysis](https://leetcode.com/problems/bitwise-user-permissions-analysis/)
```sql
-- Function directly not available in SQL Sever
SELECT
    BIT_AND(PERMISSIONS) AS COMMON_PERMS,
    BIT_OR(PERMISSIONS) AS ANY_PERMS
FROM USER_PERMISSIONS;
```

# [3220. Odd and Even Transactions](https://leetcode.com/problems/odd-and-even-transactions/)
```sql
SELECT
    TRANSACTION_DATE,
    SUM(CASE WHEN AMOUNT % 2 = 1 THEN AMOUNT ELSE 0 END) AS ODD_SUM,
    SUM(CASE WHEN AMOUNT % 2 = 0 THEN AMOUNT ELSE 0 END) AS EVEN_SUM
FROM TRANSACTIONS
GROUP BY TRANSACTION_DATE
ORDER BY TRANSACTION_DATE;
```

# [3230. Customer Purchasing Behavior Analysis](https://leetcode.com/problems/customer-purchasing-behavior-analysis/)
```sql
WITH
    T AS (
        SELECT *
        FROM
            TRANSACTIONS
            JOIN PRODUCTS USING (PRODUCT_ID)
    ),
    P AS (
        SELECT
            CUSTOMER_ID,
            CATEGORY,
            COUNT(1) CNT,
            MAX(TRANSACTION_DATE) MAX_DATE
        FROM T
        GROUP BY 1, 2
    ),
    R AS (
        SELECT
            CUSTOMER_ID,
            CATEGORY,
            RANK() OVER (
                PARTITION BY CUSTOMER_ID
                ORDER BY CNT DESC, MAX_DATE DESC
            ) RK
        FROM P
    )
SELECT
    T.CUSTOMER_ID,
    ROUND(SUM(AMOUNT), 2) TOTAL_AMOUNT,
    COUNT(1) TRANSACTION_COUNT,
    COUNT(DISTINCT T.CATEGORY) UNIQUE_CATEGORIES,
    ROUND(AVG(AMOUNT), 2) AVG_TRANSACTION_AMOUNT,
    R.CATEGORY TOP_CATEGORY,
    ROUND(COUNT(1) * 10 + SUM(AMOUNT) / 100, 2) LOYALTY_SCORE
FROM
    T T
    JOIN R R ON T.CUSTOMER_ID = R.CUSTOMER_ID AND R.RK = 1
GROUP BY 1
ORDER BY 7 DESC, 1;
```

# [3252. Premier League Table Ranking II](https://leetcode.com/problems/premier-league-table-ranking-ii/)
```sql
WITH
    T AS (
        SELECT
            TEAM_NAME,
            WINS * 3 + DRAWS AS POINTS,
            RANK() OVER (ORDER BY WINS * 3 + DRAWS DESC) AS POSITION,
            COUNT(1) OVER () AS TOTAL_TEAMS
        FROM TEAMSTATS
    )
SELECT
    TEAM_NAME,
    POINTS,
    POSITION,
    CASE
        WHEN POSITION <= CEIL(TOTAL_TEAMS / 3.0) THEN 'TIER 1'
        WHEN POSITION <= CEIL(2 * TOTAL_TEAMS / 3.0) THEN 'TIER 2'
        ELSE 'TIER 3'
    END TIER
FROM T
ORDER BY 2 DESC, 1;
```

# [3262. Find Overlapping Shifts](https://leetcode.com/problems/find-overlapping-shifts/)
```sql
SELECT
    T1.EMPLOYEE_ID,
    COUNT(*) AS OVERLAPPING_SHIFTS
FROM
    EMPLOYEESHIFTS T1
    JOIN EMPLOYEESHIFTS T2
        ON T1.EMPLOYEE_ID = T2.EMPLOYEE_ID
        AND T1.START_TIME < T2.START_TIME
        AND T1.END_TIME > T2.START_TIME
GROUP BY
    T1.EMPLOYEE_ID
HAVING
    COUNT(*) > 0
ORDER BY
    T1.EMPLOYEE_ID;
```

# [3278. Find Candidates for Data Scientist Position II](https://leetcode.com/problems/find-candidates-for-data-scientist-position-ii/)
```sql
WITH PROJECTSKILLS AS (
    SELECT
        PROJECT_ID,
        COUNT(SKILL) AS REQUIRED_SKILLS
    FROM PROJECTS
    GROUP BY PROJECT_ID
),
CANDIDATESCORES AS (
    SELECT
        PROJECTS.PROJECT_ID,
        CANDIDATES.CANDIDATE_ID,
        100 + SUM(
            CASE
                WHEN CANDIDATES.PROFICIENCY > PROJECTS.IMPORTANCE THEN 10
                WHEN CANDIDATES.PROFICIENCY < PROJECTS.IMPORTANCE THEN -5
                ELSE 0
            END
        ) AS SCORE,
        COUNT(PROJECTS.SKILL) AS MATCHED_SKILLS
    FROM PROJECTS
    INNER JOIN CANDIDATES ON PROJECTS.SKILL = CANDIDATES.SKILL
    GROUP BY
        PROJECTS.PROJECT_ID,
        CANDIDATES.CANDIDATE_ID
),
RANKEDCANDIDATES AS (
    SELECT
        CANDIDATESCORES.PROJECT_ID,
        CANDIDATESCORES.CANDIDATE_ID,
        CANDIDATESCORES.SCORE,
        RANK() OVER (
            PARTITION BY CANDIDATESCORES.PROJECT_ID
            ORDER BY
                CANDIDATESCORES.SCORE DESC,
                CANDIDATESCORES.CANDIDATE_ID
        ) AS [RANK]
    FROM CANDIDATESCORES
    INNER JOIN PROJECTSKILLS ON CANDIDATESCORES.PROJECT_ID = PROJECTSKILLS.PROJECT_ID
    WHERE
        CANDIDATESCORES.MATCHED_SKILLS = PROJECTSKILLS.REQUIRED_SKILLS
)
SELECT
    PROJECT_ID,
    CANDIDATE_ID,
    SCORE
FROM RANKEDCANDIDATES
WHERE
    [RANK] = 1
ORDER BY
    PROJECT_ID;
```

# [3293. Calculate Product Final Price](https://leetcode.com/problems/calculate-product-final-price/)
```sql
SELECT
    PRODUCT_ID,
    PRICE * (100 - ISNULL(DISCOUNT, 0)) / 100 AS FINAL_PRICE,
    CATEGORY
FROM
    PRODUCTS
    LEFT JOIN DISCOUNTS ON PRODUCTS.CATEGORY = DISCOUNTS.CATEGORY
ORDER BY
    PRODUCT_ID;
```

# [3308. Find Top Performing Driver](https://leetcode.com/problems/find-top-performing-driver/)
```sql
WITH
    T AS (
        SELECT
            FUEL_TYPE,
            DRIVER_ID,
            ROUND(AVG(RATING), 2) AS RATING,
            SUM(DISTANCE) AS DISTANCE,
            SUM(ACCIDENTS) AS ACCIDENTS
        FROM
            DRIVERS
            JOIN VEHICLES ON DRIVERS.DRIVER_ID = VEHICLES.DRIVER_ID
            JOIN TRIPS ON VEHICLES.VEHICLE_ID = TRIPS.VEHICLE_ID
        GROUP BY
            FUEL_TYPE,
            DRIVER_ID
    ),
    P AS (
        SELECT
            *,
            RANK() OVER (
                PARTITION BY FUEL_TYPE
                ORDER BY RATING DESC, DISTANCE DESC, ACCIDENTS ASC
            ) AS [RK]
        FROM T
    )
SELECT
    FUEL_TYPE, DRIVER_ID, RATING, DISTANCE
FROM P
WHERE
    [RK] = 1
ORDER BY
    FUEL_TYPE;
```

# [3322. Premier League Table Ranking III](https://leetcode.com/problems/premier-league-table-ranking-iii/)
```sql
WITH TEAMSTATSCALCULATED AS (
    SELECT
        SEASON_ID,
        TEAM_ID,
        TEAM_NAME,
        WINS * 3 + DRAWS AS POINTS,
        GOALS_FOR - GOALS_AGAINST AS GOAL_DIFFERENCE
    FROM
        SEASONSTATS
)
SELECT
    SEASON_ID,
    TEAM_ID,
    TEAM_NAME,
    POINTS,
    GOAL_DIFFERENCE,
    RANK() OVER (
        PARTITION BY SEASON_ID
        ORDER BY
            POINTS DESC,
            GOAL_DIFFERENCE DESC,
            TEAM_NAME
    ) AS POSITION
FROM
    TEAMSTATSCALCULATED
ORDER BY
    SEASON_ID, POSITION, TEAM_NAME;
```

# [3328. Find Cities in Each State II](https://leetcode.com/problems/find-cities-in-each-state-ii/)
```sql
SELECT
    STATE,
    STRING_AGG(CITY, ', ') WITHIN GROUP (ORDER BY CITY) AS CITIES,
    COUNT(
        CASE
            WHEN LEFT(CITY, 1) = LEFT(STATE, 1) THEN 1
        END
    ) AS MATCHING_LETTER_COUNT
FROM CITIES
GROUP BY STATE
HAVING COUNT(CITY) >= 3 AND COUNT(CASE WHEN LEFT(CITY, 1) = LEFT(STATE, 1) THEN 1 END) > 0
ORDER BY MATCHING_LETTER_COUNT DESC, STATE;
```

# [3338. Second Highest Salary II](https://leetcode.com/problems/second-highest-salary-ii/)
```sql
WITH
  RANKEDEMPLOYEES AS (
    SELECT *, DENSE_RANK() OVER(
      PARTITION BY DEPT
      ORDER BY SALARY DESC
    ) AS RNK
    FROM EMPLOYEES
  )
SELECT EMP_ID, DEPT
FROM RANKEDEMPLOYEES
WHERE RNK = 2
ORDER BY 1;
```

# [3421. Find Students Who Improved](https://leetcode.com/problems/find-students-who-improved/)
```sql
WITH
  RANKEDSCORES AS (
    SELECT
      STUDENT_ID,
      SUBJECT,
      SCORE,
      EXAM_DATE,
      RANK() OVER (PARTITION BY STUDENT_ID, SUBJECT ORDER BY EXAM_DATE) AS RN_ASC,
      RANK() OVER (PARTITION BY STUDENT_ID, SUBJECT ORDER BY EXAM_DATE DESC) AS RN_DESC
    FROM SCORES
  ),
  FIRSTLASTSCORES AS (
    SELECT
      STUDENT_ID,
      SUBJECT,
      MIN(CASE WHEN RN_ASC = 1 THEN SCORE END) AS FIRST_SCORE,
      MAX(CASE WHEN RN_DESC = 1 THEN SCORE END) AS LATEST_SCORE
    FROM RANKEDSCORES GROUP BY STUDENT_ID, SUBJECT
    HAVING COUNT(*) > 1
  )
SELECT STUDENT_ID, SUBJECT, FIRST_SCORE, LATEST_SCORE
FROM FIRSTLASTSCORES
WHERE LATEST_SCORE > FIRST_SCORE
ORDER BY STUDENT_ID, SUBJECT
```

# [3475. DNA Pattern Recognition](https://leetcode.com/problems/dna-pattern-recognition/)
```sql
SELECT
  *,
  IIF(DNA_SEQUENCE LIKE 'ATG%', 1, 0) AS HAS_START,
  IIF(DNA_SEQUENCE LIKE '%TAA' OR DNA_SEQUENCE LIKE '%TAG' OR DNA_SEQUENCE LIKE '%TGA', 1, 0) AS HAS_STOP,
  IIF(DNA_SEQUENCE LIKE '%ATAT%', 1, 0) AS HAS_ATAT,
  IIF(DNA_SEQUENCE LIKE '%GGG%', 1, 0) AS HAS_GGG
FROM SAMPLES
ORDER BY SAMPLE_ID;
```

# [3497. Analyze Subscription Conversion](https://leetcode.com/problems/analyze-subscription-conversion/)
```sql
WITH
  FREETRIAL AS (
    SELECT USER_ID, AVG(ACTIVITY_DURATION * 1.0) AS AVG_FREE_TRIAL_DURATION
    FROM USERACTIVITY
    WHERE ACTIVITY_TYPE = 'free_trial'
    GROUP BY USER_ID
  ),
  PAID AS (
    SELECT USER_ID, AVG(ACTIVITY_DURATION * 1.0) AS AVG_PAID_DURATION
    FROM USERACTIVITY
    WHERE ACTIVITY_TYPE = 'paid'
    GROUP BY USER_ID
  ),
  CONVERTEDUSERS AS (
    SELECT DISTINCT FREETRIAL.USER_ID
    FROM FREETRIAL
    INNER JOIN PAID
      ON FREETRIAL.USER_ID = PAID.USER_ID
  )
SELECT
  CONVERTEDUSERS.USER_ID,
  ROUND(FREETRIAL.AVG_FREE_TRIAL_DURATION, 2) AS TRIAL_AVG_DURATION,
  ROUND(PAID.AVG_PAID_DURATION, 2) AS PAID_AVG_DURATION
FROM CONVERTEDUSERS
INNER JOIN FREETRIAL
  ON CONVERTEDUSERS.USER_ID = FREETRIAL.USER_ID
INNER JOIN PAID
  ON CONVERTEDUSERS.USER_ID = PAID.USER_ID
ORDER BY 1;
```

# [3521. Find Product Recommendation Pairs](https://leetcode.com/problems/find-product-recommendation-pairs/)
```sql
WITH PRODUCTPAIRS AS (
    SELECT
        P1.USER_ID,
        P1.PRODUCT_ID AS PRODUCT1_ID,
        P2.PRODUCT_ID AS PRODUCT2_ID
    FROM
        PRODUCTPURCHASES AS P1
    JOIN
        PRODUCTPURCHASES AS P2
        ON P1.USER_ID = P2.USER_ID
    WHERE
        P1.PRODUCT_ID < P2.PRODUCT_ID
)
SELECT
    TP.PRODUCT1_ID,
    TP.PRODUCT2_ID,
    PI1.CATEGORY AS PRODUCT1_CATEGORY,
    PI2.CATEGORY AS PRODUCT2_CATEGORY,
    COUNT(DISTINCT TP.USER_ID) AS CUSTOMER_COUNT
FROM
    PRODUCTPAIRS AS TP
JOIN
    PRODUCTINFO AS PI1
    ON TP.PRODUCT1_ID = PI1.PRODUCT_ID
JOIN
    PRODUCTINFO AS PI2
    ON TP.PRODUCT2_ID = PI2.PRODUCT_ID
GROUP BY
    TP.PRODUCT1_ID,
    TP.PRODUCT2_ID,
    PI1.CATEGORY,
    PI2.CATEGORY
HAVING
    COUNT(DISTINCT TP.USER_ID) >= 3
ORDER BY
    CUSTOMER_COUNT DESC,
    PRODUCT1_ID ASC,
    PRODUCT2_ID ASC;
```

# [3564. Seasonal Sales Analysis](https://leetcode.com/problems/seasonal-sales-analysis/)
```sql
WITH
    SEASONALSALES AS (
        SELECT
            CASE
                WHEN MONTH(S.SALE_DATE) IN (12, 1, 2) THEN 'Winter'
                WHEN MONTH(S.SALE_DATE) IN (3, 4, 5) THEN 'Spring'
                WHEN MONTH(S.SALE_DATE) IN (6, 7, 8) THEN 'Summer'
                WHEN MONTH(S.SALE_DATE) IN (9, 10, 11) THEN 'Fall'
            END AS SEASON,
            P.CATEGORY,
            SUM(S.QUANTITY) AS TOTAL_QUANTITY,
            SUM(S.QUANTITY * S.PRICE) AS TOTAL_REVENUE
        FROM
            SALES AS S
        JOIN PRODUCTS AS P
            ON S.PRODUCT_ID = P.PRODUCT_ID
        GROUP BY
            CASE
                WHEN MONTH(S.SALE_DATE) IN (12, 1, 2) THEN 'Winter'
                WHEN MONTH(S.SALE_DATE) IN (3, 4, 5) THEN 'Spring'
                WHEN MONTH(S.SALE_DATE) IN (6, 7, 8) THEN 'Summer'
                WHEN MONTH(S.SALE_DATE) IN (9, 10, 11) THEN 'Fall'
            END,
            P.CATEGORY
    ),
    TOPCATEGORYPERSEASON AS (
        SELECT
            SEASON,
            CATEGORY,
            TOTAL_QUANTITY,
            TOTAL_REVENUE,
            RANK() OVER (
                PARTITION BY SEASON
                ORDER BY TOTAL_QUANTITY DESC, TOTAL_REVENUE DESC
            ) AS RK
        FROM SEASONALSALES
    )
SELECT
    SEASON,
    CATEGORY,
    TOTAL_QUANTITY,
    TOTAL_REVENUE
FROM
    TOPCATEGORYPERSEASON
WHERE
    RK = 1
ORDER BY
    1;
```

# [3580. Find Consistently Improving Employees](https://leetcode.com/problems/find-consistently-improving-employees/)
```sql
WITH
    RECENT AS (
        SELECT
            EMPLOYEE_ID,
            REVIEW_DATE,
            RATING,
            ROW_NUMBER() OVER (
                PARTITION BY EMPLOYEE_ID
                ORDER BY REVIEW_DATE DESC
            ) AS RN,
            (
                LAG(RATING) OVER (
                    PARTITION BY EMPLOYEE_ID
                    ORDER BY REVIEW_DATE DESC
                ) - RATING
            ) AS DELTA
        FROM PERFORMANCE_REVIEWS
    )
SELECT
    R.EMPLOYEE_ID,
    E.NAME,
    SUM(R.DELTA) AS IMPROVEMENT_SCORE
FROM
    RECENT R
    JOIN EMPLOYEES E ON R.EMPLOYEE_ID = E.EMPLOYEE_ID
WHERE R.RN > 1 AND R.RN <= 3
GROUP BY R.EMPLOYEE_ID, E.NAME
HAVING COUNT(*) = 2 AND MIN(R.DELTA) > 0
ORDER BY 3 DESC, 2;
```

# [3586. Find COVID Recovery Patients](https://leetcode.com/problems/find-covid-recovery-patients/)
```sql
WITH
    FIRST_POSITIVE AS (
        SELECT
            PATIENT_ID,
            MIN(TEST_DATE) AS FIRST_POSITIVE_DATE
        FROM COVID_TESTS
        WHERE RESULT = 'Positive'
        GROUP BY PATIENT_ID
    ),
    FIRST_NEGATIVE_AFTER_POSITIVE AS (
        SELECT
            T.PATIENT_ID,
            MIN(T.TEST_DATE) AS FIRST_NEGATIVE_DATE
        FROM
            COVID_TESTS T
            JOIN FIRST_POSITIVE P
                ON T.PATIENT_ID = P.PATIENT_ID AND T.TEST_DATE > P.FIRST_POSITIVE_DATE
        WHERE T.RESULT = 'Negative'
        GROUP BY T.PATIENT_ID
    )
SELECT
    P.PATIENT_ID,
    P.PATIENT_NAME,
    P.AGE,
    DATEDIFF(day, F.FIRST_POSITIVE_DATE, N.FIRST_NEGATIVE_DATE) AS RECOVERY_TIME
FROM
    FIRST_POSITIVE F
    JOIN FIRST_NEGATIVE_AFTER_POSITIVE N ON F.PATIENT_ID = N.PATIENT_ID
    JOIN PATIENTS P ON P.PATIENT_ID = F.PATIENT_ID
ORDER BY RECOVERY_TIME ASC, PATIENT_NAME ASC;
```

# [3601. Find Drivers with Improved Fuel Efficiency](https://leetcode.com/problems/find-drivers-with-improved-fuel-efficiency/)
```sql
SELECT A.DRIVER_ID, DRIVER_NAME
    , ROUND(FIRST_HALF_AVG, 2) FIRST_HALF_AVG
    , ROUND(SECOND_HALF_AVG, 2) SECOND_HALF_AVG
    , ROUND((SECOND_HALF_AVG - FIRST_HALF_AVG), 2) AS EFFICIENCY_IMPROVEMENT 
    FROM (
    SELECT DRIVER_ID
    , AVG(CASE WHEN MONTH(TRIP_DATE) <= 6 THEN DISTANCE_KM*1.0/FUEL_CONSUMED END) AS FIRST_HALF_AVG 
    , AVG(CASE WHEN MONTH(TRIP_DATE) > 6 THEN DISTANCE_KM*1.0/FUEL_CONSUMED END) AS SECOND_HALF_AVG

    FROM TRIPS
    GROUP BY DRIVER_ID
) A 
LEFT JOIN DRIVERS D ON A.DRIVER_ID = D.DRIVER_ID
WHERE (SECOND_HALF_AVG - FIRST_HALF_AVG) > 0
```

# [3611. Find Overbooked Employees](https://leetcode.com/problems/find-overbooked-employees/)
```sql
SET DATEFIRST 1; -- To start the week from Monday .It can change database to database
WITH PROCESS_1 AS (
    SELECT 
        EMPLOYEE_ID,
        DATEPART(WEEK, MEETING_DATE) AS WEEK, 
        DATEPART(YEAR, MEETING_DATE) AS YR,
        SUM(DURATION_HOURS) AS DURATION_TOTAL
    FROM MEETINGS
    GROUP BY 
        EMPLOYEE_ID, 
        DATEPART(WEEK, MEETING_DATE), 
        DATEPART(YEAR, MEETING_DATE)
)
SELECT 
    P.EMPLOYEE_ID, 
    E.EMPLOYEE_NAME, 
    E.DEPARTMENT, 
    COUNT(P.EMPLOYEE_ID) AS MEETING_HEAVY_WEEKS 
FROM PROCESS_1 P
INNER JOIN EMPLOYEES E ON P.EMPLOYEE_ID = E.EMPLOYEE_ID
WHERE DURATION_TOTAL > 20
GROUP BY 
    P.EMPLOYEE_ID, 
    E.EMPLOYEE_NAME, 
    E.DEPARTMENT
HAVING COUNT(P.EMPLOYEE_ID) > 1
ORDER BY 
    MEETING_HEAVY_WEEKS DESC, 
    EMPLOYEE_NAME;
```

# [3626. Find Stores with Inventory Imbalance](https://leetcode.com/problems/find-stores-with-inventory-imbalance/)
```sql
WITH MIN_MAX_PRODUCT AS (
  SELECT 
    STORE_ID, 
    MIN(PRICE) AS MIN_PRICE, 
    MAX(PRICE) AS MAX_PRICE 
  FROM 
    INVENTORY 
  GROUP BY 
    STORE_ID 
  HAVING 
    COUNT(DISTINCT PRODUCT_NAME) > = 3
), 
MIN_MAX_PRODUCT_QUANT AS (
  SELECT 
    INV.STORE_ID, 
    ROUND(
      MIN(
        CASE WHEN MIN_PRICE = PRICE THEN QUANTITY ELSE NULL END
      ) * 1.0 / MAX(
        CASE WHEN MAX_PRICE = PRICE THEN QUANTITY ELSE NULL END
      ), 
      2
    ) AS IMBALANCE_RATIO, 
    MIN(
      CASE WHEN MIN_PRICE = PRICE THEN PRODUCT_NAME ELSE NULL END
    ) AS CHEAPEST_PRODUCT, 
    MAX(
      CASE WHEN MAX_PRICE = PRICE THEN PRODUCT_NAME ELSE NULL END
    ) AS MOST_EXP_PRODUCT 
  FROM 
    INVENTORY INV 
    INNER JOIN MIN_MAX_PRODUCT P ON P.STORE_ID = INV.STORE_ID 
  GROUP BY 
    INV.STORE_ID
) 
SELECT 
  A.STORE_ID, 
  STORE_NAME, 
  LOCATION, 
  MOST_EXP_PRODUCT, 
  CHEAPEST_PRODUCT, 
  IMBALANCE_RATIO 
FROM 
  MIN_MAX_PRODUCT_QUANT A 
  INNER JOIN STORES S ON S.STORE_ID = A.STORE_ID 
  AND IMBALANCE_RATIO > 1
ORDER BY 
  6 DESC, 2 ASC
```

# [3657. Find Loyal Customers](https://leetcode.com/problems/find-loyal-customers/)
```sql
```

# [534. Game Play Analysis III](https://leetcode.com/problems/game-play-analysis-iii/)
```sql
SELECT  
    ACTIVITY.PLAYER_ID,  
    ACTIVITY.EVENT_DATE,  
    SUM(PREVACTIVITY.GAMES_PLAYED) AS GAMES_PLAYED_SO_FAR
FROM ACTIVITY
INNER JOIN ACTIVITY AS PREVACTIVITY  
    ON (    
        ACTIVITY.PLAYER_ID = PREVACTIVITY.PLAYER_ID    
        AND ACTIVITY.EVENT_DATE >= PREVACTIVITY.EVENT_DATE
    )
GROUP BY 
    ACTIVITY.PLAYER_ID, 
    ACTIVITY.EVENT_DATE
ORDER BY 
    ACTIVITY.PLAYER_ID, 
    ACTIVITY.EVENT_DATE;
------------------------
SELECT
    PLAYER_ID,
    EVENT_DATE,
    SUM(GAMES_PLAYED) OVER (
        PARTITION BY PLAYER_ID
        ORDER BY EVENT_DATE
    ) AS GAMES_PLAYED_SO_FAR
FROM ACTIVITY
ORDER BY
    PLAYER_ID,
    EVENT_DATE;
```

# [550. Game Play Analysis IV](https://leetcode.com/problems/game-play-analysis-iv/)
```sql
WITH PLAYERS AS (
  SELECT PLAYER_ID, MIN(EVENT_DATE) AS FIRST_LOGIN
  FROM ACTIVITY
  GROUP BY PLAYER_ID
)
SELECT ROUND(
    CAST(COUNT(T2.PLAYER_ID) AS DECIMAL) / COUNT(T1.PLAYER_ID),
    2
  ) AS FRACTION
FROM PLAYERS AS T1
LEFT JOIN ACTIVITY AS T2
  ON T1.PLAYER_ID = T2.PLAYER_ID
  AND DATEDIFF(DAY, T1.FIRST_LOGIN, T2.EVENT_DATE) = 1;
```

# [570. Managers with at Least 5 Direct Reports](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/)
```sql
SELECT E1.NAME
FROM EMPLOYEE E1
JOIN (
    SELECT MANAGERID, COUNT(*) AS DIRECTREPORTS
    FROM EMPLOYEE
    GROUP BY MANAGERID
    HAVING COUNT(*) >= 5
) E2 ON E1.ID = E2.MANAGERID;
```

# [574. Winning Candidate](https://leetcode.com/problems/winning-candidate/)
```sql
SELECT C.NAME
FROM CANDIDATE AS C
LEFT JOIN VOTE AS V ON C.ID = V.CANDIDATEID
GROUP BY C.ID, C.NAME
ORDER BY COUNT(V.CANDIDATEID) DESC
OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY
```

# [578. Get Highest Answer Rate Question](https://leetcode.com/problems/get-highest-answer-rate-question/)
```sql
WITH T AS (
    SELECT
        QUESTION_ID AS SURVEY_LOG,
        CAST(SUM(CASE WHEN ACTION = 'answer' THEN 1 ELSE 0 END) OVER (PARTITION BY QUESTION_ID) AS FLOAT) /
        NULLIF(SUM(CASE WHEN ACTION = 'show' THEN 1 ELSE 0 END) OVER (PARTITION BY QUESTION_ID), 0) AS RATIO
    FROM SURVEYLOG
)
SELECT TOP 1 SURVEY_LOG
FROM T
ORDER BY RATIO DESC, SURVEY_LOG;
```

# [580. Count Student Number in Departments](https://leetcode.com/problems/count-student-number-in-departments/)
```sql
SELECT D.DEPT_NAME, COUNT(S.STUDENT_ID) AS STUDENT_NUMBER
FROM DEPARTMENT AS D
LEFT JOIN STUDENT AS S ON D.DEPT_ID = S.DEPT_ID
GROUP BY D.DEPT_ID, D.DEPT_NAME
ORDER BY STUDENT_NUMBER DESC, D.DEPT_NAME;
```

# [585. Investments in 2016](https://leetcode.com/problems/investments-in-2016/)
```sql
WITH T AS (
    SELECT 
        TIV_2016,
        COUNT(*) OVER (PARTITION BY TIV_2015) AS CNT_SAME_TIV_2015,
        COUNT(*) OVER (PARTITION BY LAT, LON) AS CNT_SAME_LOCATION
    FROM INSURANCE
)
SELECT ROUND(SUM(TIV_2016), 2) AS TIV_2016
FROM T
WHERE CNT_SAME_TIV_2015 > 1 AND CNT_SAME_LOCATION = 1;
```

# [602. Friend Requests II: Who Has the Most Friends](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/)
```sql
WITH BASE AS (
    SELECT REQUESTER_ID AS ID FROM REQUESTACCEPTED
    UNION ALL
    SELECT ACCEPTER_ID AS ID FROM REQUESTACCEPTED
)
SELECT TOP 1 ID, COUNT(*) AS NUM
FROM BASE
GROUP BY ID
ORDER BY NUM DESC;
```

# [608. Tree Node](https://leetcode.com/problems/tree-node/)
```sql
SELECT DISTINCT T1.ID, (
    CASE
    WHEN T1.P_ID IS NULL  THEN 'Root'
    WHEN T1.P_ID IS NOT NULL AND T2.ID IS NOT NULL THEN 'Inner'
    WHEN T1.P_ID IS NOT NULL AND T2.ID IS NULL THEN 'Leaf'
    END
) AS TYPE 
FROM TREE T1
LEFT JOIN TREE T2
ON T1.ID = T2.P_ID
```

# [612. Shortest Distance in a Plane](https://leetcode.com/problems/shortest-distance-in-a-plane/)
```sql
SELECT ROUND(SQRT(MIN(POWER(p2.x - p1.x, 2) + POWER(p2.y - p1.y, 2))), 2) AS shortest
FROM point_2d p1
JOIN point_2d p2
    ON p1.x <> p2.x OR p1.y <> p2.y;
```

# [614. Second Degree Follower](https://leetcode.com/problems/second-degree-follower/)
```sql
SELECT F1.FOLLOWER, COUNT(DISTINCT F2.FOLLOWER) AS NUM
FROM FOLLOW AS F1
JOIN FOLLOW AS F2 ON F1.FOLLOWER = F2.FOLLOWEE
GROUP BY F1.FOLLOWER
ORDER BY F1.FOLLOWER;
```

# [626. Exchange Seats](https://leetcode.com/problems/exchange-seats/)
```sql
SELECT
    CASE
        WHEN MOD(ID, 2) <> 0 AND ID = (SELECT MAX(ID) FROM SEAT) THEN ID -- ODD ID AND IT'S THE LAST ID
        WHEN MOD(ID, 2) <> 0 THEN ID + 1 -- ODD ID, SWAP WITH THE NEXT ID
        ELSE ID - 1 -- EVEN ID, SWAP WITH THE PREVIOUS ID
    END AS ID,
    STUDENT
FROM
    SEAT
ORDER BY
    ID ASC;
---------------------------
SELECT
    ID,
    CASE
        WHEN MOD(ID, 2) = 1 AND LEAD(STUDENT, 1, STUDENT) OVER (ORDER BY ID) IS NOT NULL THEN LEAD(STUDENT, 1, STUDENT) OVER (ORDER BY ID)
        WHEN MOD(ID, 2) = 0 THEN LAG(STUDENT) OVER (ORDER BY ID)
        ELSE STUDENT -- THIS CASE IS TECHNICALLY COVERED BY LEAD'S DEFAULT OR THE FIRST WHEN, BUT GOOD FOR CLARITY.
    END AS STUDENT
FROM
    SEAT
ORDER BY
    ID ASC;
```

# [627. Swap Salary](https://leetcode.com/problems/swap-salary/)
```sql
UPDATE SALARY SET SEX = CASE WHEN SEX = 'm' THEN 'f' ELSE 'm' END;
```