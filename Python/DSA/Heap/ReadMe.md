# Kth Largest Element in a Stream
```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```
# Last Stone Weight
```python
import heapq

class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        max_heap = [-s for s in stones]
        heapq.heapify(max_heap)

        while len(max_heap) > 1:
            y = -heapq.heappop(max_heap)
            x = -heapq.heappop(max_heap)
            if y > x:
                heapq.heappush(max_heap, -(y - x))
        
        return -max_heap[0] if max_heap else 0
```
# Kth Largest Element in an Array
```python
import heapq

class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        return heapq.nlargest(k, nums)[k-1]
```
# K Closest Points to Origin
```python
import heapq
import math

class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        min_heap = []
        for x, y in points:
            dist = math.sqrt(x**2 + y**2)
            heapq.heappush(min_heap, (dist, [x, y]))
        
        result = []
        for _ in range(k):
            result.append(heapq.heappop(min_heap)[1])
        return result
```
# High Five
```python
import heapq

class Solution:
    def highFive(self, items: list[list[int]]) -> list[list[int]]:
        scores = {}
        for student_id, score in items:
            if student_id not in scores:
                scores[student_id] = []
            heapq.heappush(scores[student_id], score)
            if len(scores[student_id]) > 5:
                heapq.heappop(scores[student_id])
        
        result = []
        for student_id in sorted(scores.keys()):
            avg_score = sum(scores[student_id]) // len(scores[student_id])
            result.append([student_id, avg_score])
        return result
```
# Employee Free Time
```python
import heapq

class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule: 'list[list[Interval]]') -> 'list[Interval]':
        intervals = []
        for employee_schedule in schedule:
            for interval in employee_schedule:
                intervals.append((interval.start, interval.end))
        
        intervals.sort()
        
        merged = []
        if not intervals:
            return []

        current_start, current_end = intervals[0]
        for i in range(1, len(intervals)):
            next_start, next_end = intervals[i]
            if next_start <= current_end:
                current_end = max(current_end, next_end)
            else:
                merged.append(Interval(current_start, current_end))
                current_start = next_start
                current_end = next_end
        merged.append(Interval(current_start, current_end))

        free_time = []
        for i in range(len(merged) - 1):
            free_time.append(Interval(merged[i].end, merged[i+1].start))
        
        return free_time
```
# Sliding Window Maximum
```python
import collections

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq = collections.deque()
        result = []

        for i in range(len(nums)):
            if dq and dq[0] == i - k:
                dq.popleft()
            
            while dq and nums[dq[-1]] <= nums[i]:
                dq.pop()
            
            dq.append(i)

            if i >= k - 1:
                result.append(nums[dq[0]])
        
        return result
```
# Top K Frequent Elements
```python
import collections
import heapq

class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = collections.Counter(nums)
        min_heap = []

        for num, freq in counts.items():
            heapq.heappush(min_heap, (freq, num))
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        
        result = [item[1] for item in min_heap]
        return result
```
# Find Median from Data Stream
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []

    def addNum(self, num: int) -> None:
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)
        
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def findMedian(self) -> float:
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0
        else:
            return float(-self.max_heap[0])
```
# Merge sorted files
```python
import heapq

def merge_sorted_files(files: list[list[int]]) -> list[int]:
    min_heap = []
    
    for i, file in enumerate(files):
        if file:
            heapq.heappush(min_heap, (file[0], i, 0))
    
    result = []
    while min_heap:
        val, file_idx, element_idx = heapq.heappop(min_heap)
        result.append(val)
        
        if element_idx + 1 < len(files[file_idx]):
            heapq.heappush(min_heap, (files[file_idx][element_idx + 1], file_idx, element_idx + 1))
            
    return result
```
# Sort an increasing-decreasing array
```python
def sort_increasing_decreasing_array(arr: list[int]) -> list[int]:
    if not arr:
        return []

    subarrays = []
    start = 0
    for i in range(1, len(arr) + 1):
        if i == len(arr) or \
           (i < len(arr) and arr[i] >= arr[i-1] and (i == len(arr) - 1 or arr[i+1] < arr[i])) or \
           (i < len(arr) and arr[i] <= arr[i-1] and (i == len(arr) - 1 or arr[i+1] > arr[i])):
            
            if arr[i-1] < arr[start]:
                subarrays.append(arr[start:i][::-1])
            else:
                subarrays.append(arr[start:i])
            start = i
            
    return merge_sorted_files(subarrays)
```
# Sort an almost-sorted array
```python
import heapq

def sort_almost_sorted_array(arr: list[int], k: int) -> list[int]:
    min_heap = []
    result = []

    for i in range(len(arr)):
        heapq.heappush(min_heap, arr[i])
        if len(min_heap) > k:
            result.append(heapq.heappop(min_heap))
    
    while min_heap:
        result.append(heapq.heappop(min_heap))
        
    return result
```
# Compute the k closest stars
```python
import heapq
import math

class Star:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def distance_from_origin(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __lt__(self, other):
        return self.distance_from_origin() > other.distance_from_origin()

def compute_k_closest_stars(stars: list[Star], k: int) -> list[Star]:
    max_heap = []

    for star in stars:
        heapq.heappush(max_heap, star)
        if len(max_heap) > k:
            heapq.heappop(max_heap)
            
    return sorted(max_heap, key=lambda s: s.distance_from_origin())
```
# Compute the median of online data
```python
import heapq

def compute_median_of_online_data(data_stream):
    min_heap = []
    max_heap = []
    medians = []

    for num in data_stream:
        if not max_heap or num <= -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)
        
        if len(max_heap) > len(min_heap) + 1:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        elif len(min_heap) > len(max_heap):
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
        
        if len(max_heap) == len(min_heap):
            medians.append((-max_heap[0] + min_heap[0]) / 2.0)
        else:
            medians.append(float(-max_heap[0]))
            
    return medians
```
# Compute the k largest elements in a max-heap
```python
import heapq

def compute_k_largest_in_max_heap(max_heap_list: list[int], k: int) -> list[int]:
    result = []
    temp_max_heap = [-x for x in max_heap_list]
    heapq.heapify(temp_max_heap)

    for _ in range(k):
        if not temp_max_heap:
            break
        result.append(-heapq.heappop(temp_max_heap))
    return result
```
# Implement a stack API using a heap
```python
import heapq

class StackUsingHeap:
    def __init__(self):
        self.heap = []
        self.counter = 0

    def push(self, val: int) -> None:
        heapq.heappush(self.heap, (-self.counter, val))
        self.counter += 1

    def pop(self) -> int:
        if not self.heap:
            raise IndexError("pop from empty stack")
        return heapq.heappop(self.heap)[1]

    def top(self) -> int:
        if not self.heap:
            raise IndexError("top from empty stack")
        return self.heap[0][1]

    def is_empty(self) -> bool:
        return len(self.heap) == 0
```
