import math
from math import comb
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import beta


class Agent():
    def __init__(self, pop_size, x, y, dec_rule="S", risk_av=False):
        self.dec_rule = dec_rule # S = accept with probability other players accept, B = best response
        self.risk_av = risk_av # toggle for expected utility with risk aversion

        self.pop_size = pop_size
        # x and y are payoffs
        # 0 < x < y
        self.x = x # if player accepts offer
        self.y = y # if all players reject offer

        self.n_strats = comb(self.pop_size, 2)

        self.theta = np.linspace(0, 1, self.pop_size)
        self.posterior = beta.pdf(self.theta, 1, 1)
        self.ac_prior = 1
        self.rej_prior = 1

        self.prob_accept = 0.5
        self.prob_reject = 0.5

        self.prob_others_accept = 0.5
        self.prob_others_reject = 0.5

        self.last_choice = 0
        self.total_util = 0

    def move(self):

        # playing mixed strategy
        if self.dec_rule == "S":
            choice = np.random.choice(["accept","reject"], size=1, p=[self.prob_accept, self.prob_reject])

        # playing best response
        if self.dec_rule == "B":
            ac, rej = self.get_exp_util(self.prob_reject)
            if ac > rej:
                choice = "accept"
            else:
                choice = "reject"

        self.last_choice = choice

        return choice

    def payoff(self, accept):
        # payoff is y if every player rejects offer
        # otherwise it is x (if player accepts) or 0 (if player rejects)
        if self.last_choice == "reject" and accept == False:
            payoff = self.y
        elif self.last_choice == "accept":
            payoff = self.x
        else:
            payoff = 0
        self.total_util += payoff

    def update_belief(self, acceptances):
        #n = self.pop_size
        #k = acceptances

        #prior = self.prob_accept # P(H)
        #likelihood = comb(n, k) * np.power(prior, k) * np.power((1-prior), n-k) # P(D|H)
        #norm_constant = comb(n, k) * np.power(1 - prior, k) * np.power((prior), k) # P(D)
        #posterior = (prior * likelihood) / (norm_constant + likelihood) # P(H|D)


        self.ac_prior += acceptances
        self.rej_prior += self.pop_size - acceptances

        # updating probability distribution for accept given the previous number of acceptances / rejections
        self.posterior = beta.pdf(self.theta, self.ac_prior, self.rej_prior)

        # mean likelihood player accepts offer
        mean = self.posterior.mean()

        # assuming the players belief of the probability others accept is same as probability they will accept
        self.prob_accept = mean
        self.prob_reject = 1 - mean

    def plot_dist(self):
        plt.plot(self.theta, self.posterior, label='Bayesian Update of Acceptances / Rejections')
        plt.xlabel('Projected Likelihood of Accepting')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_exp_util(self, p_rej):
        accept = self.x
        if self.risk_av:
            accept = math.log(self.x)
        reject = np.power(p_rej, (self.pop_size - 1)) * self.y
        return accept, reject



    def random_starting_probs(self, mean=0.5, std_dev=0.1):

        # Agents starting probability of accept is a random sample from a pdf
        # centered at 0.5

        lin_space = np.linspace(0,1,100)
        norm.pdf(lin_space, loc=mean, scale=std_dev)
        p_accept = norm.rvs(loc=mean, scale=std_dev, size=1)

        self.prob_accept = p_accept[0]
        self.prob_reject = 1 - p_accept[0]

        self.prob_others_reject = self.prob_reject
        self.prob_others_accept = self.prob_accept

