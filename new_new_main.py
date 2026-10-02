import matplotlib.pyplot as plt
import math
import os
import datetime
import numpy as np
from new_agent import *


def plot_episodes_outcomes(data, dir, episodes):
    for episode in data:
        plt.plot(episode)
    plt.xlabel('Steps')
    plt.ylabel(f'Avg Probability of Accepting over {episodes} Episodes')
    plt.savefig(f"{dir}/{episodes} episodes")
    plt.close()
    #plt.show()

def plot_episode_outcome(ep_data, dir, episode):
    plt.plot(ep_data[0])
    plt.xlabel('Steps')
    plt.ylabel('Avg Probability of Accepting')
    plt.savefig(f"{dir}/episodes/probs_episode {episode}")
    plt.close()

    plt.plot(ep_data[1], label="Acceptances")
    plt.plot(ep_data[2], label="Rejections")
    plt.legend(loc='best')
    plt.xlabel('Steps')
    plt.ylabel('No Players')
    plt.savefig(f"{dir}/episodes/episode {episode}")
    plt.close()
    #plt.show()


def save_game_info(n_episodes, episode_length, x, y, pop_size, dir, risk, dec_rule, conv_to_reject):
    with open(f'{dir}/run info.txt', 'w') as file:
        info = [f"Number of episodes: {n_episodes}",
                f"Rounds per episode: {episode_length}",
                f"Number of players: {pop_size}",
                f"x: {x}",
                f"y: {y}",
                f"Risk aversion: {risk}",
                f"{conv_to_reject} episodes converged to reject",
                f"{n_episodes - conv_to_reject} episodes converged to accept"]
        
        file.writelines(line + "\n" for line in info)
        if dec_rule == "S":
            file.write('Playing mixed strategy\n')
        if dec_rule == "B":
            file.write('Playing best response\n')
        

def run_episodes(n_episodes, episode_length, x, y, pop_size, dir, dec_rule, risk_av=False):
        data = []
        conv_to_reject = 0
        # running each episode and plotting episode outcome
        for episode in range(n_episodes):
            agents = build_agents(x,y, pop_size, dec_rule, risk_av)
            episode_data = run_simulation(agents, episode_length)

            # only plotting the first episode that converges to reject 
            if episode_data[1][-1] == 0:
                if conv_to_reject == 0:
                    plot_episode_outcome(episode_data, dir, episode)
                conv_to_reject += 1

            data.append(episode_data[0])

        # plot average probability of acceptance over time for each episode
        plot_episodes_outcomes(data, dir, n_episodes)
        save_game_info(n_episodes, episode_length, x, y, pop_size, dir, risk_av, dec_rule, conv_to_reject)

def build_agents(x, y, pop_size, dec_rule, risk_av):
    agents = []
    for i in range(pop_size):
        player = Agent(pop_size, x, y, dec_rule, risk_av)
        player.random_starting_probs()
        agents.append(player)
    return agents 

def run_simulation(agents, steps=1000):
    history = [[],[],[]]

    for step in range(steps):
        acceptances = 0
        for agent in agents:
            if agent.move() == "accept":
                acceptances += 1

        for agent in agents:
            agent.update_belief(acceptances)
            agent.payoff(acceptances)       

        history[0].append(agents[0].prob_accept)
        history[1].append(acceptances)
        history[2].append(len(agents) - acceptances)

    return history



# log files set-up
run = datetime.datetime.now()
run = run.strftime("%m:%d:%Y, %H:%M:%S")
dir_name = f"run {run}"
os.mkdir(dir_name)
new_dir = f"{dir_name}/episodes"
os.mkdir(new_dir)

game_type = "simple"


# game parameters
n_episodes = 100
episode_length = 100
pop_size = 3
x = 5
y = 10

dec_rule = "B" # S = accept with probability other players accept, B = best response
risk_av = False

run_episodes(n_episodes, episode_length, x, y, pop_size, dir_name, dec_rule=dec_rule, risk_av=risk_av)
