
# enqueue(item) 往队列中添加一个item元素
# dequeue() 从队列头部删除一个元素
# is_empty() 判断一个队列是否为空
# size() 返回队列的大小


class Queue(object):
    def __init__(self):
        self.__item = []

    # enqueue(item) 往队列中添加一个item元素
    def enqueue(self, data):
        self.__item.append(data)

    def enqueue2(self, data):
        self.__item.insert(0, data)


    # dequeue() 从队列头部删除一个元素
    def dequeue(self):
        return self.__item.pop(0)

    def dequeue2(self):
        return self.__item.pop()

    # is_empty() 判断一个队列是否为空
    def is_empty(self):
        return not self.size()

    # size() 返回队列的大小
    def size(self):
        return len(self.__item)



if __name__ == "__main__":
    q = Queue()

    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)



    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())

    print(q.is_empty())
    print(q.size())