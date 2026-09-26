import math
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class Agent():
    def __init__(self, pop_size, x, y, dec_rule="S", risk_av=False):
        self.dec_rule = dec_rule # S = accept with probability other players accept, B = best response
        self.risk_av = risk_av # toggle for expected utility with risk aversion

        self.pop_size = pop_size
        # x and y are payoffs
        # 0 < x < y
        self.x = x # if player accepts offer
        self.y = y # if all players reject offer

        self.alpha = 1
        self.beta = 1

        self.prob_accept = 0.5
        self.prob_reject = 0.5

        self.prob_others_accept = 0.5
        self.prob_others_reject = 0.5

        self.last_choice = 0
        self.total_util = 0
        self.time = 0 # number of moves made


    def move(self):
        self.time += 1

        # playing mixed strategy for at least the first 5 moves
        if self.dec_rule == "S" or self.time < 5:
            choice = np.random.choice(["accept","reject"], size=1, p=[self.prob_accept, self.prob_reject])

        # playing best response
        elif self.dec_rule == "B":
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
        self.alpha += acceptances
        self.beta += (self.pop_size - acceptances)
        self.prob_accept = self.alpha / (self.alpha + self.beta)
        self.prob_reject = 1 - self.prob_accept


    def plot_dist(self, dir, episode):
        ### copied from: https://statsthinking21.github.io/statsthinking21-python/10-BayesianStatistics.html ###
        # plot the likelihood, prior, and posterior

        plt.plot(self.bayes_df['proportion'], self.bayes_df['likelihood'], label='likelihood')
        plt.plot(self.bayes_df['proportion'], self.bayes_df['prior'], label='prior')
        plt.plot(self.bayes_df['proportion'], self.bayes_df['posterior'],
                 'k--', label='posterior')
        ##### copy ends

        plt.legend()
        plt.grid(True)
        new_dir = f"{dir}/episode {str(episode)} figs"
        os.mkdir(new_dir)
        plt.savefig(f"{new_dir}/agent1 step {self.time}.jpg")
        plt.close()
        #plt.show()



    def get_exp_util(self, p_rej):
        accept = self.x
        if self.risk_av:
            accept = math.log(self.x)
        reject = np.power(p_rej, (self.pop_size - 1)) * self.y
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

