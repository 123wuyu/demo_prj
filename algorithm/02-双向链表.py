


# 双向链表的结构特征
# 节点特征： 三个域：数据，向前引用，向后引用
# 头节点的向前引用为空，尾节点的向后引用为空



class Node(object):
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DLinkList(object):
    def __init__(self):
        self.__head = None

    # is_empty() 链表是否为空
    def is_empty(self):
        return not self.__head

    # add(item) 链表头部添加元素
    def add(self, data):
        node = Node(data)
        if s.is_empty():
            self.__head = node
            return

        node.next = self.__head
        self.__head.prev = node
        self.__head = node

    # show() 遍历整个链表
    def show(self):
        cur = self.__head

        while cur != None:
            # cur是一个有效节点
            print(cur.data, end=' --> ')
            cur = cur.next
        print()

    # append(item) 链表尾部添加元素
    def append(self, data):
        if self.is_empty():
            self.add(data)
            return

        cur = self.__head

        # 当cur指向的不是尾部节点的时候，就偏移
        # cur指向尾部节点的特征是： cur.next == None
        while cur.next != None:
            cur = cur.next

        # cur指向的就是尾部节点
        node = Node(data)
        cur.next = node
        node.prev = cur


    # length() 链表长度
    def length(self):
        cur = self.__head
        count = 0
        while cur != None:
            # cur是一个有效节点
            count += 1
            cur = cur.next

        return count

    # search(item) 查找节点是否存在
    def search(self, data):
        cur = self.__head
        while cur != None:
            # cur是一个有效节点
            if cur.data == data:
                return True
            cur = cur.next

        return False


    # remove(item) 删除节点
    def remove(self, data):
        cur = self.__head
        while cur != None:

            if cur.data == data:
                # 就是要删除的节点

                # 头部特殊处理
                if cur == self.__head:
                    self.__head = self.__head.next
                    # 将新的头节点的prev指向空，保证双向链表的结构特征不变
                    if self.__head:
                        self.__head.prev = None
                    return

                # 尾部特殊处理
                if cur.next == None:
                    cur.prev.next = cur.next
                    return

                cur.next.prev = cur.prev
                cur.prev.next = cur.next

            cur = cur.next


    # insert(index, data) 指定位置添加元素
    def insert(self, index, data):
        if index <= 0:
            self.add(data)
            return

        if index > self.length() - 1:
            self.append(data)
            return

        cur = self.__head
        for i in range(index-1):
            cur = cur.next

        # cur指向的就是index-1个
        node = Node(data)
        node.next = cur.next
        node.prev = cur
        cur.next.prev = node
        cur.next = node



if __name__ == "__main__":
    s = DLinkList()

    print("is_empty: ", s.is_empty())

    s.add(1)
    s.add(2)
    s.add(3)

    s.show()

    s.append(999)
    s.show()

    print("length: ", s.length())
    print("search: ", s.search(78))

    s.remove(3)
    s.show()

    s.insert(99999, 888)
    s.show()