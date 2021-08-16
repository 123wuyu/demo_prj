


# 完全二叉树
# 存储数据的时候是按照从上到下，从左到右的顺序存储的： 保证是一个有序的树


class Node(object):
    """
    数据域
    左孩子的引用
    右孩子的引用
    """
    def __init__(self, data):
        self.data = data
        self.lchild = None
        self.rchild = None



class BinaryTree(object):
    def __init__(self):
        self.root = None



if __name__ == "__main__":
    b = BinaryTree()

    node1 = Node(0)
    node2 = Node(1)
    node3 = Node(2)

    b.root = node1
    node1.lchild = node2
    node1.rchild = node3

    node4 = Node(3)
    node2.lchild = node4
    node5 = Node(4)
    node2.rchild = node5

    print(b.root.data)
    print(b.root.lchild.data)
    print(b.root.rchild.data)
    print(b.root.lchild.lchild.data)
    print(b.root.lchild.rchild.data)

