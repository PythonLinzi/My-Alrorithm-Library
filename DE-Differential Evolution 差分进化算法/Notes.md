  Differential evolution is a stochastic population based method that is useful for global optimization problems. At
each pass through the population the algorithm mutates each candidate solution by mixing with other candidate
solutions to create a trial candidate. There are several strategies [2] for creating trial candidates, which suit some
problems more than others. The ‘best1bin’ strategy is a good starting point for many systems. In this strategy two
members of the population are randomly chosen. Their difference is used to mutate the best member (the best in
best1bin), b0, so far:
                    b′ = b0 + mutation ∗ (population[rand0] − population[rand1])
  A trial vector is then constructed. Starting with a randomly chosen ‘i’th parameter the trial is sequentially filled
(in modulo) with parameters from b' or the original candidate. The choice of whether to use b' or the original
candidate is made with a binomial distribution (the ‘bin’ in ‘best1bin’) - a random number in [0, 1) is generated. If
this number is less than the recombination constant then the parameter is loaded from b', otherwise it is loaded
from the original candidate. The final parameter is always loaded from b'. Once the trial candidate is built its
fitness is assessed. If the trial is better than the original candidate then it takes its place. If it is also better than the
best overall candidate it also replaces that. 
>  To improve your chances of finding a global minimum:  
>  >use higher popsizevalues, with higher mutation and (dithering), but lower recombination values.  
>  >This has the effect of widening the search radius, but slowing convergence.  
---------
>  By default the best solution vector is updated continuously within a single iteration (updating='immediate'). 
>  >This is a modification  of the original differential evolution algorithm  
>  >which can lead to faster convergence as trial vectors can immediately benefit from improved solutions.  
>  >To use the original Storn and Price behaviour, updating the best solution once per iteration, set updating='deferred'.
