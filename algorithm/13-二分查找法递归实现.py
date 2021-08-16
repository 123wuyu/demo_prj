

l = [0, 1, 2, 8, 13, 17, 19, 32, 42]


def binary_search(alist, data):
    n = len(alist)

    if n == 0:
        # maximum recursion depth exceeded in comparison
        return False

    mid_index = n//2
    if alist[mid_index] == data:
        return True

    if data > alist[mid_index]:
        # 要对右表进行拆分
        return binary_search(alist[mid_index+1:], data)
    else:
        # 要对左表进行拆分
        return binary_search(alist[:mid_index], data)



print(binary_search(l, -1))