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
```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # If s1 is longer than s2, no permutation is possible
        if len(s1) > len(s2):
            return False

        # Frequency arrays for characters 'a' to 'z'
        s1Count, s2Count = [0] * 26, [0] * 26

        # Initialize counts for s1 and the first window of s2
        for i in range(len(s1)):
            s1Count[ord(s1[i]) - ord('a')] += 1
            s2Count[ord(s2[i]) - ord('a')] += 1

        # Count how many characters match in frequency
        matches = sum(1 for i in range(26) if s1Count[i] == s2Count[i])

        # Start sliding window
        l = 0
        for r in range(len(s1), len(s2)):
            if matches == 26:
                return True  # All characters match → permutation found

            # Add new character to the window (right side)
            index = ord(s2[r]) - ord('a')
            s2Count[index] += 1

            # Update matches based on the new character
            if s1Count[index] == s2Count[index]:
                matches += 1  # New character now matches
            elif s1Count[index] + 1 == s2Count[index]:
                matches -= 1  # It was matching before, now it's over-counted

            # Remove old character from the window (left side)
            index = ord(s2[l]) - ord('a')
            s2Count[index] -= 1

            # Update matches based on the removed character
            if s1Count[index] == s2Count[index]:
                matches += 1  # After removal, it matches again
            elif s1Count[index] - 1 == s2Count[index]:
                matches -= 1  # It was matching before, now it's under-counted

            l += 1  # Move the window forward

        # Final check after loop
        return matches == 26

```
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
