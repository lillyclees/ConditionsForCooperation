y > x > 0

M = number of players that must reject to trigger new offer

> (in a simple stag hunt game M = population size) 

y = payoff for all if >= M players reject

x = payoff for accept 

0 = payoff for reject if < M players reject 

utility function for arbitrary player p:

accept =  x

reject = (probability p rejects)<sup>pop size - 1</sup> * y


episode structure:
1. each player is assigned a random probability of accepting / rejecting 
3. for steps 1-5 
- 3.1. players move with respect to their probabilities 
- 3.2. players recieve information on total number of rejections / acceptances 
- 3.3. players update their belief that others will reject / accept
- 3.4. players use this belief as their new probability 
4. for steps 1-n 
- 4.1. players play best response with respect to their belief 
- 4.2. players update their belief 

## Results so far
As the number of players increase, the likelihood of converging to reject decreases.
When the upper bound of the reward (y) is increased the likelihood of converging to reject increases 

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/7d5029be-30aa-4034-8828-97699bb7548e" />

Number of episodes: 100
Rounds per episode: 100
Number of players: 3
x: 5
y: 10
Risk aversion: False
20 episodes converged to reject
80 episodes converged to accept
Playing best response

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/c055634f-e36d-493c-aa35-86506988bfc6" />

Number of episodes: 100
Rounds per episode: 100
Number of players: 5
x: 5
y: 10
Risk aversion: False
9 episodes converged to reject
91 episodes converged to accept
Playing best response

  <img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/0cf48eae-8a99-4c2c-8ce4-6b724b675b4b" />

Number of episodes: 100
Rounds per episode: 100
Number of players: 10
x: 5
y: 10
Risk aversion: False
0 episodes converged to reject
100 episodes converged to accept
Playing best response


<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/4f2cc52c-49cb-43e9-b54d-5d5ec93dacc0" />

Number of episodes: 100
Rounds per episode: 100
Number of players: 10
x: 5
y: 15
Risk aversion: False
1 episodes converged to reject
99 episodes converged to accept
Playing best response


<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/acfbde54-51d7-4364-90c9-3b457e04526c" />

Number of episodes: 1000
Rounds per episode: 100
Number of players: 25
x: 5
y: 10
Risk aversion: False
0 episodes converged to reject
1000 episodes converged to accept
Playing best response

