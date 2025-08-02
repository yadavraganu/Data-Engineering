from binary_search_tree import BstNode, add_node, levelOrderTraversal
from collections import deque


def topView(root):
    dq = deque([(root, 0)])
    map = {0: root.val}
    while dq:
        curr_node, hd = dq.popleft()
        if hd not in map:
            map[hd] = curr_node.val
        if curr_node.left:
            dq.append((curr_node.left, hd - 1))
        if curr_node.right:
            dq.append((curr_node.right, hd + 1))
    return [map[key] for key in sorted(map)]


if __name__ == "__main__":
    root = BstNode(50)
    add_node(root, 30)
    add_node(root, 20)
    add_node(root, 40)
    add_node(root, 70)
    add_node(root, 60)
    add_node(root, 80)
    print("#" * 10)
    levelOrderTraversal(root)
    print(topView(root))
