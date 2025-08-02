class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None


class BinaryTree:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def addNode(self, root, data):
        if root is None:
            return 'Tree does not exist'
        queue = [root]
        while queue:
            current_node = queue.pop(0)
            if current_node.left is None:
                current_node.left = Node(data)
                return f'Node {data} inserted'
            else:
                queue.append(current_node.left)
            if current_node.right is None:
                current_node.right = Node(data)
                return f'Node {data} inserted'
            else:
                queue.append(current_node.right)

    def preOrderTraversal(self, root):
        if root is None:
            return
        print(root.data)
        self.preOrderTraversal(root.left)
        self.preOrderTraversal(root.right)

    def postOrderTraversal(self, root):
        if root is None:
            return
        self.postOrderTraversal(root.left)
        self.postOrderTraversal(root.right)
        print(root.data)

    def inOrderTraversal(self, root):
        if root is None:
            return
        self.inOrderTraversal(root.left)
        print(root.data)
        self.inOrderTraversal(root.right)

    def levelOrderTraversal(self, root):
        if root is None:
            return 'Tree does not exist'
        queue = [root]
        while queue:
            current_node = queue.pop(0)
            print(current_node.data)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

    def search(self, root, data):
        if root is None:
            return 'Tree does not exist'
        queue = [root]
        while queue:
            current_node = queue.pop(0)
            if current_node.data == data:
                return 'Node found'
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return 'Node not found'

    def getDeepestNode(self, root):
        dpn = None
        if root is None:
            return 'Tree does not exist'
        queue = [root]
        while queue:
            current_node = queue.pop(0)
            dpn = current_node
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return dpn

    def delDeepestNode(self, root, deepestNode):
        if root is None:
            return
        queue = [root]
        while queue:
            current_node = queue.pop(0)
            if current_node == deepestNode:
                current_node.data = None
                return f'Deepest node {deepestNode.data} deleted'
            if current_node.left:
                if current_node.left == deepestNode:
                    current_node.left = None
                    return f'Deepest node {deepestNode.data} deleted'
                else:
                    queue.append(current_node.left)
            if current_node.right:
                if current_node.right == deepestNode:
                    current_node.right = None
                    return f'Deepest node {deepestNode.data} deleted'
                else:
                    queue.append(current_node.right)
        return 'Node not found'

    def delete(self, root, data):
        if root is None:
            return
        queue = [root]
        while queue:
            current_node = queue.pop(0)
            if current_node.data == data:
                dpn = self.getDeepestNode(root)
                current_node.data = dpn.data
                self.delDeepestNode(root, dpn)
                return f'Node {data} deleted'
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return 'Node not found'

    def deleteTree(self, root):
        root.data = None
        root.left = None
        root.right = None
        return 'Tree deleted'


if __name__ == '__main__':
    bt = BinaryTree(1)
    print(f"{'#' * 20}InsertData{'#' * 20}")
    print(bt.addNode(bt, 2))
    print(bt.addNode(bt, 3))
    print(bt.addNode(bt, 4))
    print(f"{'#' * 20}PreOrderTraversal{'#' * 20}")
    bt.preOrderTraversal(bt)
    print(f"{'#' * 20}InOrderTraversal{'#' * 20}")
    bt.inOrderTraversal(bt)
    print(f"{'#' * 20}PostOrderTraversal{'#' * 20}")
    bt.postOrderTraversal(bt)
    print(f"{'#' * 20}LevelOrderTraversal{'#' * 20}")
    bt.levelOrderTraversal(bt)
    print(f"{'#' * 20}Search{'#' * 20}")
    print(bt.search(bt, 2))
    print(f"{'#' * 20}FindDeepestNode{'#' * 20}")
    print(bt.getDeepestNode(bt).data)
    print(f"{'#' * 20}DeleteDeepestNode{'#' * 20}")
    #print(bt.delDeepestNode(bt.root, bt.deepestNode(bt.root)))
    print(f"{'#' * 20}Delete{'#' * 20}")
    print(bt.delete(bt, 2))
    #print(bt.deleteTree(bt))
    #bt.preOrderTraver
    # sal(bt.root)
