from agent import *
import os
import datetime
import csv


def create_agents(pop_size, start_probs, rule, risk, x, y):
    players = []
    for i in range(pop_size):
        player = Agent(pop_size, x, y, dec_rule=rule, risk_av=risk)
        if start_probs == "pdf":
            player.pdf_starting_probs()
        if start_probs == "random":
            player.random_starting_probs()

        players.append(player)

    return players

def plot_episodes_outcomes(data, dir, episodes):
    plt.plot(data)
    plt.xlabel('Steps')
    plt.ylabel('Avg Probability of Accepting')
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

def run_episodes(n_episodes, episode_length, x, y, pop_size, game_type, start_probs, dir, risk, dec_rule):

    # writing run information to run info.txt
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


        data = []
        # running each episode and plotting episode outcome
        for episode in range(n_episodes):
            avg_probs, acceptance_trend = run_episode(episode_length, x, y, pop_size, str(episode), game_type,
                                                      start_probs, episode, dir, risk, dec_rule)
            rejections = [pop_size - i for i in acceptance_trend]
            plot_episode_outcome([avg_probs, acceptance_trend, rejections], dir, episode)
            data.append(avg_probs)
        # plot average probability of acceptance over time for each episode
        plot_episodes_outcomes(data, dir, n_episodes)


def run_episode(episode_length, x, y, pop_size, game_no, game_type, start_probs, episode, dir, risk, dec_rule):
    file_name = game_type + game_no + start_probs + "x=" + str(x) + "y=" + str(y)
    players = create_agents(pop_size, start_probs, dec_rule, risk, x, y)

    avg_probs = []
    acceptance_trend = []
    data = []

    for step in range(episode_length):

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
        acceptance_trend.append(acceptances)

        # plot player 1's Bayesian distribution every 100 steps
        #if step % 100 == 0:
        #    players[0].plot_dist(dir, episode)

    # save episode info to csv
    with open(f'{dir}/{file_name}.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Step", "Acceptances", "Prob Accepts", "Total Payoffs"])
        writer.writeheader()
        writer.writerows(data)

    return avg_probs, acceptance_trend

# log files set-up
run = datetime.datetime.now()
run = run.strftime("%m:%d:%Y, %H:%M:%S")
dir_name = f"run {run}"
os.mkdir(dir_name)
new_dir = f"{dir_name}/episodes"
os.mkdir(new_dir)

fields = ['Step', 'Acceptances', 'Beliefs', 'Total Payoffs']
game_type = "simple"


# game parameters
pop_size = 100
x = 5
y = 15
n_episodes = 1
episode_length = 100
dec_rule = "B" # S = accept with probability other players accept, B = best response
start_probs = "pdf" # random / pdf
risk_av = False

run_episodes(n_episodes, episode_length, x, y, pop_size, game_type, start_probs, dir_name, risk_av, dec_rule)






