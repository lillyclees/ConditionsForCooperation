from agent import *
import os
import datetime
import csv


def create_agents(pop_size):
    players = []
    for i in range(pop_size):
        player = Agent(pop_size, x, y, dec_rule="S", risk_av=False)
        player.random_starting_probs()
        players.append(player)

    return players

def plot_episodes_outcome(data, dir, episodes):
    plt.plot(data)
    plt.xlabel('Steps')
    plt.ylabel('Avg Probability of Accepting')
    plt.savefig(f"{dir}/{episodes} episodes")
    #plt.show()

def plot_episode_outcome(data, dir, episode):
    plt.plot(data)
    plt.xlabel('Steps')
    plt.ylabel('Avg Probability of Accepting')
    plt.savefig(f"{dir}/episode {episode}")
    #plt.show()

def run_episodes(n_episodes, episode_length, x, y, pop_size, game_no, game_type, start_probs, dir):
    data = []
    for episode in range(n_episodes):
        avg_probs = run_episode(episode_length, x, y, pop_size, game_no + str(episode), game_type, start_probs, episode, dir)
        plot_episode_outcome(avg_probs, dir, episode)
        data.append(avg_probs)
    plot_episodes_outcome(data, dir, n_episodes)


def run_episode(episode_length, x, y, pop_size, game_no, game_type, start_probs, episode, dir):
    file_name = game_type + game_no + start_probs + "x=" + str(x) + "y=" + str(y)
    players = create_agents(pop_size)

    avg_probs = []
    data = []

    for step in range(episode_length):
        print(step)
        accept = False
        acceptances = 0
        prob_accepts = []
        total_payoffs = []

        # make moves
        for player in players:
            if player.move() == "accept":
                accept = True
                acceptances += 1
            if player.prob_accept > 1:
                print("wrong")
            prob_accepts.append(player.prob_accept)

        # disperse payoffs and update beliefs
        for player in players:
            player.payoff(accept)
            player.update_belief(acceptances)
            total_payoffs.append(player.total_util)

        episode_data = {}
        episode_data["Step"] = step
        episode_data["Acceptances"] = acceptances
        episode_data["Prob Accepts"] = prob_accepts
        episode_data["Total Payoffs"] = total_payoffs
        data.append(episode_data)


        avg_probs.append(sum(prob_accepts) / pop_size)

        if step % 100 == 0:
            players[0].plot_dist(dir, episode)


    with open(f'{dir_name}/{file_name}.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Step", "Acceptances", "Prob Accepts", "Total Payoffs"])
        writer.writeheader()
        writer.writerows(data)

    return avg_probs

# log saving set-up
run = datetime.datetime.now()
dir_name = f"run {run}"
os.mkdir(dir_name)
fields = ['Step', 'Acceptances', 'Beliefs', 'Total Payoffs']
game_type = "simple"
game_no = "1"
start_probs = "random"

# game parameters
pop_size = 100
x = 5
y = 10
n_episodes = 1
episode_length = 1000

#run_episodes(n_episodes, episode_length, x, y, pop_size, game_no, game_type, start_probs)
















