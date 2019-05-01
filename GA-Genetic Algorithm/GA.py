"""遗传算法实现求函数极大值"""
#from numba import jit
import numpy as np
import matplotlib.pyplot as plt


class GA():
    '''genetic algorithm'''
    def __init__(self,target_function,pop_size,cross_rate,mutate_rate,generation_n,x_bound,precision):
        self.f=target_function
        self.size=pop_size
        self.cross_rate=cross_rate
        self.mutate_rate=mutate_rate
        self.generations_n=generation_n
        self.x_bound=x_bound
        self.precision=precision
        self.DNA_length=int(np.log2((x_bound[1]-x_bound[0])/precision))+1
        self.DNA_length=10
        self.pop=np.random.randint(0,2,size=(self.size,self.DNA_length))

    def fitness(self,y): return y-np.min(y)+1e-3  #find non-zero fitness for selection

    def binary_to_decimal(self,pop):
        '''convert binary DNA to decimal and normalize it to a range(xbound)'''
        return pop.dot(2**np.arange(self.DNA_length)[::-1])/float(2**self.DNA_length)*self.x_bound[1]

    def select(self,fitness):
        '''nature selection wrt pop's fitness'''
        index=np.random.choice(np.arange(self.size),size=self.size,p=fitness/fitness.sum())
        return self.pop[index]

    def cross(self,parent,pop):
        ''' mating process (genes crossover)'''
        if np.random.rand()<self.cross_rate:
            idx=np.random.randint(0,self.size,size=1)
            cross_points=np.random.randint(0,2,size=self.DNA_length).astype(np.bool)
            parent[cross_points]=pop[idx,cross_points]
        return parent

    def mutate(self,child):
        for point in range(0,self.DNA_length):
            if np.random.rand()<self.mutate_rate:
                child[point]=1 if child[point]==0 else 0
        return child

if __name__=='__main__':
    def f(x): return np.sin(10 * x) * x + np.cos(2 * x) * x  # to find the maximum of this function

    plt.ion()
    ga=GA(f,100,0.8,0.003,200,[0,5],1e-3)
    x = np.linspace(*ga.x_bound, 200)
    ans=np.array([]) #
    for _ in range(ga.generations_n):
        f_values = f(ga.binary_to_decimal(ga.pop))

        if 'sca' in globals(): sca.remove()
        plt.plot(x, f(x),color='c')
        sca = plt.scatter(ga.binary_to_decimal(ga.pop), f_values, s=100, lw=0, c='blue', alpha=0.5);
        plt.pause(0.05)

        fit = ga.fitness(f_values)
        print('Best DNA: ', ga.pop[np.argmax(fit), :])
        ans=np.append(ans,ga.pop[np.argmax(fit),:]) #record answer
        ga.pop = ga.select(fit)
        pop_copy = ga.pop.copy()
        for parent in ga.pop:
            child = ga.cross(parent, pop_copy)
            child = ga.mutate(child)
            parent = child
    #record best answer
    ans_size=ans.size
    ans=ans.reshape(int(ans_size/ga.DNA_length),ga.DNA_length)
    ans_decimal=ga.binary_to_decimal(ans)
    y_ans=f(ans_decimal)
    re=ans_decimal[np.argmax(y_ans)]
    print()
    plt.plot(x, f(x))
    plt.plot(re,f(re),'*r')

    plt.ioff()
    plt.show()