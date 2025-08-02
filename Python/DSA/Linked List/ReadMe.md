# 1. Add Two Numbers
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy_head = ListNode(0)
    current = dummy_head
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        total_sum = val1 + val2 + carry
        carry = total_sum // 10
        current.next = ListNode(total_sum % 10)
        current = current.next

        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    return dummy_head.next
```
# 2. Reverse a Linked List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: ListNode) -> ListNode:
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```
# 3. Detect Cycle in a Linked List
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    return False
```
# 4. Merge Two Sorted Lists
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy_head = ListNode(0)
    current = dummy_head

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    if l1:
        current.next = l1
    elif l2:
        current.next = l2

    return dummy_head.next
```
# 5. Merge K Sorted Lists
```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: list[ListNode]) -> ListNode:
    dummy_head = ListNode(0)
    current = dummy_head
    min_heap = []

    # Push the head of each list into the min-heap
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(min_heap, (l.val, i, l)) # (value, list_index, node_object)

    while min_heap:
        val, list_index, node = heapq.heappop(min_heap)
        current.next = node
        current = current.next
        if node.next:
            heapq.heappush(min_heap, (node.next.val, list_index, node.next))

    return dummy_head.next
```
# 6. Remove Nth Node From End Of List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0, head)
    first = dummy
    second = dummy

    # Move first pointer n steps ahead
    for _ in range(n + 1):
        first = first.next

    # Move both pointers until first reaches the end
    while first:
        first = first.next
        second = second.next

    # Remove the nth node
    second.next = second.next.next

    return dummy.next
```
# 7. Reorder List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reorderList(head: ListNode) -> None:
    """
    Do not return anything, modify head in-place instead.
    """
    if not head or not head.next:
        return

    # 1. Find the middle of the list
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Split the list into two halves
    # first_half starts from head
    # second_half starts from slow (middle)
    second_half = slow.next
    slow.next = None # Break the link to separate the two halves

    # 3. Reverse the second half
    prev = None
    current = second_half
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    second_half_reversed = prev

    # 4. Merge the two halves
    first_half = head
    while second_half_reversed:
        temp1 = first_half.next
        temp2 = second_half_reversed.next

        first_half.next = second_half_reversed
        second_half_reversed.next = temp1

        first_half = temp1
        second_half_reversed = temp2
```
# 8. Middle of the Linked-List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def middleNode(head: ListNode) -> ListNode:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```
# 9. Flatten Binary Tree to Linked List
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flatten(root: TreeNode) -> None:
    """
    Do not return anything, modify root in-place instead.
    """
    if not root:
        return

    # Use a stack for iterative pre-order traversal
    stack = [root]
    prev = None

    while stack:
        current = stack.pop()

        if prev:
            prev.right = current
            prev.left = None # Set left child to None

        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)

        prev = current
```
# 10. Reverse Nodes in k-Group
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseKGroup(head: ListNode, k: int) -> ListNode:
    if not head or k == 1:
        return head

    dummy = ListNode(0, head)
    prev_group_end = dummy
    current = head

    while current:
        # Check if there are at least k nodes remaining
        count = 0
        temp = current
        while temp and count < k:
            temp = temp.next
            count += 1

        if count == k:
            # Reverse the k-group
            group_start = current
            group_prev = temp # The node after the current k-group
            for _ in range(k):
                next_node = current.next
                current.next = group_prev
                group_prev = current
                current = next_node

            # Connect the reversed group
            prev_group_end.next = group_prev
            prev_group_end = group_start # The new end of the reversed group

        else:
            # Less than k nodes remaining, leave them as they are
            prev_group_end.next = current
            break

    return dummy.next
```
