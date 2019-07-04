'''
To improve your chances of finding a global minimum:
 *use higher popsize values,
 *with higher mutation and (dithering),
 *but lower recombination values.
 This has the effect of widening the search radius, but slowing convergence.
'''

# from scipy.optimize import rosen # import Rosenbrock func as example
from scipy.optimize import differential_evolution as de

def rose(x):
    '''Rosenbrock Function'''
    return sum(100 * (x[1:] - x[:-1]) ** 2 + (x[:-1] - 1) ** 2)


bnds = [(0, 2), (0, 2), (0, 2)]
ans = de(func=rose, bounds=bnds, maxiter=1000, popsize=25,
         tol=0.01, mutation=(0.5, 1), recombination=0.7)
print(ans.x, ans.fun)
