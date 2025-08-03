## Easy
### 1050. Actors and Directors Who Cooperated At Least Three Times
```sql
SELECT ACTOR_ID, DIRECTOR_ID FROM ACTORDIRECTOR GROUP BY ACTOR_ID, DIRECTOR_ID HAVING COUNT(*) >= 3
```
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
### 1148. Article Views I
```sql
SELECT DISTINCT AUTHOR_ID AS ID
FROM VIEWS
WHERE AUTHOR_ID = VIEWER_ID
ORDER BY ID ASC;
```
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
### 1211. Queries Quality and Percentage
```sql
SELECT QUERY_NAME,
       ROUND(SUM(RATING*1.0/POSITION)*1.0/COUNT(*),2) AS QUALITY,
       ROUND(COUNT(CASE WHEN RATING<3 THEN 1 ELSE NULL END)*100.00/COUNT(*), 2) AS POOR_QUERY_PERCENTAGE 
FROM QUERIES
GROUP BY QUERY_NAME
```
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
### 1303. Find the Team Size
```sql
SELECT
  EMPLOYEE_ID,
  COUNT(*) OVER(PARTITION BY TEAM_ID) AS TEAM_SIZE
FROM EMPLOYEE;
```
### 1322. Ads Performance
```sql
SELECT
    AD_ID,
    ROUND(IFNULL(SUM(ACTION = 'Clicked') / SUM(ACTION IN ('Clicked', 'Viewed')) * 100, 0), 2) AS CTR
FROM ADS
GROUP BY 1
ORDER BY 2 DESC, 1;
```
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
### 1378. Replace Employee ID With The Unique Identifier
```sql
SELECT
  EU.UNIQUE_ID,
  E.NAME
FROM EMPLOYEES E
LEFT JOIN EMPLOYEEUNI EU
ON E.ID = EU.ID;
```
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
### 1527. Patients With a Condition
```sql
SELECT *
FROM PATIENTS
WHERE
    CONDITIONS LIKE 'DIAB1%' OR
    CONDITIONS LIKE '% DIAB1%';
```
### 1543. Fix Product Name Format
```sql
```
### 1565. Unique Orders and Customers Per Month
```sql
```
### 1571. Warehouse Manager
```sql
```
### 1581. Customer Who Visited but Did Not Make Any Transactions
```sql
```
### 1587. Bank Account Summary II
```sql
```
### 1607. Sellers With No Sales
```sql
```
### 1623. All Valid Triplets That Can Represent a Country
```sql
```
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
### 1661. Average Time of Process per Machine
```sql
```
### 1667. Fix Names in a Table
```sql
```
### 1677. Product's Worth Over Invoices
```sql
```
### 1683. Invalid Tweets
```sql
```
### 1693. Daily Leads and Partners
```sql
```
### 1729. Find Followers Count
```sql
```
### 1731. The Number of Employees Which Report to Each Employee
```sql
```
### 1741. Find Total Time Spent by Each Employee
```sql
```
### 175. Combine Two Tables
```sql
```
### 1757. Recyclable and Low Fat Products
```sql
SELECT PRODUCT_ID
FROM PRODUCTS
WHERE LOW_FATS = 'Y' AND RECYCLABLE = 'Y';
```
### 1777. Product's Price for Each Store
```sql
```
### 1789. Primary Department for Each Employee
```sql
```
### 1795. Rearrange Products Table
```sql
```
### 1809. Ad-Free Sessions
```sql
```
### 181. Employees Earning More Than Their Managers
```sql
```
### 182. Duplicate Emails
```sql
```
### 1821. Find Customers With Positive Revenue this Year
```sql
```
### 183. Customers Who Never Order
```sql
```
### 1853. Convert Date Format
```sql
```
### 1873. Calculate Special Bonus
```sql
```
### 1890. The Latest Login in
```sql
```
### 1939. Users That Actively Request Confirmation Messages
```sql
```
### 196. Delete Duplicate Emails
```sql
```
### 1965. Employees With Missing Information
```sql
```
### 197. Rising Temperature
```sql
```
### 1978. Employees Whose Manager Left the Company
```sql
```
### 2026. Low-Quality Problems
```sql
```
### 2072. The Winner University
```sql
```
### 2082. The Number of Rich Customers
```sql
```
### 2205. The Number of Users That Are Eligible for Discount
```sql
```
### 2230. The Users That Are Eligible for Discount
```sql
```
### 2329. Product Sales Analysis V
```sql
```
### 2339. All the Matches of the League
```sql
```
### 2356. Number of Unique Subjects Taught by Each Teacher
```sql
```
### 2377. Sort the Olympic Table
```sql
```
### 2480. Form a Chemical Bond
```sql
```
### 2504. Concatenate the Name and the Profession
```sql
```
### 2668. Find Latest Salaries
```sql
```
### 2669. Count Artist Occurrences On Spotify Ranking List
```sql
```
### 2687. Bikes Last Time Used
```sql
```
### 2837. Total Traveled Distance
```sql
```
### 2853. Highest Salaries Difference
```sql
```
### 2985. Calculate Compressed Mean
```sql
```
### 2987. Find Expensive Cities
```sql
```
### 2990. Loan Types
```sql
```
### 3051. Find Candidates for Data Scientist Position
```sql
```
### 3053. Classifying Triangles by Lengths
```sql
```
### 3059. Find All Unique Email Domains
```sql
```
### 3150. Invalid Tweets II
```sql
```
### 3172. Second Day Verification
```sql
```
### 3198. Find Cities in Each State
```sql
```
### 3246. Premier League Table Ranking
```sql
```
### 3358. Books with NULL Ratings
```sql
```
### 3415. Find Products with Three Consecutive Digits
```sql
```
### 3436. Find Valid Emails
```sql
```
### 3465. Find Products with Valid Serial Numbers
```sql
```
### 3570. Find Books with No Available Copies
```sql
```
### 511. Game Play Analysis I
```sql
```
### 512. Game Play Analysis II
```sql
```
### 577. Employee Bonus
```sql
```
### 584. Find Customer Referee
```sql
```
### 586. Customer Placing the Largest Number of Orders
```sql
```
### 595. Big Countries
```sql
```
### 596. Classes With at Least 5 Students
```sql
```
### 597. Friend Requests I: Overall Acceptance Rate
```sql
```
### 603. Consecutive Available Seats
```sql
```
### 607. Sales Person
```sql
```
### 610. Triangle Judgement
```sql
```
### 613. Shortest Distance in a Line
```sql
```
### 619. Biggest Single Number
```sql
```
### 620. Not Boring Movies
```sql
```
## Medium
### 1045. Customers Who Bought All Products
```sql
```
### 1070. Product Sales Analysis III
```sql
```
### 1077. Project Employees III
```sql
```
### 1098. Unpopular Books
```sql
```
### 1107. New Users Daily Count
```sql
```
### 1112. Highest Grade For Each Student
```sql
```
### 1126. Active Businesses
```sql
```
### 1132. Reported Posts II
```sql
```
### 1149. Article Views II
```sql
```
### 1158. Market Analysis I
```sql
```
### 1164. Product Price at a Given Date
```sql
```
### 1174. Immediate Food Delivery II
```sql
```
### 1193. Monthly Transactions I
```sql
```
### 1204. Last Person to Fit in the Bus
```sql
```
### 1205. Monthly Transactions II
```sql
```
### 1212. Team Scores in Football Tournament
```sql
```
### 1264. Page Recommendations
```sql
```
### 1270. All People Report to the Given Manager
```sql
```
### 1285. Find the Start and End Number of Continuous Ranges
```sql
```
### 1308. Running Total for Different Genders
```sql
```
### 1321. Restaurant Growth
```sql
```
### 1341. Movie Rating
```sql
```
### 1355. Activity Participants
```sql
```
### 1364. Number of Trusted Contacts of a Customer
```sql
```
### 1393. Capital Gain/Loss
```sql
```
### 1398. Customers Who Bought Products A and B but Not C
```sql
```
### 1440. Evaluate Boolean Expression
```sql
```
### 1445. Apples & Oranges
```sql
```
### 1454. Active Users
```sql
```
### 1459. Rectangles Area
```sql
```
### 1468. Calculate Salaries
```sql
```
### 1501. Countries You Can Safely Invest In
```sql
```
### 1532. The Most Recent Three Orders
```sql
```
### 1549. The Most Recent Orders for Each Product
```sql
```
### 1555. Bank Account Summary
```sql
```
### 1596. The Most Frequently Ordered Products for Each Customer
```sql
```
### 1613. Find the Missing IDs
```sql
```
### 1699. Number of Calls Between Two Persons
```sql
```
### 1709. Biggest Window Between Visits
```sql
```
### 1715. Count Apples and Oranges
```sql
```
### 1747. Leetflex Banned Accounts
```sql
```
### 176. Second Highest Salary
```sql
```
### 177. Nth Highest Salary
```sql
```
### 178. Rank Scores
```sql
```
### 1783. Grand Slam Titles
```sql
```
### 180. Consecutive Numbers
```sql
```
### 1811. Find Interview Candidates
```sql
```
### 1831. Maximum Transaction Each Day
```sql
```
### 184. Department Highest Salary
```sql
```
### 1841. League Statistics
```sql
```
### 1843. Suspicious Bank Accounts
```sql
```
### 1867. Orders With Maximum Quantity Above Average
```sql
```
### 1875. Group Employees of the Same Salary
```sql
```
### 1907. Count Salary Categories
```sql
```
### 1934. Confirmation Rate
```sql
```
### 1949. Strong Friendship
```sql
```
### 1951. All the Pairs With the Maximum Number of Common Followers
```sql
```
### 1988. Find Cutoff Score for Each School
```sql
```
### 1990. Count the Number of Experiments
```sql
```
### 2020. Number of Accounts That Did Not Stream
```sql
```
### 2041. Accepted Candidates From the Interviews
```sql
```
### 2051. The Category of Each Member in the Store
```sql
```
### 2066. Account Balance
```sql
```
### 2084. Drop Type 1 Orders for Customers With Type 0 Orders
```sql
```
### 2112. The Airport With the Most Traffic
```sql
```
### 2142. The Number of Passengers in Each Bus I
```sql
```
### 2159. Order Two Columns Independently
```sql
```
### 2175. The Change in Global Rankings
```sql
```
### 2228. Users With Two Purchases Within Seven Days
```sql
```
### 2238. Number of Times a Driver Was a Passenger
```sql
```
### 2292. Products With Three or More Orders in Two Consecutive Years
```sql
```
### 2298. Tasks Count in the Weekend
```sql
```
### 2308. Arrange Table by Gender
```sql
```
### 2314. The First Day of the Maximum Recorded Degree in Each City
```sql
```
### 2324. Product Sales Analysis IV
```sql
```
### 2346. Compute the Rank as a Percentage
```sql
```
### 2372. Calculate the Influence of Each Salesperson
```sql
```
### 2388. Change Null Values in a Table to the Previous Value
```sql
```
### 2394. Employees With Deductions
```sql
```
### 2686. Immediate Food Delivery III
```sql
```
### 2688. Find Active Users
```sql
```
### 2738. Count Occurrences in Text
```sql
```
### 2783. Flight Occupancy and Waitlist Analysis
```sql
```
### 2820. Election Results
```sql
```
### 2854. Rolling Average Steps
```sql
```
### 2893. Calculate Orders Within Each Interval
```sql
```
### 2922. Market Analysis III
```sql
```
### 2978. Symmetric Coordinates
```sql
```
### 2984. Find Peak Calling Hours for Each City
```sql
```
### 2986. Find Third Transaction
```sql
```
### 2988. Manager of the Largest Department
```sql
```
### 2989. Class Performance
```sql
```
### 2993. Friday Purchases I
```sql
```
### 3050. Pizza Toppings Cost Analysis
```sql
```
### 3054. Binary Tree Nodes
```sql
```
### 3055. Top Percentile Fraud
```sql
```
### 3056. Snaps Analysis
```sql
```
### 3058. Friends With No Mutual Friends
```sql
```
### 3087. Find Trending Hashtags
```sql
```
### 3089. Find Bursty Behavior
```sql
```
### 3118. Friday Purchase III
```sql
```
### 3124. Find Longest Calls
```sql
```
### 3126. Server Utilization Time
```sql
```
### 3140. Consecutive Available Seats II
```sql
```
### 3166. Calculate Parking Fees and Duration
```sql
```
### 3182. Find Top Scoring Students
```sql
```
### 3204. Bitwise User Permissions Analysis
```sql
```
### 3220. Odd and Even Transactions
```sql
```
### 3230. Customer Purchasing Behavior Analysis
```sql
```
### 3252. Premier League Table Ranking II
```sql
```
### 3262. Find Overlapping Shifts
```sql
```
### 3278. Find Candidates for Data Scientist Position II
```sql
```
### 3293. Calculate Product Final Price
```sql
```
### 3308. Find Top Performing Driver
```sql
```
### 3322. Premier League Table Ranking III
```sql
```
### 3328. Find Cities in Each State II
```sql
```
### 3338. Second Highest Salary II
```sql
```
### 3421. Find Students Who Improved
```sql
```
### 3475. DNA Pattern Recognition
```sql
```
### 3497. Analyze Subscription Conversion
```sql
```
### 3521. Find Product Recommendation Pairs
```sql
```
### 3564. Seasonal Sales Analysis
```sql
```
### 3580. Find Consistently Improving Employees
```sql
```
### 3586. Find COVID Recovery Patients
```sql
```
### 3601. Find Drivers with Improved Fuel Efficiency
```sql
```
### 3611. Find Overbooked Employees
```sql
```
### 3626. Find Stores with Inventory Imbalance
```sql
```
### 534. Game Play Analysis III
```sql
```
### 550. Game Play Analysis IV
```sql
```
### 570. Managers with at Least 5 Direct Reports
```sql
```
### 574. Winning Candidate
```sql
```
### 578. Get Highest Answer Rate Question
```sql
```
### 580. Count Student Number in Departments
```sql
```
### 585. Investments in
```sql
```
### 602. Friend Requests II: Who Has the Most Friends
```sql
```
### 608. Tree Node
```sql
```
### 612. Shortest Distance in a Plane
```sql
```
### 614. Second Degree Follower
```sql
```
### 626. Exchange Seats
```sql
```
### 627. Swap Salary
```sql
```
## Hard
### 1097. Game Play Analysis V
```sql
```
### 1127. User Purchase Platform
```sql
```
### 1159. Market Analysis II
```sql
```
### 1194. Tournament Winners
```sql
```
### 1225. Report Contiguous Dates
```sql
```
### 1336. Number of Transactions per Visit
```sql
```
### 1369. Get the Second Most Recent Activity
```sql
```
### 1384. Total Sales Amount by Year
```sql
```
### 1412. Find the Quiet Students in All Exams
```sql
```
### 1479. Sales by Day of the Week
```sql
```
### 1635. Hopper Company Queries I
```sql
```
### 1645. Hopper Company Queries II
```sql
```
### 1651. Hopper Company Queries III
```sql
```
### 1767. Find the Subtasks That Did Not Execute
```sql
```
### 185. Department Top Three Salaries
```sql
```
### 1892. Page Recommendations II
```sql
```
### 1917. Leetcodify Friends Recommendations
```sql
```
### 1919. Leetcodify Similar Friends
```sql
```
### 1972. First and Last Call On the Same Day
```sql
```
### 2004. The Number of Seniors and Juniors to Join the Company
```sql
```
### 2010. The Number of Seniors and Juniors to Join the Company II
```sql
```
### 2118. Build the Equation
```sql
```
### 2153. The Number of Passengers in Each Bus II
```sql
```
### 2173. Longest Winning Streak
```sql
```
### 2199. Finding the Topic of Each Post
```sql
```
### 2252. Dynamic Pivoting of a Table
```sql
```
### 2253. Dynamic Unpivoting of a Table
```sql
```
### 2362. Generate the Invoice
```sql
```
### 2474. Customers With Strictly Increasing Purchases
```sql
```
### 2494. Merge Overlapping Events in the Same Hall
```sql
```
### 262. Trips and Users
```sql
```
### 2701. Consecutive Transactions with Increasing Amounts
```sql
```
### 2720. Popularity Percentage
```sql
```
### 2752. Customers with Maximum Number of Transactions on Consecutive Days
```sql
```
### 2793. Status of Flight Tickets
```sql
```
### 2991. Top Three Wineries
```sql
```
### 2994. Friday Purchases II
```sql
```
### 2995. Viewers Turned Streamers
```sql
```
### 3052. Maximize Items
```sql
```
### 3057. Employees Project Allocation
```sql
```
### 3060. User Activities within Time Bounds
```sql
```
### 3061. Calculate Trapping Rain Water
```sql
```
### 3103. Find Trending Hashtags II
```sql
```
### 3156. Employee Task Duration and Concurrent Tasks
```sql
```
### 3188. Find Top Scoring Students II
```sql
```
### 3214. Year on Year Growth Rate
```sql
```
### 3236. CEO Subordinate Hierarchy
```sql
```
### 3268. Find Overlapping Shifts II
```sql
```
### 3368. First Letter Capitalization
```sql
```
### 3374. First Letter Capitalization II
```sql
```
### 3384. Team Dominance by Pass Success
```sql
```
### 3390. Longest Team Pass Streak
```sql
```
### 3401. Find Circular Gift Exchange Chains
```sql
```
### 3451. Find Invalid IP Addresses
```sql
```
### 3482. Analyze Organization Hierarchy
```sql
```
### 3554. Find Category Recommendation Pairs
```sql
```
### 3617. Find Students with Study Spiral Pattern
```sql
```
### 569. Median Employee Salary
```sql
```
### 571. Find Median Given Frequency of Numbers
```sql
```
### 579. Find Cumulative Salary of an Employee
```sql
```
### 601. Human Traffic of Stadium
```sql
```
### 615. Average Salary: Departments VS Company
```sql
```
### 618. Students Report By Geography
```sql
```
