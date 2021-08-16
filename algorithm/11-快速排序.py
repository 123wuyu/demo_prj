



def quick_sort(alist, start, end):
    # start>=end
    if start >= end:
        return

    low = start
    high = end

    mid = alist[low]

    # 当low>=high就退出循环
    # 如果要保序：alist[high] >= mid 和 alist[low] <= mid 只取其中一种
    while low < high:
        while alist[high] >= mid and low < high:
            high -= 1
        alist[low] = alist[high]

        while alist[low] < mid and low < high:
            low += 1
        alist[high] = alist[low]

    # low == high
    alist[low] = mid

    # 以low下标为界，分为左表和右表
    # 左表：[start, low-1]
    quick_sort(alist, start, low-1)
    # 右表：[high+1, end]
    quick_sort(alist, high+1, end)


l = [54, 26, 17, 31,       44, 55, 20]

quick_sort(l, 0, len(l)-1)
print(l)