
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
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """ 
    while not board.is_ended(state) and not node.untried_actions: # while the node is not terminated and there is no untried node left 
        
        best_child = None
        best_value = float("-inf") #infinitely negative
        
        for child in node.child_nodes.values():

            #maybe not necessary
            is_opponent = (board.current_player(state) != bot_identity)

            
            ucbValue = ucb(child, is_opponent) #greater the  better
            if ucbValue > best_value:
                best_value = ucbValue
                best_child = child
        node = best_child
        state = board.next_state(state, node.parent_action) # the action taken to transition from the parent to the current node
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
    #reference: https://ai-boson.github.io/mcts/

    action = node.untried_actions.pop() 
    next_state = board.next_state(state, action) 
    child_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    "def __init__(self, parent=None, parent_action=None, action_list=[]):"
    node.child_nodes[action]=child_node  #connecting the node to the tree

    return child_node, next_state


def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        all_possible_action = board.legal_actions(state) # gets all the possible action from the current state of the game

        action = choice(all_possible_action) #select one action from all possible actions

        state = board.next_state(state, action)

    return state


def backpropagate(node: MCTSNode, won: bool):
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
    """ Calcualtes the UCB value for the given node from the perspective of the bot

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
    # checks if state is a win state for identity_of_bot
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
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # ...
        selection = traverse_nodes(node, board, state, bot_identity,)
        child_node, child_state = selection

        if not board.is_ended(child_state):
            child_node, child_state = expand_leaf(child_node, board, child_state)
           

        future_state = rollout(board, child_state)
        winner = is_win(board, future_state, bot_identity)
        backpropagate(child_node, winner)



    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node)
    
    print(f"Action chosen: {best_action}")
    return best_action
