
l = [54, 26, 17, 31, 44, 55, 20]


def insert_sort(alist):
    n = len(alist)

    for i in range(1, n):
        # 抽取的第i张牌

        for j in range(i, 0, -1):
            # 将j和j+1这样第相邻比较对象进行比较。大的放后，小的放前就是升序
            # 前置比较对象是j，后置比较对象j-1
            if alist[j] < alist[j-1]:
                alist[j], alist[j-1] = alist[j-1],alist[j]
            else:
                break


insert_sort(l)
print(l)