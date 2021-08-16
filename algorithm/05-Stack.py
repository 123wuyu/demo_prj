



# push(item) 添加一个新的元素item到栈顶
# pop() 弹出栈顶元素
# peek() 返回栈顶元素
# is_empty() 判断栈是否为空
# size() 返回栈的元素个数


class Stack(object):
    def __init__(self):
        self.__item = []



    # push(item) 添加一个新的元素item到栈顶
    def push(self, data):
        self.__item.append(data)

    # pop() 弹出栈顶元素
    def pop(self):
        return self.__item.pop()

    # peek() 返回栈顶元素
    def peek(self):
        return self.__item[len(self.__item)-1]

    # is_empty() 判断栈是否为空
    def is_empty(self):
        return not self.size()

    # size() 返回栈的元素个数
    def size(self):
        return len(self.__item)


if __name__ == "__main__":
    s = Stack()

    s.push(1)
    s.push(2)
    s.push(3)

    print(s.pop())
    print(s.pop())
    print(s.pop())

    print(s.is_empty())
    print(s.size())