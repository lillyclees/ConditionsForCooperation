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
n_episodes = 100
episode_length = 100
pop_size = 3
n_type = "F" # network type: (S)tar, (F)ully connected

x = 5 # p0: inital offer 
y = 5 # ammount offer is increased by
threashold = pop_size #K

inc_fair = True # included in fairness: yet to implement this, for now it is universal 
fair_b = y # pf: fairness benchmark - ditto
unfairness_param = 1 - (x/fair_b) #f: unfairness parameter [0,1] - ditto 

dec_rule = "B" # S = accept with probability other players accept, B = best response
risk_av = False


run_episodes(n_episodes, 
             episode_length, 
             threashold, 
             pop_size, 
             x, y, 
             dec_rule, 
             risk_av, 
             inc_fair, 
             n_type, 
             dir_name,
             fair_b,
             unfairness_param,
             res_threash=0)
