### Two Sum
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    num_map = {}  # Stores value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return [] # Should not reach here based on problem constraints
```
### Best Time to Buy and Sell Stock
```python
def maxProfit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
```
### Contains Duplicate
```python
def maxProfit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
```
### Contains Duplicate II
```python
def containsNearbyDuplicate(nums: list[int], k: int) -> bool:
    num_indices = {}  # Stores value -> last_seen_index
    for i, num in enumerate(nums):
        if num in num_indices and abs(i - num_indices[num]) <= k:
            return True
        num_indices[num] = i
    return False
```
### Product of Array Except Self
```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n

    # Calculate prefix products
    prefix_product = 1
    for i in range(n):
        answer[i] = prefix_product
        prefix_product *= nums[i]

    # Calculate suffix products and multiply with prefix products
    suffix_product = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix_product
        suffix_product *= nums[i]

    return answer
```
### Maximum Subarray
```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:            
        res = nums[0]
        total = 0

        for n in nums:
            if total < 0:
                total = 0

            total += n
            res = max(res, total)
        
        return res
```
### Maximum Product Subarray
```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        curr_max = 1
        curr_min = 1
        res = float("-inf")

        for i in nums:
            temp = curr_max * i
            curr_max = max(i, temp, curr_min * i)
            curr_min = min(i, temp, curr_min * i)

            res = max(res, curr_max)
        return res
```
### Find Minimum in Rotated Sorted Array
```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        l = 0
        r = len(nums) - 1
        res = float("inf")

        while l <= r:
            mid = l + (r - l) // 2
            if nums[l] <= nums[mid]:
                res = min(res, nums[l])
                l = mid + 1
            else:
                res = min(res, nums[mid])
                r = mid - 1
        return res
```
### Search in Rotated Sorted Array
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            if nums[l] <= nums[mid]:
                if nums[l] <= target <= nums[mid]:
                    r = mid
                else:
                    l = mid + 1
            else:
                if nums[mid] <= target <= nums[r]:
                    l = mid
                else:
                    r = mid - 1
        return -1
```
### Two Sum II
```python
def two_sum(numbers, target):
    left, right = 0, len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return [left + 1, right + 1]  # 1-based indexing
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []
```
### 3 Sum
```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        i = 0
        nums.sort()
        res = []
        while i < len(nums) - 2:
            if nums[i] == nums[i - 1] and i > 0:
                i += 1
                continue
            else:
                j, k = i + 1, len(nums) - 1
                while j < k:
                    total = nums[i] + nums[j] + nums[k]
                    if total == 0:
                        res.append([nums[i], nums[j], nums[k]])
                        while j < k and nums[j] == nums[j + 1]:
                            j += 1
                        while j < k and nums[k] == nums[k - 1]:
                            k -= 1
                        j += 1
                        k -= 1
                    elif total < 0:
                        j += 1
                    else:
                        k -= 1
            i += 1
        return res
```
### Merge Sorted Array
```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        m_ind = m - 1
        n_ind = n - 1
        merge_ind = m + n - 1
        while m_ind >= 0 and n_ind >= 0:
            if nums1[m_ind] > nums2[n_ind]:
                nums1[merge_ind] = nums1[m_ind]
                m_ind -= 1
            else:
                nums1[merge_ind] = nums2[n_ind]
                n_ind -= 1
            merge_ind -= 1
        while n_ind >= 0:
            nums1[merge_ind] = nums2[n_ind]
            n_ind -= 1
            merge_ind -= 1
```
### Container With Most Water
```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        # Calculate current area
        current_water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, current_water)

        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water
```
### Verifying an Alien Dictionary
```python
import collections

def isAlienSorted(words: list[str], order: str) -> bool:
    # Step 1: Create a mapping from alien character to its numerical order
    char_order = {char: i for i, char in enumerate(order)}

    # Step 2: Define a helper function to compare two words based on the alien order
    def compare(word1: str, word2: str) -> bool:
        min_len = min(len(word1), len(word2))
        
        # Iterate through characters up to the length of the shorter word
        for i in range(min_len):
            char1_val = char_order[word1[i]] # Get numerical value of char from word1
            char2_val = char_order[word2[i]] # Get numerical value of char from word2

            if char1_val < char2_val:
                return True  # word1 comes before word2
            elif char1_val > char2_val:
                return False # word1 comes after word2

        return len(word1) <= len(word2)

    # Step 3: Iterate through adjacent pairs of words and compare them
    for i in range(len(words) - 1):
        if not compare(words[i], words[i+1]):
            return False
    return True
```
### Next Permutation
```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:

        # 1. Find the first decreasing element from the right (pivot)
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        # If such an element exists ,Find the smallest element to the right of pivot that is greater than pivot
        if i >= 0:
            for j in range(len(nums) - 1, i, -1):
                if nums[j] > nums[i]:
                    break
            # Swap the pivot with this found elemen
            nums[i], nums[j] = nums[j], nums[i]
        l = i + 1
        r = len(nums) - 1
        # Reverse the suffix starting from pivot + 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            r -= 1
            l += 1
```
### Remove Duplicates from Sorted Array
```python
def remove_duplicates(nums):
    if not nums:
        return 0

    i = 0  # Pointer for the last unique element
    for j in range(1, len(nums)):
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]

    return i + 1  # Length of array with unique elements
```
### Find First and Last Position of Element in Sorted Array
```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def binary_search_left(nums,target):
            l,r = 0,len(nums)-1
            first = -1
            while l<=r:
                mid = l + ((r-l)//2)
                if nums[mid]<target:
                    l = mid+1
                elif nums[mid]>target:
                    r = mid-1
                else:
                    r = mid-1
                    first = mid
            return first 
        def binary_search_right(nums,target):
            l,r = 0,len(nums)-1
            last = -1
            while l<=r:
                mid = l + ((r-l)//2)
                if nums[mid]<target:
                    l = mid+1
                elif nums[mid]>target:
                    r = mid-1
                else:
                    l = mid+1
                    last = mid
            return last  
        return  [binary_search_left(nums,target),binary_search_right(nums,target)]
```
### Trapping Rain Water
```python
class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        water = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += max(0, left_max - height[left])
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += max(0, right_max - height[right])

        return water
```
### Median of Two Sorted Arrays
```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        l1 = len(nums1)
        l2 = len(nums2)

        if l1 > l2:
            return self.findMedianSortedArrays(nums2, nums1)
        total_len = l1 + l2
        half_len = (total_len + 1) // 2
        l = 0
        r = l1
        print(l,r,total_len,half_len)
        while l <= r:
            part1 = (l + r) // 2
            part2 = half_len - part1

            l1_left = nums1[part1 - 1] if part1 != 0 else float("-inf")
            l2_left = nums2[part2 - 1] if part2 != 0 else float("-inf")
            l1_right = nums1[part1] if part1 != l1 else float("inf")
            l2_right = nums2[part2] if part2 != l2 else float("inf")

            if l1_left <= l2_right and l2_left <= l1_right:
                if total_len % 2 == 1:
                    return max(l1_left, l2_left)
                else:
                    return (max(l1_left, l2_left) + min(l1_right, l2_right)) / 2
            elif l1_left > l2_right:
                r = part1 - 1
            elif l1_right < l2_left:
                l = part1 + 1
        return 0.0
```
### Valid Anagram
```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        from collections import Counter

        cntr = Counter(s)
        if len(s) == len(t):
            for i in t:
                if i not in cntr or cntr[i] == 0:
                    return False
                else:
                    cntr[i] -= 1
        else:
            return False
        return True
```
### Top K Frequent Elements
```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        from collections import Counter

        cntr = Counter(nums)

        bckts = [[] for _ in range(len(nums) + 1)]

        for num, count in cntr.items():
            bckts[count].append(num)

        res = []

        for i in range(len(bckts) - 1, 0, -1):
            for num in bckts[i]:
                res.append(num)
                if len(res) == k:
                    return res
```
### Group Anagrams
```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        import collections

        # Use a defaultdict to automatically create a list if a key is new
        anagram_groups = collections.defaultdict(list)

        for word in strs:
            # Sort the word to create a canonical key for anagrams
            # Example: "eat" -> "aet", "tea" -> "aet"
            sorted_word_tuple = tuple(sorted(word))  # Use tuple for hashable key
            anagram_groups[sorted_word_tuple].append(word)

        return list(anagram_groups.values())
```
### Valid Sudoku
```python
import collections

def isValidSudoku(board: list[list[str]]) -> bool:
    rows = collections.defaultdict(set)
    cols = collections.defaultdict(set)
    boxes = collections.defaultdict(set) # Key: (row_box_index, col_box_index)

    for r in range(9):
        for c in range(9):
            char = board[r][c]
            if char == '.':
                continue

            # Check row
            if char in rows[r]:
                return False
            rows[r].add(char)

            # Check column
            if char in cols[c]:
                return False
            cols[c].add(char)

            # Check 3x3 box
            # Integer division to get box indices (0-2 for rows, 0-2 for columns)
            box_row = r // 3
            box_col = c // 3
            if char in boxes[(box_row, box_col)]:
                return False
            boxes[(box_row, box_col)].add(char)
            
    return True
```
### Encode and Decode Strings
```python
class Codec:
    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single string.
        """
        encoded_string = []
        for s in strs:
            encoded_string.append(str(len(s)) + '#' + s)
        return "".join(encoded_string)

    def decode(self, s: str) -> list[str]:
        """Decodes a single string to a list of strings.
        """
        decoded_strings = []
        i = 0
        while i < len(s):
            j = i
            # Find the '#' delimiter
            while j < len(s) and s[j] != '#':
                j += 1
            
            # Extract the length
            length_str = s[i:j]
            length = int(length_str)
            
            # Extract the string itself
            start_of_string = j + 1
            end_of_string = start_of_string + length
            decoded_strings.append(s[start_of_string:end_of_string])
            
            # Move pointer to the beginning of the next string
            i = end_of_string
            
        return decoded_strings
```
### Longest Consecutive Sequence
```python
def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0

    for num in num_set:
        # Only start counting if it's the beginning of a sequence
        if num - 1 not in num_set:
            current = num
            streak = 1

            while current + 1 in num_set:
                current += 1
                streak += 1

            longest = max(longest, streak)

    return longest
```
