# I hate Katan

Are you tired of losing Katan and your friends making fun of you? Up until now, the right tool found you. Say no more to losing in Katan!

## Requirements

- agent receives game board state, based on that it should work out the best possible winning strategy

### MVP

- simulation for just one player (expected low branching and strategy entropy),
- constant board layout,
- just final output

## Problem characteristics

By STATE I understand a given board state, which include:

- tile:
  - resource type,
  - numeric value
- player constructions:
  - villages,
  - roads,
  - cities
- also, the position of the thief,
- player resources?

By ACTIONS I understand the move a player can make from given state, obviously some states are not possible to achieve due to i.e. insufficient resources. Here are all possible ACTIONS:

- use resources for a construction or random gain (development card)

Game events:

- dice rolls,
- development card, there are couple possible options that can be done:
  - place a knight and reposition the thief (which lets the player to pick random card from selected opponent), this card is the most often,
  - score a point,
  - get selected resource from all players,
  - others
- resource theft

### Assumptions

- I can't explore all possible states, there are too many possible options,
- players can ruin the strategy, agent should adapt it after a change,
- the faster win strategy gives, the better,
