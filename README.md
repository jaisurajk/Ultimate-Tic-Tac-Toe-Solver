## Team members: 
    Daniel Villalon 
    Jaisuraj Kaleeswaran
    
## Objective

We created a bot that can play Ultimate Tic-Tac-Toe by implementing the Monte Carlo Tree Search (MCTS) Algorithm. The goal of this bot is to beat human players and two bots, rollout_bot and random_bot. 

- Random_bot: Selects a random action every turn
- Rollout_bot: For every possible move from the immediate state, a finite number of games is sampled and the move with the highest expected turnout is selected.
  

mcts_vanilla.py and mcts_modified.py are where we wrote the functionalities of the bot to implement Monte Carlo Tree Search. Here's how the interface looks like:

- board.legal_actions(state): Returns the moves available in the state.
- board.next_state(state): Returns a new state constructed by applying action in state.
- board.is_ended(state): Returns True if the game has ended in state and False otherwise.
- board.current_player(state): Returns the index of the current player in state.
- board.points_values(state): Returns a dictionary of the score of each player. Will return none if the game is not ended.
- board.owned_boxes(state): Returns a string representation of the board state.
- board.display_action(action): Returns a string representation of the game action.

... in which board is a class name.

These functions will be called on the various stages of MCTS:
- traverse_nodes: Navigate the tree node
- Expand_leaf: Adding a new MCTSNode to the tree
- Rollout: Simulating the remainder of the game

- Goal of mcts_vanilla.py: Beat Rollout_bot most of the time for a tree size of 1000 nodes.
- Goal of mcts_modified.py: Beat Rollout_bot most of the time for a tree size of 1000 nodes using our unique heuristic approach.

## MODIFICATION OF MCTS_MODIFIED.PY

In our modifications to 'mcts_modified.py', we focused on enhancing the performance by adding a heuristic approach during the rollout phase. We introduced the 'heuristic_choice' function, which uses the 'next_move' function to score possible moves. The 'heuristic_choice' function iterates through all potential moves, evaluates each one, and selects the move with the highest score. The 'next_move' function assigns scores based on specific criteria: it gives a high score of 10 if the move results in a win for the bot, a score of 5 if the move blocks the opponent's win, and a score of 1 for any other move. This heuristic helps the program by making the bot prioritize moves that lead to immediate wins or prevent the opponent from winning, thus making the bot smarter and more effective.

## EXPERIMENTS

Experiment 1: 
- Two versions of MCTS bot played each other
- Player 1 fixed at 100 nodes/tree
- Player 2 has 4 different sizes and plays 100 games

Experiment 2:
- 3 sets of 100 games where mcts_modified plays against mcts_vanilla, each with a tree size of 1000 nodes

## References

# Helped with the structure and logic
https://ai-boson.github.io/mcts/ 

# Helped with the general logistics of the algorithm
https://www.youtube.com/watch?v=UXW2yZndl7U&t=352s&pp=ygUObWN0cyBhbGdvcml0aG0%3D




