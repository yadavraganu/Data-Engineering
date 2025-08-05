### Single Number
Key Insight:
- XOR (^) of a number with itself is 0: a ^ a = 0
- XOR of a number with 0 is the number itself: a ^ 0 = a
- XOR is commutative and associative, so order doesn't matter.
```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```
### Number of 1 Bits
```python
def hamming_weight(n):
    count = 0
    while n:
        count += n & 1  # Add 1 if the last bit is 1
        n >>= 1         # Shift bits to the right
    return count
```
### Counting Bits
### Add Binary
### Reverse Bits
### Missing Number
### Sum of Two Integers
### Reverse Integer
### Bitwise AND of Numbers Range	
### Minimum Array End
