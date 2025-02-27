from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        bot_identity: The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node
    """ 
    while not board.is_ended(state) and not node.untried_actions:
        best_child = None
        best_value = float("-inf")
        for child in node.child_nodes.values():
            is_opponent = (board.current_player(state) != bot_identity)
            ucb_value = ucb(child, is_opponent)
            if ucb_value > best_value:
                best_value = ucb_value
                best_child = child
        node = best_child
        state = board.next_state(state, node.parent_action)
    return node, state

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node
    """
    action = node.untried_actions.pop()
    next_state = board.next_state(state, action)
    child_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    node.child_nodes[action] = child_node
    return child_node, next_state

def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder with a heuristic.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state
    """
    while not board.is_ended(state):
        possible_moves = board.legal_actions(state)
        action = heuristic_choice(board, state, possible_moves)
        state = board.next_state(state, action)
    return state

def heuristic_choice(board: Board, state, possible_moves):
   
    best_action = None
    highest_score = float('-inf')
    for move in possible_moves:
        move_score = next_move(board, state, move)
        if move_score > highest_score:
            highest_score = move_score
            best_action = move
    return best_action

def next_move(board: Board, state, move):

    next_state = board.next_state(state, move)
    if board.points_values(next_state) == {1: 1, 2: -1}:
        return 10  # Winning move
    if board.points_values(next_state) == {1: -1, 2: 1}:
        return 5  # Blocking opponent's win
    return 1  # any other move



def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    """
    current_node = node
    while current_node is not None:
        current_node.visits += 1
        if won:
            current_node.wins += 1
        current_node = current_node.parent

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calculates the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    nv = node.visits
    if not nv:
        return float('inf')
    Q = node.wins / nv
    N = node.parent.visits if node.parent else 1
    ucb_val = Q + sqrt(2 * log(N) / nv)
    return -ucb_val if is_opponent else ucb_val

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    """
    best_child = None
    best_score = -float('inf')
    for child in root_node.child_nodes.values():
        score = child.wins / child.visits if child.visits > 0 else 0
        if score > best_score:
            best_score = score
            best_child = child
    return best_child.parent_action if best_child else None

def is_win(board: Board, state, identity_of_bot: int):
    """ Checks if the state is a win state for identity_of_bot

    Args:
        board: The game setup.
        state: The state of the game.
        identity_of_bot: The bot's identity, either 1 or 2

    Returns:
        bool: True if the state is a win state for the bot, False otherwise
    """
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state
    """
    bot_identity = board.current_player(current_state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        node, state = traverse_nodes(node, board, state, bot_identity)
        if not board.is_ended(state):
            node, state = expand_leaf(node, board, state)
        end_state = rollout(board, state)
        won = is_win(board, end_state, bot_identity)
        backpropagate(node, won)

    best_action = get_best_action(root_node)
    print(f"Action chosen: {best_action}")
    return best_action
