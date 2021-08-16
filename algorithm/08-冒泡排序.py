
l = [54, 26, 17, 31, 44, 55, 20]


def pop_sort(alist):
    n = len(alist)

    # 确定的是要冒几次泡
    for i in range(n-1):
        # 分别冒泡： 第0，1，2，3...n-2次泡
        # 进行第i次冒泡
        count = 0

        for j in range(n-1-i):
            # j是每次冒泡的相邻比较对象的前置比较对象的下标
            # j和j+1进行比较，大的放后就是升序
            if alist[j] > alist[j+1]:
                alist[j], alist[j+1] = alist[j+1], alist[j]
                count += 1

        if count == 0:
            break


pop_sort(l)
print(l)