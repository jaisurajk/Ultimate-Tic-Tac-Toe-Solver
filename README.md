## Team members: 
    Daniel Villalon 
    Jaisuraj Kaleeswaran

## MODIFICATION OF MCTS_MODIFIED.PY

In our modifications to 'mcts_modified.py', we focused on enhancing the performanceby adding a heuristic approach during the rollout phase. We introduced the 'heuristic_choice' function, which uses the 'next_move' function to score possible moves. The 'heuristic_choice' function iterates through all potential moves, evaluates each one, and selects the move with the highest score. The 'next_move' function assigns scores based on specific criteria: it gives a high score of 10 if the move results in a win for the bot, a score of 5 if the move blocks the opponent's win, and a score of 1 for any other move. This heuristic helps the program by making the bot prioritize moves that lead to immediate wins or prevent the opponent from winning, thus making the bot smarter and more effective.

## References

# Helped with the structure and logic
https://ai-boson.github.io/mcts/ 

# Helped with the general logistics of the algorithm
https://www.youtube.com/watch?v=UXW2yZndl7U&t=352s&pp=ygUObWN0cyBhbGdvcml0aG0%3D




