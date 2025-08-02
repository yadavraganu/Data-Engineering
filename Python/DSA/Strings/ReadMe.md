## 1. Longest Substring Without Repeating Characters
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}
        max_length = 0
        start = 0
        for end in range(len(s)):
            if s[end] in char_index_map and char_index_map[s[end]] >= start:
                start = char_index_map[s[end]] + 1
            char_index_map[s[end]] = end
            max_length = max(max_length, end - start + 1)
        return max_length
```
## 2. Longest Repeating Character Replacement
```python
from collections import defaultdict

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        char_counts = defaultdict(int)
        max_frequency = 0
        max_length = 0
        left = 0
        for right in range(len(s)):
            char_counts[s[right]] += 1
            max_frequency = max(max_frequency, char_counts[s[right]])
            if (right - left + 1) - max_frequency > k:
                char_counts[s[left]] -= 1
                left += 1
            max_length = max(max_length, right - left + 1)
        return max_length
```
## 3. Fizz Buzz
```python
class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        answer = []
        for i in range(1, n + 1):
            divisible_by_3 = (i % 3 == 0)
            divisible_by_5 = (i % 5 == 0)
            if divisible_by_3 and divisible_by_5:
                answer.append("FizzBuzz")
            elif divisible_by_3:
                answer.append("Fizz")
            elif divisible_by_5:
                answer.append("Buzz")
            else:
                answer.append(str(i))
        return answer
```
## 4. Longest Common Prefix
```python
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""
        prefix = strs[0]
        for i in range(1, len(strs)):
            while strs[i].find(prefix) != 0:
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix
```
## 5. Minimum Window Substring
```python
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""
        target_counts = Counter(t)
        required_chars = len(target_counts)
        window_counts = {}
        formed_chars = 0
        left = 0
        min_length = float('inf')
        min_start = 0
        for right in range(len(s)):
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1
            if char in target_counts and window_counts[char] == target_counts[char]:
                formed_chars += 1
            while formed_chars == required_chars and left <= right:
                current_window_length = right - left + 1
                if current_window_length < min_length:
                    min_length = current_window_length
                    min_start = left
                char_to_remove = s[left]
                window_counts[char_to_remove] -= 1
                if char_to_remove in target_counts and window_counts[char_to_remove] < target_counts[char_to_remove]:
                    formed_chars -= 1
                left += 1
        return "" if min_length == float('inf') else s[min_start : min_start + min_length]
```
## 6. Valid Anagram
```python
from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)
```
## 7. Group Anagrams
```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        anagram_groups = defaultdict(list)
        for s in strs:
            sorted_s = "".join(sorted(s))
            anagram_groups[sorted_s].append(s)
        return list(anagram_groups.values())
```
## 8. Valid Parentheses
```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_map = {")": "(", "}": "{", "]": "["}
        for char in s:
            if char in bracket_map:
                if not stack or stack.pop() != bracket_map[char]:
                    return False
            else:
                stack.append(char)
        return not stack
```
## 9. Valid Palindrome
```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
```
## 10. Longest Palindromic Substring
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        longest_palindrome = ""
        max_length = 0
        def expand_around_center(left, right):
            nonlocal longest_palindrome, max_length
            while left >= 0 and right < len(s) and s[left] == s[right]:
                current_length = right - left + 1
                if current_length > max_length:
                    max_length = current_length
                    longest_palindrome = s[left : right + 1]
                left -= 1
                right += 1
        for i in range(len(s)):
            expand_around_center(i, i)
            expand_around_center(i, i + 1)
        return longest_palindrome if longest_palindrome else s[0]
```
## 11. Letter Combinations of a Phone Number
```python
class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        phone_map = {
            '2': "abc", '3': "def", '4': "ghi", '5': "jkl", 
            '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
        }
        result = []
        def backtrack(index, current_combination):
            if index == len(digits):
                result.append("".join(current_combination))
                return
            digit = digits[index]
            letters = phone_map[digit]
            for letter in letters:
                current_combination.append(letter)
                backtrack(index + 1, current_combination)
                current_combination.pop()
        backtrack(0, [])
        return result
```
## 12. Palindromic Substrings
```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        count = 0
        n = len(s)
        def expand_around_center(left, right):
            nonlocal count
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
        for i in range(n):
            expand_around_center(i, i)
            expand_around_center(i, i + 1)
        return count
```
## 13. Encode and Decode Strings
```python
class Solution:
    def encode(self, strs: list[str]) -> str:
        encoded_string = ""
        for s in strs:
            encoded_string += str(len(s)) + "#" + s
        return encoded_string

    def decode(self, s: str) -> list[str]:
        decoded_strs = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            start_of_string = j + 1
            end_of_string = start_of_string + length
            decoded_strs.append(s[start_of_string : end_of_string])
            i = end_of_string
        return decoded_strs
```
## 14. Palindrome Linked List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        if not head or not head.next:
            return True
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second_half_start = self.reverseList(slow)
        first_half_start = head
        while second_half_start:
            if first_half_start.val != second_half_start.val:
                return False
            first_half_start = first_half_start.next
            second_half_start = second_half_start.next
        return True

    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev
```
## 15. Text Justification
```python
class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        result = []
        n = len(words)
        i = 0
        while i < n:
            current_line = []
            current_length = 0
            j = i
            while j < n and current_length + len(words[j]) + len(current_line) <= maxWidth:
                current_line.append(words[j])
                current_length += len(words[j])
                j += 1
            num_words_on_line = len(current_line)
            total_spaces_needed = maxWidth - current_length
            if num_words_on_line == 1 or j == n:
                line = " ".join(current_line)
                line += " " * (maxWidth - len(line))
            else:
                num_gaps = num_words_on_line - 1
                base_spaces_per_gap = total_spaces_needed // num_gaps
                extra_spaces = total_spaces_needed % num_gaps
                line = ""
                for k in range(num_words_on_line):
                    line += current_line[k]
                    if k < num_gaps:
                        line += " " * base_spaces_per_gap
                        if extra_spaces > 0:
                            line += " "
                            extra_spaces -= 1
            result.append(line)
            i = j
        return result
```
