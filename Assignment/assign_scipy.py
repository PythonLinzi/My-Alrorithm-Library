import numpy as np
from scipy.optimize import linear_sum_assignment


def assign(matrix: np.ndarray):
	'''lowest cost assignment'''
	row_idx, col_idx = linear_sum_assignment(matrix)
	ans = matrix[row_idx, col_idx].sum()
	idx = []
	for i, row in enumerate(row_idx):
		col = col_idx[i]
		v = matrix[row][col]
		print('(%d, %d) -> %d' % (row + 1, col + 1, v))
	print('Maximal Profit = %d' % ans)
	return idx, ans


def assign_max(matrix: np.ndarray):
	'''highest profit assignment'''
	inf, sum, tmp = 0x3f3f3f3f, 0, []
	for row in matrix:
		tmp_r = []
		for col in row:
			tmp_r.append(inf - col)
		tmp.append(tmp_r)
	row_idx, col_idx = linear_sum_assignment(tmp)
	for i, row in enumerate(row_idx):
		col = col_idx[i]
		v = matrix[row][col]
		sum += v
		print('(%d, %d) -> %d' % (row + 1, col + 1, v))
	print('Maximal Profit = %d' % sum)
	return sum


if __name__ == '__main__':
	cost = [[5, 9, 1], [10, 3, 2], [8, 7, 4]]
	cost = np.array(cost)
	assign(cost)
	assign_max(cost)
