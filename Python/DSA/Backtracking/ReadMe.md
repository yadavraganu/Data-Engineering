## Subsets
```python
def subsets(nums):
    result = []
    n = len(nums)

    def backtrack(index, current_subset):
        result.append(list(current_subset))

        for i in range(index, n):
            current_subset.append(nums[i])
            backtrack(i + 1, current_subset)
            current_subset.pop()

    backtrack(0, [])
    return result
```
## Permutations
```python
def permutations(nums):
    result = []
    n = len(nums)
    used = [False] * n

    def backtrack(current_permutation):
        if len(current_permutation) == n:
            result.append(list(current_permutation))
            return

        for i in range(n):
            if not used[i]:
                used[i] = True
                current_permutation.append(nums[i])
                backtrack(current_permutation)
                current_permutation.pop()
                used[i] = False

    backtrack([])
    return result

# Example Usage:
# print(permutations([1, 2, 3]))
```
## Subsets II
```python
def subsets_with_dup(nums):
    result = []
    nums.sort()
    n = len(nums)

    def backtrack(index, current_subset):
        result.append(list(current_subset))

        for i in range(index, n):
            if i > index and nums[i] == nums[i-1]:
                continue
            current_subset.append(nums[i])
            backtrack(i + 1, current_subset)
            current_subset.pop()

    backtrack(0, [])
    return result

# Example Usage:
# print(subsets_with_dup([1, 2, 2]))
```
## Letter Combinations of a Phone Number
```python
```
## Combination Sum
```python
from typing import List

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []          # Stores all valid combinations
        subset = []       # Current combination being built

        def _helper(i: int, tgt: int) -> None:
            if tgt == 0:
                res.append(subset.copy())  # Found a valid combination
                return
            if tgt < 0 or i == len(nums):
                return  # Invalid path or end of list

            # Include current number and recurse
            subset.append(nums[i])
            _helper(i, tgt - nums[i])      # Reuse same number
            subset.pop()                   # Backtrack

            # Skip current number and move to next
            _helper(i + 1, tgt)

        _helper(0, target)                 # Start recursion
        return res
```
## Combination Sum II
```python
from typing import List


class Solution:
    def combinationSum2(self, nums: List[int], target: int) -> List[List[int]]:
        res = []          # Stores all unique combinations
        subset = []       # Current combination being built
        nums.sort()       # Sort to group duplicates together

        def _helper(i: int, tgt: int) -> None:
            if tgt == 0:
                res.append(subset.copy())  # Found a valid combination
                return
            if i >= len(nums) or tgt < 0:
                return  # Out of bounds or invalid path

            # Include current number
            subset.append(nums[i])
            _helper(i + 1, tgt - nums[i])  # Move to next index
            subset.pop()                  # Backtrack

            # Skip duplicates
            next_i = i + 1
            while next_i < len(nums) and nums[next_i] == nums[i]:
                next_i += 1

            # Exclude current number and move to next distinct value
            _helper(next_i, tgt)

        _helper(0, target)
        return res
```
## Word Search
```python
```
## Word Search II
```python
```
## Palindrome Partitioning
```python
```
## N Queens
```python
```
# Combinations
```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        nums = list(range(1,n+1))

        def _helper(idx,curr):
            
            if len(curr) == k:
                res.append(curr.copy())
                return
            if idx > n-1 :
                return
            curr.append(nums[idx])
            _helper(idx+1,curr)
            curr.pop()
            _helper(idx+1,curr)

        _helper(0,[])
        return res
```
