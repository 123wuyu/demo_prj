

# 单向链表结构特征
# 节点：有两个域：数据域，引用域
# 尾部节点的引用域指向空
# 每个节点只有一个向后的引用


class Node(object):
    def __init__(self, data):
        # 数据域
        self.data = data
        # 引用域
        self.next = None

class SingleLinkList(object):
    def __init__(self):
        self.__head = None
        # self.length = 0

    # is_empty() 链表是否为空
    def is_empty(self):
        # return not self.__head
        if self.__head == None:
            return True
        else:
            return False

    # add(data) 链表头部添加元素
    # O(1)
    def add(self, data):
        node = Node(data)

        node.next = self.__head
        self.__head = node

        # self.length += 1

    # show() 遍历整个链表
    def show(self):
        cur = self.__head

        while cur != None:
            # if cur == None:
            #     break
            # 当cur指向当不为空，说明年该节点是有效节点
            print(cur.data, end=" --> ")
            cur = cur.next

        print()


    # append(data) 链表尾部添加元素
    def append(self, data):
        cur = self.__head

        if s.is_empty():
            s.add(data)
            # self.length += 1
            return

        # 当cur不是尾部节点的时候，我就偏移（cur = cur.next）
        while cur.next != None:
            cur = cur.next

        # cur指向的就是尾部节点
        node = Node(data)
        cur.next = node
        # self.length += 1

    # length() 链表长度
    def length(self):
        cur = self.__head
        count = 0

        while cur != None:
            # cur是一个有效的节点
            count += 1
            cur = cur.next

        return count

    # search(data) 查找节点是否存在
    def search(self, data):
        cur = self.__head

        while cur != None:
            # cur是一个有效的节点
            if cur.data == data:
                return True

            cur = cur.next

        return False



    # remove(data) 删除节点
    def remove(self, data):
        cur = self.__head
        pre = None

        while cur != None:
            if cur.data == data:
                # cur当前节点就是我们要删除的节点
                if cur == self.__head:
                    # 当前要删除的节点正好是头节点
                    self.__head = self.__head.next
                    return

                pre.next = cur.next
                return

            # pre指向的就是cur的前置节点
            pre = cur
            cur = cur.next


    # insert(index, data) 指定位置添加元素
    def insert(self, index, data):
        # index <= 0
        # 插入头部
        if index <= 0:
            s.add(data)
            return

        # index > s.length()-1
        # 插入尾部
        if index > s.length() - 1:
            s.append(data)
            return

        cur = self.__head

        for i in range(index-1):
            cur = cur.next

        # cur指向的就是第index-1个节点
        node = Node(data)
        node.next = cur.next
        cur.next = node





if __name__ == "__main__":
    s = SingleLinkList()

    print("is empty: ", s.is_empty())

    # s.add(1)
    # s.add(2)
    # s.add(3)

    s.show()

    # s.append(10)

    s.show()

    print("length: ", s.length())

    print("search: ", s.search(11))

    # s.remove(2)
    # s.remove(3)
    # s.remove(10)
    # s.show()

    s.insert(2, 999)
    # s.insert(1, 888)
    s.show()

    # s.insert(-9, 777)
    # s.insert(99999, 666)
    # s.show()



