class BstNode:
    def __init__(self, val):
        self.val = val
        self.right = None
        self.left = None


def add_node(root_node, val):
    if root_node is None:
        return BstNode(val)
    if val <= root_node.val:
        root_node.left = add_node(root_node.left, val)
    if val > root_node.val:
        root_node.right = add_node(root_node.right, val)
    return root_node


def levelOrderTraversal(root):
    if root is None:
        return 'Tree does not exist'
    queue = [root]
    while queue:
        current_node = queue.pop(0)
        print(current_node.val)
        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)


def pre_order_traversal(root_node):
    if root_node is None:
        return
    print(root_node.val)
    pre_order_traversal(root_node.left)
    pre_order_traversal(root_node.right)


def post_order_traversal(root_node):
    if root_node is None:
        return
    pre_order_traversal(root_node.left)
    pre_order_traversal(root_node.right)
    print(root_node.val)


def in_order_traversal(root_node):
    if root_node is None:
        return
    pre_order_traversal(root_node.left)
    print(root_node.val)
    pre_order_traversal(root_node.right)


def delete_node(root_node, value):
    if root_node is None:
        return root_node
    if value > root_node.val:
        root_node.right = delete_node(root_node.right, value)
    elif value < root_node.val:
        root_node.left = delete_node(root_node.left, value)
    else:
        if root_node.left is None and root_node.right is not None:
            return root_node.right
        elif root_node.right is None and root_node.left is not None:
            return root_node.left
        elif root_node.right is None and root_node.left is None:
            return None
        else:
            temp = root_node.right
            while temp.left:
                temp = temp.left
            root_node.val = temp.val
            root_node.right = delete_node(root_node.right, temp.val)
    return root_node


def delete_bst(root_node):
    root_node.val = None
    root_node.left = None
    root_node.right = None


if __name__ == '__main__':
    root = BstNode(50)
    add_node(root, 30)
    add_node(root, 20)
    add_node(root, 40)
    add_node(root, 70)
    add_node(root, 60)
    add_node(root, 80)
    print('#' * 10)
    pre_order_traversal(root)
    print('#' * 10)
    root = delete_node(root, 50)
    print('#' * 10)
    levelOrderTraversal(root)
    print('#' * 10)
