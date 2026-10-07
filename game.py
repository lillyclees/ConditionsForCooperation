import matplotlib.pyplot as plt
import math
import os
import datetime
import numpy as np
from agent import *
import networkx as nx
import time


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


def save_game_info(N_sims, T, N, dir, agent_aggs, majority_reject, n_type, time):
    with open(f'{dir}/run info.txt', 'w') as file:
        info = [f"Number of episodes: {N_sims}",
                f"Rounds per episode: {T}",
                f"Number of players: {N}",
                f"Time: {time} secs",
                f"{majority_reject} episodes ended with the majority rejecting ",
                f"{N_sims - majority_reject} episodes ended with the majority accepting",
                f"Threashold: {agent_aggs[0]}",
                f"Alpha: {agent_aggs[2]} (belief learning rate)",
                f"Delta: {agent_aggs[3]} (discount factor)",
                f"p_f: {agent_aggs[4]} (fairness benchmark)",
                f"f: {agent_aggs[5]} (unfairness parameter)",
                f"(1 - f)*p_f == p_0: {agent_aggs[6]} (inital offer)",
                f" {agent_aggs[7]/agent_aggs[6]}*p_0 == p_1: {agent_aggs[7]} (increased offer)",
                f"V_0, V_1: {agent_aggs[8], agent_aggs[9]} (continuation value)"]
        
        file.writelines(line + "\n" for line in info)

        if n_type == "S":
            file.write('Star network\n')
        else:
            file.write('Fully connected network\n')
        

def run_sims(N_sims, T, n_type, N, agent_aggs, dir):
        start = time.time()

        data = []
        majority_reject = 0
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

            episode_data = run_simulation(T, agents, *agent_aggs)

            if episode_data[2][-1] / N > 0.5:
                majority_reject += 1
                if majority_reject < 5:
                    plot_episode_outcome(episode_data, dir, episode)

            data.append(episode_data[0])

        # plot average probability of acceptance over time for each episode
        plot_episodes_outcomes(data, dir, N_sims)

        end = time.time()
        save_game_info(N_sims, T, N, dir, agent_aggs, majority_reject, n_type, end-start)


def run_simulation(T, G, K, N, alpha, delta, p_f, f, p_0, p_1, V_0, V_1):
    history = [[],[],[]]
    current_p = p_0

    agents = list(G.nodes)
    for step in range(T):
        threash_met = False
        acceptances = 0

        # each agent moves
        for agent in agents:
            if agent.move(current_p, p_1, delta, V_1, V_0) == 1:
                acceptances += 1

        # checking if threashold was met, if so, updating reward 
        if acceptances >= K:
            #print(f"step {step} sucsesfully coordinated")
            current_p = p_1
        
        # updating each agent's belief 
        for agent in agents:
            # getting information about agent's neighbor's actions
            neighbors = []
            for peer in list(G.neighbors(agent)):
                neighbors.append([1 - peer.last_choice, peer.last_choice])

            # updating agent's belief 
            agent.update_belief(neighbors)

        history[0].append(acceptances/N)
        history[1].append(acceptances)
        history[2].append(N - acceptances)

    return history


def build_agents(K, N, alpha, delta, p_f, f, p_0, p_1, V_0, V_1):
    agents = []

    rho = np.random.uniform(0.01, 0.10, size=N) # p: risk aversion coefficient
    beta = np.random.uniform(1.0, 5.0, size=N) # b: choice sensitivity
    C = np.random.uniform(p_0, p_0, size=N)
    #C = np.random.uniform(0.5*p_0, 5.0, size=N) # C: oppertunity cost

    r = np.random.normal(loc=p_f, scale=5.0, size=N) # r: reservation threashold, minimum amount of compensation / maximum cost 
    fairness_part = 1 # [0,1] percentage of agents who participated in generating the fairness criteria

    for i in range(N):
        included = True if random.uniform(0, 1) < fairness_part else False
        player = Agent(K, N, rho[i], beta[i], C[i], r[i], alpha, included)
        agents.append(player)

    return agents
