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
```
## Combination Sum II
```python
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
