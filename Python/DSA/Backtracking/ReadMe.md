# 1. Subsets
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
# 2. Permutations
```python
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []  # Stores all the permutations
        used = [False] * len(nums)  # Tracks which elements are used in the current permutation

        def _helper(subset):
            if len(subset) == len(nums):
                res.append(subset[:])  # Add a copy of the current permutation to the result
                return

            for i in range(len(nums)):
                if not used[i]:  # Skip if the element is already used
                    used[i] = True
                    subset.append(nums[i])  # Choose the element
                    _helper(subset)         # Explore further
                    subset.pop()           # Undo the choice (backtrack)
                    used[i] = False        # Mark the element as unused again

        _helper([])
        return res
```
# 3. Subsets II
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
####################
from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()  # Sort to group duplicates together

        def _helper(idx, subset):
            if idx == len(nums):
                res.append(subset.copy())  # Add a copy of the current subset
                return

            # Include the current element
            subset.append(nums[idx])
            _helper(idx + 1, subset)
            subset.pop()  # Backtrack

            # Skip duplicates
            next_idx = idx + 1
            while next_idx < len(nums) and nums[next_idx] == nums[next_idx - 1]:
                next_idx += 1

            # Exclude the current element and move to the next distinct one
            _helper(next_idx, subset)

        _helper(0, [])
        return res
```
# 4. Letter Combinations of a Phone Number
```python
```
# 5. Combination Sum
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
# 6. Combination Sum II
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
# 7. Word Search
```python
```
# 8. Word Search II
```python
```
# 9. Palindrome Partitioning
```python
```
# 10. N Queens
```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []  # Stores all valid board configurations
        board = [["."] * n for _ in range(n)]  # Initialize empty board
        col = set()  # Tracks occupied columns
        pos_diag = set()  # Tracks occupied positive diagonals (r - c)
        neg_diag = set()  # Tracks occupied negative diagonals (r + c)

        def _helper(r):
            if r == n:
                # All queens placed successfully, add current board to result
                result.append(["".join(row) for row in board])
                return

            for c in range(n):
                # Skip if column or diagonal is under attack
                if c in col or (r + c) in neg_diag or (r - c) in pos_diag:
                    continue

                # Place queen and mark column and diagonals
                col.add(c)
                pos_diag.add(r - c)
                neg_diag.add(r + c)
                board[r][c] = 'Q'

                _helper(r + 1)  # Move to next row

                # Backtrack: remove queen and unmark threats
                board[r][c] = '.'
                col.remove(c)
                pos_diag.remove(r - c)
                neg_diag.remove(r + c)

        _helper(0)  # Start placing queens from row 0
        return result
```
# 11. Combinations
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
