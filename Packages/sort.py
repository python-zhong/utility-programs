def ssort(*data) -> list:  # 选择排序 [不稳定]
    data = list(data)
    n = 0
    while n < len(data):
        mi = min(data[n:])
        ind = n+data[n:].index(mi)
        data[n], data[ind] = data[ind], data[n]
        n += 1
    return data
def bsort(*data) -> list:  # 冒泡排序 [稳定]
    data = list(data)
    while True:
        flag = True
        for i in range(len(data) - 1):
            if data[i] > data[i+1]:
                data[i], data[i+1] = data[i+1], data[i]
                flag = False
        if flag:
            break
    return data
def isort(*data) -> list:  # 插入排序 [稳定]
    data = list(data)
    n = 1
    while n < len(data):
        for i in range(n):
            if data[i] > data[n]:
                data.insert(i, data.pop(n))
                break
        else:
            data.insert(i+1, data.pop(n))
        n += 1
    return data
def qsort(*data) -> list:  # 快速排序 [不稳定]
    def _internal(data, l, r):
        mid = data[(l+r)//2]
        i, j = l, r
        def do():
            nonlocal i, j
            while data[i] < mid:
                i += 1
            while data[j] > mid:
                j -= 1
            if i <= j:
                data[i], data[j] = data[j], data[i]
                i += 1
                j -= 1
        while True:
            do()
            if not (i <= j):
                break
        if l < j:
            data = _internal(data, l, j)
        if i < r:
            data = _internal(data, i, r)
        return data
    return _internal(list(data), 0, len(data) - 1)
