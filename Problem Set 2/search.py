import math
from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    
    # get the turn of the player to start the game
    start_agent = game.get_turn(state)

    def get_value(state,depth):
        
        # check if this is a terminal state, end the game and return the value of the utility 
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[start_agent], None
        
        # if it is in the maximum depth, return the heuristic value
        if depth == max_depth:
            return heuristic(game, state, start_agent), None
        
        # get the current player turn 
        agent = game.get_turn(state)

        # if the turn is 0, then it is a max node
        if agent == 0:
            return max_value(state, depth)
        else:
            return min_value(state, depth)
        

    def min_value(state, depth):
        
        # initiate the min value with positive infinity
        v_min = math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1)[0]
            # if the successor_value less or equal than min value, update the min value and the action to take
            if successor_value <= v_min: 
                v_min = successor_value 
                taken_action = action
                
        return v_min , taken_action

    def max_value(state, depth):

        # initiate the max value with negative infinity
        v_max = -math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1)[0]
            # if the successor_value more than min value, update the min value and the action to take
            if successor_value > v_max: 
                v_max = successor_value 
                taken_action = action

        return v_max , taken_action
    
    return get_value(state, 0)


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()

    # get the turn of the player to start the game
    start_agent = game.get_turn(state)

    def get_value(state, depth, alpha, beta):

        # check if this is a terminal state, end the game and return the value of the utility 
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[start_agent], None

        # if it is in the maximum depth, return the heuristic value
        if depth == max_depth:
            return heuristic(game, state, start_agent), None

        # get the current player turn 
        agent = game.get_turn(state)

        # if the turn is 0, then it is a max node
        if agent == 0:
            return max_value(state, depth, alpha, beta)
        else:
            return min_value(state, depth, alpha, beta)
        

    def min_value(state, depth, alpha, beta):

        # initiate the min value with positive infinity
        v_min = math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1, alpha, beta)[0]
            # if the successor_value less or equal than min value, update the min value and the action to take            
            if successor_value <= v_min: 
                v_min = successor_value 
                taken_action = action

            # pruning check: if min value less or equal alpha, then prune the branch
            if v_min <= alpha: 
                return v_min , taken_action

            # if not so update the beta
            beta = min(beta, v_min)
                
        return v_min , taken_action

    def max_value(state, depth, alpha, beta):

        # initiate the max value with negative infinity
        v_max = -math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1, alpha, beta)[0]
            # if the successor_value more than min value, update the min value and the action to take
            if successor_value > v_max: 
                v_max = successor_value 
                taken_action = action
                        
            # pruning check: if max value more or equal than beta, then prune the branch
            if v_max >= beta: 
                return v_max , taken_action
            
            # if not so update the alpha
            alpha = max(alpha, v_max)

        return v_max , taken_action
    
    return get_value(state, 0, -math.inf, math.inf)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()

    # get the turn of the player to start the game
    start_agent = game.get_turn(state)

    def get_value(state, depth, alpha, beta):
        
        # check if this is a terminal state, end the game and return the value of the utility 
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[start_agent], None
        
        # if it is in the maximum depth, return the heuristic value
        if depth == max_depth:
            return heuristic(game, state, start_agent), None
        
        # get the current player turn 
        agent = game.get_turn(state)

        # if the turn is 0, then it is a max node
        if agent == 0:
            return max_value(state, depth, alpha, beta)
        else:
            return min_value(state, depth, alpha, beta)
        

    def min_value(state, depth, alpha, beta):

        # initiate the min value with positive infinity
        v_min = math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        
        # sort the actions ascendencly based on their heuristic
        actions_states.sort(key = lambda x: heuristic(game, x[1], 0))

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1, alpha, beta)[0]
            # if the successor_value less or equal than min value, update the min value and the action to take                        
            if successor_value <= v_min: 
                v_min = successor_value 
                taken_action = action
            
            # pruning check: if min value less or equal alpha, then prune the branch
            if v_min <= alpha: 
                return v_min , taken_action
            
            # if not so update the beta
            beta = min(beta, v_min)
                
        return v_min , taken_action

    def max_value(state, depth, alpha, beta):

        # initiate the max value with negative infinity
        v_max = -math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        
        # sort the actions descendengly based on their heuristic
        actions_states.sort(key = lambda x: heuristic(game, x[1], 0), reverse=True)

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1, alpha, beta)[0]
            # if the successor_value more than min value, update the min value and the action to take            
            if successor_value > v_max: 
                v_max = successor_value 
                taken_action = action
            
            # pruning check: if max value more or equal than beta, then prune the branch
            if v_max >= beta: 
                return v_max , taken_action
            
            # if not so update the alpha            
            alpha = max(alpha, v_max)

        return v_max , taken_action
    
    return get_value(state, 0, -math.inf, math.inf)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()

    # get the turn of the player to start the game
    start_agent = game.get_turn(state)

    def get_value(state, depth):

        # check if this is a terminal state, end the game and return the value of the utility 
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[start_agent], None
        
        # if it is in the maximum depth, return the heuristic value       
        if depth == max_depth:
            return heuristic(game, state, start_agent), None
        
        # get the current player turn 
        agent = game.get_turn(state)

        # if the turn is 0, then it is a max node
        if agent == 0:
            return max_value(state, depth)
        else:
            return expected_value(state, depth)
        
    def expected_value(state, depth):
        
        # initiate the expected value with 0
        v_exp = 0

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1)[0]

            # sum the successor values and return their average
            v_exp += successor_value
        return v_exp/len(actions_states), None


    def max_value(state, depth):
        
        # initiate the max value with negative infinity
        v_max = -math.inf

        # initiate the action to take
        taken_action = None

        # get possible actions and states of the successors for each possible action for the current state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # for each action of the successors, get the value of the successor
        for action , state in actions_states:
            successor_value = get_value(state, depth + 1)[0]
            # if the successor_value more than min value, update the min value and the action to take
            if successor_value > v_max: 
                v_max = successor_value 
                taken_action = action

        return v_max , taken_action
    
    return get_value(state, 0)