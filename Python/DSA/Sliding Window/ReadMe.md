# 1. Contains Duplicate II
```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        """
        Return True if there exist two indices i, j such that
        nums[i] == nums[j] and |i - j| <= k.
        """
        window: set[int] = set()  # holds up to k+1 most recent values
        left = 0

        for right, val in enumerate(nums):
            # if window has grown beyond size k, evict the oldest element
            if right - left > k:
                window.remove(nums[left])
                left += 1

            # duplicate in window ⇒ two equal values within k indices
            if val in window:
                return True

            window.add(val)

        return False
```
# 2. Best Time to Buy And Sell Stock   	
# 3. Longest Substring Without Repeating Characters   	
# 4. Longest Repeating Character Replacement   	
# 5. Permutation In String   	
# 6. Minimum Size Subarray Sum   	
# 7. Find K Closest Elements   	
# 8. Minimum Window Substring   	
# 9. Sliding Window Maximum   
