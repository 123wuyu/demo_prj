


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


class Queue(object):
    def __init__(self):
        self.__item = []

    def enqueue(self, data):
        self.__item.append(data)

    def dequeue(self):
        return self.__item.pop(0)

    def is_empty(self):
        return not len(self.__item)

class BinaryTree(object):
    def __init__(self):
        self.__root = None

    # add(data)： 插入一个节点，注意在插入的过程当中必须保证完全二叉树的特征
    def add(self, data):
        node = Node(data)
        if self.is_emtpy():
            self.__root = node
            return


        q = Queue()
        q.enqueue(self.__root)

        while True:
            root = q.dequeue()

            if not root.lchild:
                # 表示的是找到了一个合适的位置，并且是左孩子
                root.lchild = node
                return

            q.enqueue(root.lchild)

            if not root.rchild:
                # 表示的是找到了一个合适的位置，并且是右孩子
                root.rchild = node
                return
            q.enqueue(root.rchild)


    # show(): 广度遍历（层次遍历）二叉树
    def show(self):
        if self.is_emtpy():
            return

        q = Queue()
        q.enqueue(self.__root)

        while not q.is_empty():
            root = q.dequeue()
            print(root.data)
            if root.lchild:
                q.enqueue(root.lchild)
            if root.rchild:
                q.enqueue(root.rchild)


    def is_emtpy(self):
        return not self.__root

    # search(data): 广度遍历查找
    def search(self, data):
        if self.is_emtpy():
            return False

        q = Queue()
        q.enqueue(self.__root)

        while not q.is_empty():
            root = q.dequeue()

            if root.data == data:
                return True

            if root.lchild:
                q.enqueue(root.lchild)
            if root.rchild:
                q.enqueue(root.rchild)

        return False


    def get_root(self):
        return self.__root


    def delete(self):
        self.__root = None


def preorder(root):
    if root == None:
        return
    print(root.data)
    preorder(root.lchild)
    preorder(root.rchild)

def inorder(root):
    if root == None:
        return
    inorder(root.lchild)
    print(root.data)
    inorder(root.rchild)

def postorder(root):
    if root == None:
        return
    postorder(root.lchild)
    postorder(root.rchild)
    print(root.data)

if __name__ == "__main__":
    b = BinaryTree()

    # node1 = Node(0)
    # node2 = Node(1)
    # node3 = Node(2)
    #
    # b.root = node1
    # node1.lchild = node2
    # node1.rchild = node3
    #
    # node4 = Node(3)
    # node2.lchild = node4
    # node5 = Node(4)
    # node2.rchild = node5

    # print(b.root.data)
    # print(b.root.lchild.data)
    # print(b.root.rchild.data)
    # print(b.root.lchild.lchild.data)
    # print(b.root.lchild.rchild.data)

    for i in range(10):
        b.add(i)

    # b.show()

    # print(b.search(93))

    postorder(b.get_root())

    b.delete()