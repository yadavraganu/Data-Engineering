# Binary Tree and Trie Problems Solutions
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```
# 1. Test if a Binary Tree is Height-Balanced
```python
def is_balanced(root):
    def check(node):
        if not node:
            return 0, True
        left_height, left_balanced = check(node.left)
        right_height, right_balanced = check(node.right)
        balanced = left_balanced and right_balanced and abs(left_height - right_height) <= 1
        return max(left_height, right_height) + 1, balanced
    return check(root)[1]
```
# 2. Test if a Binary Tree is Symmetric
```python
def is_symmetric(root):
    def is_mirror(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (t1.val == t2.val and 
                is_mirror(t1.left, t2.right) and 
                is_mirror(t1.right, t2.left))
    return is_mirror(root, root)
```
# 3. Compute the Lowest Common Ancestor in a Binary Tree
```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root.val == p.val or root.val == q.val:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right
```
# 4. Compute the LCA When Nodes Have Parent Pointers
```python
def lca_with_parent(p, q):
    ancestors = set()
    while p:
        ancestors.add(p)
        p = p.parent
    while q:
        if q in ancestors:
            return q
        q = q.parent
```
# 5. Sum the Root-to-Leaf Paths in a Binary Tree
```python
def sum_root_to_leaf(root):
    def dfs(node, current_sum):
        if not node:
            return 0
        current_sum = current_sum * 10 + node.val
        if not node.left and not node.right:
            return current_sum
        return dfs(node.left, current_sum) + dfs(node.right, current_sum)
    return dfs(root, 0)
```
# 6. Find a Root to Leaf Path with Specified Sum
```python
def has_path_sum(root, target_sum):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target_sum
    return (has_path_sum(root.left, target_sum - root.val) or 
            has_path_sum(root.right, target_sum - root.val))
```
# 7. Inorder Traversal Without Recursion
```python
def inorder_traversal(root):
    stack, result = [], []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result
```
# 8. Preorder Traversal Without Recursion
```python
def preorder_traversal(root):
    if not root:
        return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result
```
# 9. Compute the Kth Node in an Inorder Traversal (kth-smallest-element-in-a-bst)
```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        if not root:
            return root
        while True:
            while root:
                stack.append(root)
                root = root.left
            elem = stack.pop()
            k = k-1
            if k == 0:
                return elem.val
            root = elem.right
```
# 10. Compute the Successor
```python
def inorder_successor(node):
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        return node
    while node.parent and node == node.parent.right:
        node = node.parent
    return node.parent
```
# 11. Inorder Traversal with O(1) Space (Morris Traversal)
```python
def morris_inorder_traversal(root):
    result = []
    current = root
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            if not predecessor.right:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                result.append(current.val)
                current = current.right
    return result
```
# 12. Reconstruct Binary Tree from Preorder and Inorder
```python
def build_tree(preorder, inorder):
    inorder_index = {val: idx for idx, val in enumerate(inorder)}
    def helper(pre_start, in_start, in_end):
        if pre_start >= len(preorder) or in_start > in_end:
            return None
        root_val = preorder[pre_start]
        root = TreeNode(root_val)
        in_index = inorder_index[root_val]
        left_size = in_index - in_start
        root.left = helper(pre_start + 1, in_start, in_index - 1)
        root.right = helper(pre_start + 1 + left_size, in_index + 1, in_end)
        return root
    return helper(0, 0, len(inorder) - 1)
```
# 13. Reconstruct Binary Tree from Preorder with Markers
```python
def build_tree_with_markers(preorder):
    def helper(it):
        val = next(it)
        if val is None:
            return None
        node = TreeNode(val)
        node.left = helper(it)
        node.right = helper(it)
        return node
    return helper(iter(preorder))
```
# 14. Form a Linked List from the Leaves of a Binary Tree
```python
def leaf_linked_list(root):
    dummy = ListNode(0)
    current = dummy
    def dfs(node):
        nonlocal current
        if not node:
            return
        if not node.left and not node.right:
            current.next = ListNode(node.val)
            current = current.next
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return dummy.next
```
# 15. Compute the Exterior of a Binary Tree
```python
def exterior_binary_tree(root):
    def is_leaf(node):
        return not node.left and not node.right
    def left_boundary(node):
        boundary = []
        while node:
            if not is_leaf(node):
                boundary.append(node)
            node = node.left if node.left else node.right
        return boundary
    def right_boundary(node):
        boundary = []
        while node:
            if not is_leaf(node):
                boundary.append(node)
            node = node.right if node.right else node.left
        return boundary[::-1]
    def leaves(node):
        if not node:
            return []
        if is_leaf(node):
            return [node]
        return leaves(node.left) + leaves(node.right)
    if not root:
        return []
    return [root] + left_boundary(root.left) + leaves(root) + right_boundary(root.right)
```
# 16. Compute the Right Sibling Tree
```python
def connect_right_siblings(root):
    if not root:
        return
    queue = [root]
    while queue:
        next_level = []
        for i in range(len(queue)):
            if i + 1 < len(queue):
                queue[i].right_sibling = queue[i + 1]
            if queue[i].left:
                next_level.append(queue[i].left)
            if queue[i].right:
                next_level.append(queue[i].right)
        queue = next_level
```
# 17. Maximum Depth of Binary Tree
```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```
# 18. Same Tree
```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        elif not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left,q.left) and self.isSameTree(p.right,q.right)
```
# 20. Invert/Flip Binary Tree
```python
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```
# 21. Binary Tree Maximum Path Sum
```python
def max_path_sum(root):
    max_sum = float('-inf')
    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        max_sum = max(max_sum, node.val + left + right)
        return node.val + max(left, right)
    dfs(root)
    return max_sum
```
# 22. Binary Tree Level Order Traversal
```python
def level_order(root):
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.pop(0)
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```
# 23. Serialize and Deserialize Binary Tree
```python
def serialize(root):
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    return result

def deserialize(data):
    if not data:
        return None
    root = TreeNode(data[0])
    queue = [root]
    i = 1
    while queue:
        node = queue.pop(0)
        if i < len(data) and data[i] is not None:
            node.left = TreeNode(data[i])
            queue.append(node.left)
        i += 1
        if i < len(data) and data[i] is not None:
            node.right = TreeNode(data[i])
            queue.append(node.right)
        i += 1
    return root
```
# 24. Subtree of Another Tree
```python
def is_subtree(s, t):
    def is_same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return is_same(a.left, b.left) and is_same(a.right, b.right)
    if not s:
        return False
    if is_same(s, t):
        return True
    return is_subtree(s.left, t) or is_subtree(s.right, t)
```
# 25. Find Leaves of Binary Tree
```python
def find_leaves(root):
    result = []
    def dfs(node):
        if not node:
            return -1
        level = 1 + max(dfs(node.left), dfs(node.right))
        if level == len(result):
            result.append([])
        result[level].append(node.val)
        return level
    dfs(root)
    return result
```
# 27. Validate Binary Search Tree
```python
def is_valid_bst(root):
    def validate(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
    return validate(root, float('-inf'), float('inf'))
```
# 28. Kth Smallest Element in a BST
```python
def kth_smallest(root, k):
    stack = []
    while True:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        k -= 1
        if k == 0:
            return root.val
        root = root.right
```
# 29. Lowest Common Ancestor of BST
```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```
# 30. Binary Tree Zigzag Level Order Traversal
```python
def zigzag_level_order(root):
    if not root:
        return []
    result, queue, left_to_right = [], [root], True
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.pop(0)
            if left_to_right:
                level.append(node.val)
            else:
                level.insert(0, node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
        left_to_right = not left_to_right
    return result
```
# 31. Implement Trie (Prefix Tree)
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end
    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```
# 32. Add and Search Word
```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    def add_word(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return node.is_end
            if word[i] == '.':
                return any(dfs(child, i + 1) for child in node.children.values())
            if word[i] in node.children:
                return dfs(node.children[word[i]], i + 1)
            return False
        return dfs(self.root, 0)
```
# 33. Word Search II
```python
def find_words(board, words):
    trie = Trie()
    for word in words:
        trie.insert(word)
    result, rows, cols = set(), len(board), len(board[0])
    def dfs(r, c, node, path):
        if not (0 <= r < rows and 0 <= c < cols):
            return
        char = board[r][c]
        if char not in node.children:
            return
        node = node.children[char]
        path += char
        if node.is_end:
            result.add(path)
        board[r][c] = '#'
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            dfs(r+dr, c+dc, node, path)
        board[r][c] = char
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")
    return list(result)
```
