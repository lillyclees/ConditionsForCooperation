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

