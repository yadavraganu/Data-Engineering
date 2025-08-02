## Insert Interval
```python
def insert(intervals, newInterval):
    result = []
    for i in intervals:
        # If current interval ends before newInterval starts, add it directly
        if i[1] < newInterval[0]:
            result.append(i)
        # If newInterval ends before current interval starts, insert newInterval and update it
        elif newInterval[1] < i[0]:
            result.append(newInterval)
            newInterval = i
        else:
            # Overlapping intervals, merge them
            newInterval[0] = min(newInterval[0], i[0])
            newInterval[1] = max(newInterval[1], i[1])
    result.append(newInterval)
    return result
```
## Merge Interval
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])  # Sort by start time
    merged = []
    for interval in intervals:
        # If no overlap, add interval
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # Merge overlapping intervals
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged
```
## Non Overlapping Intervals
```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])  # Sort by end time
    count = 0
    end = float('-inf')
    for i in intervals:
        # If overlapping, increment count
        if i[0] < end:
            count += 1
        else:
            end = i[1]
    return count
```
