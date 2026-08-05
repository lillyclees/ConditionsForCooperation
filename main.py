from agent import *

def create_agents(pop_size):
    players = []
    for i in range(pop_size):
        player = Agent(pop_size, x, y)
        player.Random_starting_probs()
        players.append(player)

    return players

def plot_outcome(data):
    plt.plot(data)
    plt.xlabel('Episode')
    plt.ylabel('Avg Probability of Accepting')
    plt.show()


fields = ['Episode', 'Acceptances', 'Beliefs', 'Total Payoffs']
game_type = "simple"
game_no = "1"
start_probs = "1n_strats"
file_name = game_type + game_no + start_probs

avg_probs = []
pop_size = 100
x = 5
y = 10
n_episodes = 10

players = create_agents(pop_size)

data = []

for episode in range(n_episodes):
    accept = False
    acceptances = 0
    prob_accepts = []
    total_payoffs = []

    # make moves
    for player in players:
        if player.move() == "accept":
            accept = True
            acceptances += 1
        prob_accepts.append(player.prob_accept)

    # disperse payoffs and update beliefs
    for player in players:
        player.payoff(accept)
        player.update_belief(acceptances)
        total_payoffs.append(player.total_util)

    #players[0].plot_dist()

    episode_data = {}
    episode_data["Episode"] = episode
    episode_data["Acceptances"] = acceptances
    episode_data["Prob Accepts"] = prob_accepts
    episode_data["Total Payoffs"] = total_payoffs
    data.append(episode_data)

    avg_probs.append(sum(prob_accepts) / pop_size)

plot_outcome(avg_probs)


with open(f'{file_name}.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Episode", "Acceptances", "Prob Accepts", "Total Payoffs"])
    writer.writeheader()
    writer.writerows(data)



















