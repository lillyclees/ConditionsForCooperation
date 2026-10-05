import matplotlib.pyplot as plt
import math
import os
import datetime
import numpy as np
from agent import *
import networkx as nx

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


def save_game_info(n_episodes, episode_length, x, y, pop_size, dir, risk, dec_rule, conv_to_reject, n_type):
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
        if n_type == "S":
            file.write('Star network\n')
        else:
            file.write('Fully connected network\n')
        

def run_episodes(n_episodes, episode_length, K, pop_size, x, y, dec_rule, risk_av, inc_fair, n_type, dir, pf, f, res_threash):
        data = []
        conv_to_reject = 0
        # running each episode and plotting episode outcome
        for episode in range(n_episodes):
            agents = build_agents(K, pop_size, x, y, res_threash, dec_rule, risk_av, inc_fair)
            if n_type == "S":
                agents = nx.star_graph(agents)
            else:
                agents = nx.complete_graph(agents)

            episode_data = run_simulation(agents, x, y, K, episode_length)

            # only plotting the first episode that converges to reject 
            if episode_data[1][-1] == 0:
                if conv_to_reject == 0:
                    plot_episode_outcome(episode_data, dir, episode)
                conv_to_reject += 1

            data.append(episode_data[0])

        # plot average probability of acceptance over time for each episode
        plot_episodes_outcomes(data, dir, n_episodes)

        save_game_info(n_episodes, episode_length, x, y, pop_size, dir, risk_av, dec_rule, conv_to_reject, n_type)


def run_simulation(G, x, y, K, steps=1000):
    history = [[],[],[]]
    a_offer = x
    agents = list(G.nodes)
    for step in range(steps):
        r_offer = 0
        acceptances = 0
        for agent in agents:
            if agent.move(a_offer, (a_offer + y)) == "accept":
                acceptances += 1

        if acceptances >= K:
            a_offer += y
            r_offer = a_offer

        for agent in agents:

            agent.payoff(a_offer, r_offer)

            peer_acceptances = 0
            peer_rejections = 0
            for peer in list(G.neighbors(agent)):
                if peer.last_choice == "accept":
                    peer_acceptances += 1
                else:
                    peer_rejections += 1

            agent.update_belief(peer_acceptances, peer_rejections)

        history[0].append(agents[0].prob_accept)
        history[1].append(acceptances)
        history[2].append(len(agents) - acceptances)

    return history


def build_agents(K, pop_size, x, y, res_threash, dec_rule, risk_av, inc_fair):
    agents = []
    for i in range(pop_size):
        # define res threash, CARA risk av, noise, fairness participateion 
        player = Agent(K, pop_size, x, y, res_threash, dec_rule, risk_av, inc_fair)
        player.random_starting_probs()
        agents.append(player)

    return agents
