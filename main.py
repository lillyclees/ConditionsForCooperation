import os
import datetime
from game import *

def make_dir():
    # log files set-up
    run = datetime.datetime.now()
    run = run.strftime("%m:%d:%Y, %H:%M:%S")
    dir_name = f"run {run}"
    os.mkdir(dir_name)
    new_dir = f"{dir_name}/episodes"
    os.mkdir(new_dir)
    return dir_name

# game parameters
N_sims = 5 # number of simulation runs / episodes
T = 500 # time steps / episode length

N = 10 # number of agents / population size
K = N # threashold for collective action

net_type = "F" # network type: (S)tar, (F)ully connected

alpha = 0.3 # belief learning rate
delta = 0.95 # discount factor

p_f, f = 100.0, 0.5 # pf: fairness benchmark, f: unfairness parameter [0,1] = 1 - (x/p_f)

alpha_p = 1.15
p_0, p_1 = (1.0 - f) * p_f, alpha_p * p_f # inital offer, increased offer 

#V_0, V_1 = 0.0, 50.0 # continuation value, shouldnt these be proportional to p_0 / p_1?
V_0, V_1 = 0.0, p_1


risk_av = False



pop_sizes = [3, 10, 50]

for pop in pop_sizes:
    dir_name = make_dir()
    agent_aggs = [pop, pop, alpha, delta, p_f, f, p_0, p_1, V_0, V_1]
    run_sims(N_sims, 
                T, 
                net_type,
                pop,
                agent_aggs,
                dir_name)
