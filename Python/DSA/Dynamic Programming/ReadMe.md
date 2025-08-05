## 1-D
### Climbing Stairs
```python
# Recursive
def climbStairs(n):
    if n <= 1:
        return 1
    return climbStairs(n - 1) + climbStairs(n - 2)

# Top Down Memoization
def climbStairs(n, memo={}):
    if n <= 1:
        return 1
    if n not in memo:
        memo[n] = climbStairs(n - 1, memo) + climbStairs(n - 2, memo)
    return memo[n]

# Bottom Up Tabulation
def climbStairs(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Space Optimized
def climbStairs(n):
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```
### Min Cost Climbing Stairs
```python
# Recursive
def minCost(cost, i):
    if i >= len(cost):
        return 0
    return cost[i] + min(minCost(cost, i + 1), minCost(cost, i + 2))

def minCostClimbingStairs(cost):
    return min(minCost(cost, 0), minCost(cost, 1))

# Top Down Memoization
def minCost(cost, i, memo):
    if i >= len(cost):
        return 0
    if i not in memo:
        memo[i] = cost[i] + min(minCost(cost, i + 1, memo), minCost(cost, i + 2, memo))
    return memo[i]

def minCostClimbingStairs(cost):
    memo = {}
    return min(minCost(cost, 0, memo), minCost(cost, 1, memo))

# Bottom Up Tabulation
def minCostClimbingStairs(cost):
    n = len(cost)
    dp = [0] * n
    dp[0], dp[1] = cost[0], cost[1]
    
    for i in range(2, n):
        dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])
    
    return min(dp[n - 1], dp[n - 2])

# Space Optimized
def minCostClimbingStairs(cost):
    a, b = cost[0], cost[1]
    for i in range(2, len(cost)):
        a, b = b, cost[i] + min(a, b)
    return min(a, b)
```
### N-th Tribonacci Number
### House Robber
### House Robber II
### Longest Palindromic Substring
### Palindromic Substrings
### Decode Ways
### Coin Change
### Maximum Product Subarray
### Word Break
### Longest Increasing Subsequence
### Partition Equal Subset Sum
### Combination Sum IV
### Perfect Squares
### Integer Break
### Stone Game III
