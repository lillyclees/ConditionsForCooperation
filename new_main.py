import matplotlib.pyplot as plt
import math
import os
import datetime
import numpy as np


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

def get_exp_util(x,y, p_rej, pop_size, risk_av=False):
        accept = x
        if risk_av:
            accept = math.log(x)
        reject = np.power(p_rej, (pop_size - 1)) * y
        return accept, reject


def save_game_info(n_episodes, episode_length, x, y, pop_size, start_probs, dir, risk, dec_rule):
    with open(f'{dir}/run info.txt', 'w') as file:
        info = [f"Number of episodes: {n_episodes}",
                f"Rounds per episode: {episode_length}",
                f"Number of players: {pop_size}",
                f"x: {x}",
                f"y: {y}",
                f"Risk aversion: {risk}"]
        file.writelines(line + "\n" for line in info)
        if dec_rule == "S":
            file.write('Playing mixed strategy\n')
        if dec_rule == "B":
            file.write('Playing best response\n')
        if start_probs == "random":
            file.write('Players initialised with random mixed strategies\n')
        if start_probs == "pdf":
            file.write('Players initialised with p accept corresponding to a sample from a PDF with mean=0.5 std=0.1\n')

def run_episodes(n_episodes, episode_length, x, y, pop_size, dir):
        data = []
        # running each episode and plotting episode outcome
        for episode in range(n_episodes):
            episode_data = run_simulation(pop_size, episode_length, x, y)
            plot_episode_outcome(episode_data, dir, episode)
            data.append(episode_data[0])

        # plot average probability of acceptance over time for each episode
        plot_episodes_outcomes(data, dir, n_episodes)



def run_simulation(pop_size=100, steps=1000, x=5, y=10, dec_rule="S", risk_av=False):
    alpha = np.ones(pop_size)
    beta = np.ones(pop_size)

    p_accept = alpha / (alpha + beta)
    history = [[],[],[]]

    for step in range(steps):
        actions = np.random.rand(pop_size) < p_accept # True = Accept, False = Reject
        if dec_rule == "S" or step < 5:
            acceptances = np.sum(actions)
        if dec_rule == "B":
            eu_accept, eu_reject = get_exp_util(x, y, 1-p_accept, pop_size)
            if eu_accept > eu_reject:
                acceptances = pop_size

        alpha += acceptances
        beta += (pop_size - acceptances)
        p_accept = alpha / (alpha + beta)

        history[0].append(p_accept)
        history[1].append(acceptances)
        history[2].append(pop_size - acceptances)

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
pop_size = 100
x = 5
y = 15
n_episodes = 10
episode_length = 1000
dec_rule = "B" # S = accept with probability other players accept, B = best response
start_probs = "pdf" # random / pdf
risk_av = False

run_episodes(n_episodes, episode_length, x, y, pop_size, dir_name)
