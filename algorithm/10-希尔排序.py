
l = [54, 26, 17, 31,     44, 55, 20, 99]


def shell_sort(alist):
    n = len(alist)

    gap = n//2


    # 当划分间隙等于0的时候退出循环，gap为1的时候就是最后一个分成1个列表的普通的插入排序
    while gap>0:

        # 分别对每个子表进行插入排序

        # 确定抽牌的下标取值范围
        for i in range(gap, n):
            # 抽取的第i张牌

            # 确定相邻比较对象的前置比较对象的下标取值范围
            for j in range(i, 0, 0-gap):
                # j和j-gap进行比较
                if alist[j] < alist[j-gap]:
                    alist[j],alist[j-gap] = alist[j-gap],alist[j]
                else:
                    break


        gap = gap//2


shell_sort(l)
print(l)