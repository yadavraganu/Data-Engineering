class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self, root):
        self.root = root

    def add_node(self, root, node):
        if root is None:
            return
        else:
            if root.value < node.value:
                if root.left is None:
                    root.left = node
                else:
                    self.add_node(root.left, node)
            elif root.value > node.value:
                if root.right is None:
                    root.right = node
                else:
                    self.add_node(root.right, node)

    def pre_order_traversal(self, root):
        if root is None:
            return
        print(root.value)
        if root.left:
            self.pre_order_traversal(root.left)
        if root.right:
            self.pre_order_traversal(root.right)


t = Tree(TreeNode(5))
t.add_node(t.root, TreeNode(10))
t.add_node(t.root, TreeNode(9))
t.add_node(t.root, TreeNode(4))
t.pre_order_traversal(t.root)
