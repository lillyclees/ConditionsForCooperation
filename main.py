import os
import datetime
from game import *

# log files set-up
run = datetime.datetime.now()
run = run.strftime("%m:%d:%Y, %H:%M:%S")
dir_name = f"run {run}"
os.mkdir(dir_name)
new_dir = f"{dir_name}/episodes"
os.mkdir(new_dir)


# game parameters
N_sims = 100 # number of simulation runs / episodes
T = 100 # time steps / episode length

N = 10 # number of agents / population size
K = N # threashold for collective action

net_type = "F" # network type: (S)tar, (F)ully connected

alpha = 0.3 # belief learning rate
delta = 0.95 # discount factor

p_f, f = 100.0, 0.25 # pf: fairness benchmark, f: unfairness parameter [0,1] = 1 - (x/p_f)
p_0, p_1 = (1.0 - f) * p_f, 1.15 * p_f # inital offer, increased offer 

V_0, V_1 = 0.0, 50.0 # continuation value, shouldnt these be proportional to p_0 / p_1?


risk_av = False

agent_aggs = [K, N, alpha, delta, p_f, f, p_0, p_1, V_0, V_1]

run_sims(N_sims, 
             T, 
             net_type,
             N,
             agent_aggs,
             dir_name)
