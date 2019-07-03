from scipy.optimize import lsq_linear

''' Solve a linear least-squares problem with bounds on the variables '''
''' min 0.5 * ||A x - b||**2  subject to lb <= x <= ub '''
A = [[0.0372, 0.2869], [0.6861, 0.7071], [0.6233, 0.6245], [0.6344, 0.6170]]
B = [0.8587, 0.1781, 0.0747, 0.8405]

res = lsq_linear(A=A, b=B, bounds=(0, 10), method='trf', max_iter=100)
print(res)


'''
Parameters: (Refer to API for more parameters)
    A: [array_like, sparse matrix of LinearOperator, shape (m, n)] Design matrix. Can be scipy.sparse.linalg.LinearOperator.
    b: [array_like, shape (m,)] Target vector.
    bounds: [2-tuple of array_like, optional] Lower and upper bounds on independent variables. 
            Defaults to no bounds. Each array must have shape (n,) or be a scalar, 
            in the latter case a bound will be the same for all variables. 
            Use np.inf with an appropriate sign to disable bounds on all or some variables.
    method: [‘trf’ or ‘bvls’, optional] Method to perform minimization.
            • ‘trf’ : Trust Region Reflective algorithm adapted for a linear least-squares problem. 
            This is an interior-point-like method and the required number of iterations is weakly correlated with the number of variables.
    max_iter: [None or int, optional] Maximum number of iterations before termination. If None (default),
              it is set to 100 for method='trf' or to the number of variables for method='bvls'
              (not counting iterations for ‘bvls’ initialization).

Returns: Refer to API
'''
