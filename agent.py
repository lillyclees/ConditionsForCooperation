import math
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class Agent():
    def __init__(self, K, N, rho, beta, C, r, inc_fair=True):
        self.rho = rho # p: risk aversion coefficient
        self.beta = beta # choice sensitivity
        self.C = C # rejection cost

        self.influenced_fairness_crit = inc_fair

        self.K = K # threashold 
        self.N = N # population size
        self.r = r # r: reservation threashold, minimum amount of compensation / maximum cost 

        self.p_reject = 0.5

        self.prob_others_reject = 0.5

        self.last_choice = 0
        self.total_util = 0
        self.time = 0 # number of moves made

        self.neighbor_beliefs  = [] # [# of acceptances, # of rejections, p of accepting]

    def create_neighors(self,neighbors):
        for i in range(len(neighbors)):
            self.neighbor_beliefs.append([1, 1, 0.5])

    def update_belief(self, neighbors):
        # belief of agent i that agent j will reject offer
        # calculating for each neighbor to account for later cases of agent-specific trust
        for j in range(len(neighbors)):
            self.neighbor_beliefs[j][0] += neighbors[j][0]
            self.neighbor_beliefs[j][1] += neighbors[j][1]
            self.neighbor_beliefs[j][2] = self.neighbor_beliefs[j][0] / (self.neighbor_beliefs[j][0] + self.neighbor_beliefs[j][1])
        
        # probability an independent agent rejects 
        self.prob_others_reject = 1 - sum(i[2] for i in self.neighbor_beliefs) / len(self.neighbor_beliefs)


    def move(self, current_p, p_1, delta, V_1, V_0): 
    
        self.time += 1

        eu_acc, eu_rej = self.get_exp_util(current_p, p_1, delta, V_1, V_0)
        
        #delta_eu = eu_rej - eu_acc
        #p_reject = 1.0 / (1.0 + np.exp(-self.beta * delta_eu))
        
        p_reject = math.exp((self.beta * eu_rej)) / (math.exp((self.beta * eu_acc)) + math.exp((self.beta * eu_rej)))
        self.p_reject = p_reject

        
        if random.uniform(0,1) > p_reject:
            choice = 1
        else:
            choice = 0

        self.last_choice = choice

        return choice


    def get_exp_util(self, current_p, p_1, delta, V_1, V_0):
        p_K_others_rej = 0
        for i in range(self.K, self.N):
            p_K_others_rej += self.prob_others_reject ** i

        p_K_less_others_rej = p_K_others_rej + self.prob_others_reject ** self.N
        
    
        # utility for accept
        #u_acc_succ = self.util(current_p - self.r + delta * V_1, self.rho)
        #u_acc_fail = self.util(current_p - self.r + delta * V_0, self.rho)
        #EU_accept = p_K_others_rej * u_acc_succ + (1 - p_K_others_rej) * u_acc_fail
        
        # agumented version 
        u_acc_succ = self.util(p_1 - self.r + delta * V_1, self.rho)
        u_acc_fail = self.util(current_p - self.r + delta * V_0, self.rho)
        EU_accept = p_K_others_rej * u_acc_succ + (1 - p_K_others_rej) * u_acc_fail


        # utility for reject
        #u_rej_succ = self.util(-self.C + delta * V_1, self.rho)
        #u_rej_fail = self.util(-self.C + delta * V_0, self.rho)
        #EU_reject = p_K_others_rej * u_rej_succ + (1 - p_K_others_rej) * u_rej_fail

        # agumented version 
        u_rej_succ = self.util(p_1 + delta * V_1, self.rho)
        u_rej_fail = self.util(-self.C + delta * V_0, self.rho)
        print(u_acc_fail)
        EU_reject = p_K_less_others_rej * u_rej_succ + (1 - p_K_less_others_rej) * u_rej_fail
        
        #print(u_acc_succ, u_acc_fail)
        #print(u_rej_succ, u_rej_fail)
        #print("===")

        return EU_accept, EU_reject

    
    def util(self, x, rho):
        return 1 - np.exp(-rho * x)


