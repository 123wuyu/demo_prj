l = [54, 26, 17, 31, 44, 55, 20]


def choose_sort(alist):
    n = len(alist)

    # 确认对第i个元素进行选择，i的下标取值范围
    for i in range(n-1):
        # i: 对第i个元素进行选择，选择相对最小的元素放放在第i位
        min_index = i

        for j in range(i+1, n):
            # 将第i个和第j个元素比较，取相对小对值交换
            # if alist[i] < alist[j]:
            #     alist[i], alist[j] = alist[j], alist[i]
            if alist[min_index] > alist[j]:
                min_index = j

        # min_index记录对就是本次选择中，相对最小的元素的下标
        alist[min_index], alist[i] = alist[i], alist[min_index]


choose_sort(l)
print(l)