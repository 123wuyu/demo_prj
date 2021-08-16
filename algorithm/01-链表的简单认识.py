





class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None



if __name__ == "__main__":
    node1 = Node(1)

    node2 = Node(2)

    node3 = Node(3)


    node1.next = node2
    node2.next = node3


    head = node1


    print(head.data)
    print(head.next.data)
    print(head.next.next.data)






