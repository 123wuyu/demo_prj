


# 递归
def merge_sort(alist):
    if len(alist) == 1:
        return alist

    n = len(alist)

    left_list = merge_sort(alist[:n//2])
    right_list = merge_sort(alist[n//2:])


    return merge(left_list, right_list)


# 合并
def merge(left_list, right_list):
    new_list = []

    l_index, r_index = 0, 0

    while l_index < len(left_list) and r_index < len(right_list):
        # if l_index > len(left_list)-1 or r_index > len(right_list)-1:
        #     break

        if left_list[l_index] < right_list[r_index]:
            new_list.append(left_list[l_index])
            l_index += 1
        else:
            new_list.append(right_list[r_index])
            r_index += 1


    new_list += left_list[l_index:]
    new_list += right_list[r_index:]


    return new_list


# a = [11,14,16,25,      1,10,12,15]
# print(merge(a[:4], a[4:]))

l = [54, 26, 17, 31, 44, 55, 20]

print(merge_sort(l))