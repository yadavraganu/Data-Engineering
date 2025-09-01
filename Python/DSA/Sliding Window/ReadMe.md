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
```python
from typing import Dict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Return the smallest substring of s that contains all characters in t.
        If no such window exists, return an empty string.
        """
        if not t or not s:
            return ""
        
        # Build frequency map for characters in t
        need: Dict[str, int] = {}
        for ch in t:
            need[ch] = need.get(ch, 0) + 1
        
        window: Dict[str, int] = {}
        have, required = 0, len(need)  # have: how many chars currently satisfied
        
        # (start_index, window_length)
        best_start, best_len = 0, float("inf")
        left = 0
        
        # Expand the window by moving right
        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1
            
            # If this char count now meets the requirement, increment have
            if ch in need and window[ch] == need[ch]:
                have += 1
            
            # When all required chars are satisfied, try to shrink from left
            while have == required:
                curr_len = right - left + 1
                if curr_len < best_len:
                    best_start, best_len = left, curr_len
                
                # Remove the leftmost char and adjust have if it falls below need
                left_char = s[left]
                window[left_char] -= 1
                if left_char in need and window[left_char] < need[left_char]:
                    have -= 1
                left += 1
        
        # Return the best window found (or "" if none)
        return s[best_start : best_start + best_len] if best_len != float("inf") else ""
```
# 9. Sliding Window Maximum   
