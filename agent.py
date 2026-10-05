import math
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class Agent():
    def __init__(self, K, pop_size, x, y, res_threash, dec_rule="S", risk_av=0, inc_fair=True):
        self.dec_rule = dec_rule # s: S = accept with probability other players accept, B = best response
        self.risk_av = risk_av # p: risk aversion coefficient
        self.decision_noise = 0 # b: decision noise
        self.influenced_fairness_crit = inc_fair

        self.pop_size = pop_size
        self.threashold = K 
        self.reservation_threashold = res_threash # r: minimum amount of compensation / maximum cost 

        self.alpha = 1
        self.beta = 1

        self.prob_accept = 0.5
        self.prob_reject = 0.5

        self.prob_others_accept = 0.5
        self.prob_others_reject = 0.5

        self.last_choice = 0
        self.total_util = 0
        self.time = 0 # number of moves made

    def update_belief(self, acceptances, rejections):
        #belief of agent i that agent j will reject offer
              #n = self.pop_size
        #k = acceptances

        self.alpha += acceptances
        self.beta += rejections
        self.prob_accept = self.alpha / (self.alpha + self.beta)
        self.prob_reject = 1 - self.prob_accept

    def update_strategy(self):
        pass

    def move(self, x, y): 
        self.time += 1

        # strategy at time t
        # playing mixed strategy for at least the first 5 moves
        if self.dec_rule == "S" or self.time < 5:
            choice = np.random.choice(["accept","reject"], size=1, p=[self.prob_accept, self.prob_reject])

        # playing best response
        elif self.dec_rule == "B":
            ac, rej = self.get_exp_util(self.prob_reject, x, y)
            if ac > rej:
                choice = "accept"
            else:
                choice = "reject"

        self.last_choice = choice

        return choice

    def payoff(self, r_offer, a_offer):
        if self.last_choice == "reject":
            payoff = r_offer # = a_offer + y if threashold met, else = 0
        else:
            payoff = a_offer # = a_offer + y if threashold met, else = a_offer
        self.total_util += payoff


    def get_exp_util(self, p_rej, x, y):
        accept = x
        if self.risk_av:
            accept = math.log(x)
        reject = np.power(p_rej, (self.pop_size - 1)) * y
        return accept, reject

    def random_starting_probs(self):
        self.prob_accept = random.uniform(0, 1.0)
        self.prob_reject = 1 - self.prob_accept

        self.prob_others_reject = self.prob_reject
        self.prob_others_accept = self.prob_accept

    def pdf_starting_probs(self, mean=0.5, std_dev=0.1):

        # Agents starting probability of accept is a random sample from a normal distribution
        # centered at 0.5 with standard deviation 0.1
        p_accept = norm.rvs(loc=mean, scale=std_dev, size=1)

        self.prob_accept = p_accept[0]
        self.prob_reject = 1 - p_accept[0]

        self.prob_others_reject = self.prob_reject
        self.prob_others_accept = self.prob_accept
    
    def calculate_res_threash(self, fairness_benchmark, std_dev=0.1):
        # res threash drawn from normal dist centered on pf
        self.reservation_threashold = norm.rvs(loc=fairness_benchmark, scale=std_dev, size=1)
