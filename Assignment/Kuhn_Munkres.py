from munkres import Munkres, print_matrix


def KuhnMunkres(matrix):
    '''lowest cost assignment'''
    print_matrix(matrix)
    m = Munkres()
    idx = m.compute(matrix)
    sum = 0
    for row, col in idx:
        v = matrix[row][col]
        sum += v
        print('(%d, %d) -> %d' % (row + 1, col + 1, v))
    print('Minimal Cost = %d' % sum)
    return idx, sum


def KuhnMunkres_Max(matrix):
    '''highest profit assignment'''
    print_matrix(matrix)
    inf, tmp = 0x3f3f3f3f, []
    for row in matrix:
        tmp_row = []
        for col in row:
            tmp_row.append(inf - col)
        tmp.append(tmp_row)
    m, sum = Munkres(), 0
    idx = m.compute(tmp)
    for row, col in idx:
        v = matrix[row][col]
        sum += v
        print('(%d, %d) -> %d' % (row, col, v))
    print('Maximal Profit = %d' % sum)
    return idx, sum


if __name__ == '__main__':
    a = [[5, 9, 1],
         [10, 3, 2],
         [8, 7, 4]]
    KuhnMunkres(a)
    KuhnMunkres_Max(a)
