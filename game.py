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


def save_game_info(N_sims, T, N, dir, agent_aggs, conv_to_reject, n_type):
    with open(f'{dir}/run info.txt', 'w') as file:
        info = [f"Number of episodes: {N_sims}",
                f"Rounds per episode: {T}",
                f"Number of players: {N}",
                f"{conv_to_reject} episodes converged to reject",
                f"{N_sims - conv_to_reject} episodes converged to accept"]
        
        file.writelines(line + "\n" for line in info)
        file.writelines(str(line) + "\n" for line in agent_aggs)

        if n_type == "S":
            file.write('Star network\n')
        else:
            file.write('Fully connected network\n')
        

def run_sims(N_sims, T, n_type, N, K, agent_aggs, dir):
        data = []
        conv_to_reject = 0
        # running each episode and plotting episode outcome
        for episode in range(N_sims):
            agents = build_agents(*agent_aggs)

            if n_type == "S":
                agents = nx.star_graph(agents)
            else:
                agents = nx.complete_graph(agents)
            
            # creating belief state about each neighbor
            for agent in agents.nodes():
                agent.create_neighors(list(agents.neighbors(agent)))

            episode_data = run_simulation(agents, K, *agent_aggs, T)

            # only plotting the first episode that converges to reject 
            if episode_data[1][-1] == 0:
                if conv_to_reject == 0:
                    plot_episode_outcome(episode_data, dir, episode)
                conv_to_reject += 1

            data.append(episode_data[0])

        # plot average probability of acceptance over time for each episode
        plot_episodes_outcomes(data, dir, N_sims)

        save_game_info(N_sims, T, N, dir, agent_aggs, conv_to_reject, n_type)


def run_simulation(G, K, N, alpha, delta, p_f, f, p_0, p_1, V_0, V_1, inc_fair, steps=1000):
    history = [[],[],[]]
    current_p = p_0

    agents = list(G.nodes)
    for step in range(steps):
        threash_met = False
        acceptances = 0
        for agent in agents:
            if agent.move(current_p, delta, V_1, V_0) == 1:
                acceptances += 1

        if acceptances >= K:
            current_p = p_1
            threash_met = True

        for agent in agents:
            agent.payoff(current_p, threash_met)

            neighbors = []
            for peer in list(G.neighbors(agent)):
                neighbors.append([1 - peer.last_choice, peer.last_choice])

            agent.update_belief(neighbors)

        history[0].append(agents[0].prob_accept)
        history[1].append(acceptances)
        history[2].append(len(agents) - acceptances)

    return history


def build_agents(N, alpha, delta, p_f, f, p_0, p_1, V_0, V_1):
    agents = []

    rho = np.random.uniform(0.01, 0.10, size=N) # p: risk aversion coefficient
    beta = np.random.uniform(1.0, 5.0, size=N) # b: choice sensitivity
    C = np.random.uniform(2.0, 5.0, size=N) # C: oppertunity cost
    r = np.random.normal(loc=p_f, scale=5.0, size=N) # r: reservation threashold, minimum amount of compensation / maximum cost 
    fairness_part = 1 # [0,1] percentage of agents who participated in generating the fairness criteria

    for i in range(N):
        included = True if random.uniform(0, 1) < fairness_part else False
        player = Agent(N, rho[i], beta[i], C[i], r[i], included)
        agents.append(player)

    return agents
