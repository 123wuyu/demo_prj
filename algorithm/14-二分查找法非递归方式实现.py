
l = [0, 1, 2, 8, 13, 17, 19, 32, 42]


def binary_search(alist, data):
    start = 0
    end = len(alist) - 1

    while start <= end: # start == end的时候表明拆分的只剩下一个元素的子表了，是最后一个取中间值判断
        mid_index = (start + end) // 2
        if alist[mid_index] == data:
            return True
        if alist[mid_index] < data:
            # 在右侧
            start = mid_index + 1
            # 确定了一个右表 alist[mid_index+1:end]
        else:
            # 在左侧
            end  = mid_index - 1
            # 确定了一个左表 alist[start:mid_index]

        # start换个end确定了一张表

    return False


print(binary_search(l, 43))