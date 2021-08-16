

# 单向循环链表的结构特征
# 节点结构特征： 数据、向后的引用
# 尾部节点的向后引用指向头节点


class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None



class SinCycLinkedlist(object):
    def __init__(self):
        self.__head = None

    # is_empty() 链表是否为空
    def is_empty(self):
        return not self.__head

    # add(item) 链表头部添加元素
    def add(self, data):
        node = Node(data)

        if self.is_empty():
            self.__head = node
            # 保证首尾相连
            self.__head.next = self.__head
            return

        cur = self.__head

        # 当前节点不是尾部节点的时候，往后偏移
        while cur.next != self.__head:
            cur = cur.next

        # cur指向的就是尾部节点
        node.next = self.__head
        self.__head = node
        cur.next = self.__head # node


    # show() 遍历整个链表
    def show(self):
        if self.is_empty():
            return

        cur = self.__head

        # 当前节点不是尾部节点的时候，往后偏移
        while cur.next != self.__head:
            print(cur.data, end=' --> ')
            cur = cur.next

        # cur指向的就是尾部节点
        print(cur.data)

    # append(item) 链表尾部添加元素
    def append(self, data):
        node = Node(data)

        if self.is_empty():
            self.add(data)
            return

        cur = self.__head
        while cur.next != self.__head:
            cur = cur.next

        # cur就是尾部节点
        cur.next = node
        node.next = self.__head


    # length() 链表长度
    def length(self):
        if self.is_empty():
            return 0

        cur = self.__head
        count = 0
        while cur.next != self.__head:
            count += 1
            cur = cur.next

        count += 1
        return count

    # search(item) 查找节点是否存在
    def search(self, data):
        if self.is_empty():
            return False

        cur = self.__head
        while cur.next != self.__head:

            if cur.data == data:
                return True

            cur = cur.next

        if cur.data == data:
            return True


        return False

    # remove(item) 删除节点
    def remove(self, data):
        if self.is_empty():
            return

        cur = self.__head
        pre = None

        while cur.next != self.__head:

            if cur.data == data:
                # 当前节点cur就是要删除的节点
                if cur == self.__head:
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next

                    # rear指向的就是尾部节点
                    self.__head = self.__head.next
                    rear.next = self.__head
                    return

                pre.next = cur.next
                return

            pre = cur
            cur = cur.next

        # cur指向的是尾部节点
        if cur.data == data:
            # 尾部节点就是要删除的节点
            if cur == self.__head:
                self.__head = None
                return
            pre.next = cur.next # self.__head
            return



    # insert(pos, item) 指定位置添加元素
    def insert(self, index, data):
        if index <= 0:
            self.add(data)
            return
        if index > self.length() - 1:
            self.append(data)
            return

        node = Node(data)
        cur = self.__head
        for i in range(index-1):
            cur = cur.next

        # cur指向的就是index-1
        node.next = cur.next
        cur.next = node


if __name__ == "__main__":
    s = SinCycLinkedlist()
    s.add(1)
    # s.add(2)
    # s.add(3)

    # s.show()

    # s.append(999)
    # s.show()
    print("length: ", s.length())
    print("search: ", s.search(3))

    # s.insert(99999, 888)
    # s.show()

    s.remove(1)
    s.show()
