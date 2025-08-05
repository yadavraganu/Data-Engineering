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
```python
def countBits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans
```
### Add Binary
```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        res = []
        carry = 0

        i, j = len(a) - 1, len(b) - 1
        while i >= 0 or j >= 0 or carry > 0:
            digitA = int(a[i]) if i >= 0 else 0
            digitB = int(b[j]) if j >= 0 else 0

            total = digitA + digitB + carry
            res.append(total % 2)
            carry = total // 2

            i -= 1
            j -= 1

        res.reverse()
        return ''.join(map(str, res))
```
### Reverse Bits
```python
def reverseBits(n: int) -> int:
    # Initialize result to 0. This will store the reversed bits.
    result = 0

    # Loop through all 32 bits of the input number
    for _ in range(32):
        # Shift result to the left by 1 bit to make space for the next bit
        result <<= 1

        # Add the last bit of n to result using bitwise OR
        result |= n & 1

        # Shift n to the right by 1 bit to process the next bit in the next iteration
        n >>= 1

    # Return the final reversed result
    return result
```
### Missing Number
### Sum of Two Integers
### Reverse Integer
### Bitwise AND of Numbers Range	
### Minimum Array End
