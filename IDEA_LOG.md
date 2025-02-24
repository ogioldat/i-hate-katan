# Idea log

Record my decision and reasoning process.

## 15 Feb 2025

- use MCTS to simulate game playouts,

## 21 Feb 2025

- use MDP to model certainty of stochastic events such as dice roll, getting a card, placing a thief, etc.
- found the formal definition of regret for RL agents, reading about ways of minimizing regret value (softmax, UCB1, eps greedy),
- need to decide which parts of my project are actually the Multi-Armed Bandit problem

### Rewards in my MCTS

- so far I assumed the reward for my RL problem is granted only at the end of the playout -- when a player wins a game. How about reworking the problem slightly? Maybe I should be more "generous" with rewards, I could reward the agent every time the point is scored 🤔

## 22 Feb 2025

- should I abstract the learning environment even more? I assumed I'm gonna use MCTS, maybe I should consider other options,
- in my case, the "bandit part" is the action selection?
- i'm gonna need some analytical way to measure the efficiency, probably moves to win ratio? might be challenging to keep it unbiased,
- MCTS feels more natural for my task, as TD is suitable for continuous problems,
- if I use MCTS, for a long time there won't be no reward

### Alternative ideas

- using Q-Learning, there states possible for Q-Table is enormous, I need to play it smart and only put entries to the table when needed, this feels possible, Q-Learning won't explore unpromising options at some point,
- should I use Q-Learning, MCTS or others?,
- Q-Learning might express well the ASAP win need,
- MCTS feels to be the simplest option,
- explore TD Lambda

## 23 Feb 2025

- I understand MDP and Bellman's equation better now, the problem I'm dealing with technically could be solved using one of these two standard methods,
- it's more clear to me which parts of the problem are MAB problems,
- do I need sth more complex? RL framework like keras, pytorch agents, OAI Gym? more complex algo like QLN?

### To explore

- DDPG, actor-critic