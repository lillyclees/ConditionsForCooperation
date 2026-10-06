import math
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class Agent():
    def __init__(self, N, rho, beta, C, r, inc_fair=True):
        self.rho = rho # p: risk aversion coefficient
        #self.B = 0 # b: decision noise
        self.beta = beta # choice sensitivity
        self.C = C # rejection cost

        self.influenced_fairness_crit = inc_fair

        self.N = N # population size
        self.r = r # r: reservation threashold, minimum amount of compensation / maximum cost 

        #self.alpha = 1
        #self.beta = 1

        self.prob_accept = 0.5
        self.prob_reject = 0.5

        self.prob_others_accept = 0.5
        self.prob_others_reject = 0.5

        self.last_choice = 0
        self.total_util = 0
        self.time = 0 # number of moves made

        self.neighbor_beliefs  = [] # [num on acceptances, # of rejections, p of accepting]

    def create_neighors(self,neighbors):
        for i in range(len(neighbors)):
            self.neighbor_beliefs.append([1, 1, 0.5])

    def update_belief(self, neighbors):
        # belief of agent i that agent j will reject offer
        # calculating for each neighbor to account for later cases of agent-specific trust
        for j in range(len(neighbors)):
            self.neighbor_beliefs[j][0] += neighbors[j][0]
            self.neighbor_beliefs[j][1] += neighbors[j][1]
            self.neighbor_beliefs[j][2] += self.neighbor_beliefs[j][0] / (self.neighbor_beliefs[j][0] + self.neighbor_beliefs[j][1])
        
        self.prob_accept = sum(i[2] for i in self.neighbor_beliefs) / len(self.neighbor_beliefs)
        self.prob_reject = 1 - self.prob_accept

        # probabiliy atleast K others reject 
        
        #p_K_others_rej = 0
        #for i in range(self.K, self.N):
        #    p_K_others_rej += self.prob_reject ** i
            

        #self.alpha += acceptances
        #self.beta += rejections
        #self.prob_accept = self.alpha / (self.alpha + self.beta)
        #self.prob_reject = 1 - self.prob_accept

    def update_strategy(self):
        pass

    def move(self, current_p, delta, V_1, V_0): 
        self.time += 1

        eu_acc, eu_rej = self.get_exp_util(current_p, delta, V_1, V_0)

        # delta_eu = eu_reject - eu_accept
        # p_reject = 1.0 / (1.0 + np.exp(-self.beta * delta_EU)
        
        p_reject = math.exp((self.beta * eu_rej)) / (math.exp((self.beta * eu_acc)) + math.exp((self.beta * eu_rej)))

        choice = np.random.choice([1,0], size=1, p=[(1-p_reject), p_reject]) # 1: accept, 0: reject

        self.last_choice = choice

        return choice

    def payoff(self, current_p, threash_met):
        payoff = current_p if self.last_choice == 1 or threash_met else 0


    def get_exp_util(self, current_p, delta, V_1, V_0):
        # utility for accept
        u_acc_succ = self.util(current_p - self.r + delta * V_1, self.rho)
        u_acc_fail = self.util(current_p - self.r + delta * V_0, self.rho)
        EU_accept = self.prob_others_reject * u_acc_succ + (1 - self.prob_others_reject) * u_acc_fail

        # utility for reject
        u_rej_succ = self.util(-self.C + delta * V_1, self.rho)
        u_rej_fail = self.util(-self.C + delta * V_0, self.rho)
        EU_reject = self.prob_others_reject * u_rej_succ + (1 - self.prob_others_reject) * u_rej_fail

        return EU_accept, EU_reject

        #accept = x
        #if self.risk_av:
        #    accept = math.log(x)
        #reject = np.power(p_rej, (self.pop_size - 1)) * y
        #return accept, reject
    
    def util(self, x, rho):
        return -np.exp(-rho * x)

    
    def calculate_res_threash(self, fairness_benchmark, std_dev=0.1):
        # res threash drawn from normal dist centered on pf
        self.reservation_threashold = norm.rvs(loc=fairness_benchmark, scale=std_dev, size=1)
