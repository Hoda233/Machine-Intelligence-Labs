from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

'''
In all of the following functions:

    frontier: data structure to store the nodes while searching

    explored: set to store the explored nodes

    problem.is_goal(state): function to check whether the given state is a goal state or not

    problem.get_actions(state): function to get all possible actions can be done on the given state

    problem.get_successor(state, action): function to get the next state given the current state and an action applied on it

    problem.get_cost(state, action): function to get the cost given the current state and an action applied on it
'''

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    '''
    Breadth First Search (BFS) is a graph algorithm that explores a graph level by level. 
    It uses a queue to visit all children of a node before moving on to their children.
    It returns the shallowest path to the goal.
    '''

    # define the frontier -> Queue (FIFO) in BFS algorithm
    frontier = deque()
    
    # define the explored set
    explored = set()

    # add the first node in frontier (initial state, empty list for actions)
    frontier.append((initial_state, []))

    # loop while frontier is not empty
    while frontier:

        # pop the left/first added node in frontier  
        state, path = frontier.popleft()

        # check if this state is a goal, then return the path from the initial state to the final state
        if problem.is_goal(state):
            return path
        
        # if this state is not a goal, add it to the explored set
        explored.add(state)

        # get states in the nodes which in frontier
        frontier_set = set([s[0] for s in frontier])
        
        # loop over possible actions for the current state 
        for action in problem.get_actions(state):
            
            # get the next state based on the action
            new_state = problem.get_successor(state, action)

            # if this new state is not explored yet and not in frontier, explore it 
            if new_state not in explored and new_state not in frontier_set:
                        
                        # append this action to the path 
                        new_path = path + [action]
                        
                        # check if this new state is a goal
                        if problem.is_goal(new_state):
                            return new_path
                        
                        # add the new node (new_state, new_path) to frontier
                        frontier.append((new_state, new_path))
    return None   


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    '''
    Depth First Search (DFS) is a graph algorithm that explores as far as possible 
    along each branch before backtracking if no goal found. 
    It uses a stack to store the nodes. It returns the deepest path to the goal.
    '''

    # define the frontier -> Stack (LIFO) in DFS algorithm
    frontier = deque()

    # define the explored set
    explored = set()

    # add the first node in frontier (initial state, empty list for actions)
    frontier.append((initial_state, []))

    # loop while frontier is not empty
    while frontier:

        # pop the top/newly added node in frontier  
        state, path = frontier.pop()
        
        # if the current state is not explored yet
        if state not in explored:
            
            # check if this new state is a goal
            if problem.is_goal(state):
                return path
            
            # if this state is not a goal, add it to the explored set
            explored.add(state)

            # loop over possible actions for the current state 
            for action in problem.get_actions(state):
                
                # get the next state based on the action
                new_state = problem.get_successor(state, action)
                        
                # append this action to the path 
                new_path = path + [action]
                
                # add the new node (new_state, new_path) to frontier
                frontier.append((new_state, new_path))
    return None  
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    '''
    Uniform Cost Search (UCS) is a graph search algorithm that finds the lowest cost path from a start node to a goal node. 
    Unlike BFS, UCS takes into account the cost associated with each edge. It uses a priority queue 
    to always explore the path with the lowest accumulative path cost, ensuring an optimal solution is found.
    '''

    # define the frontier -> Priority Queue based on lowest g function (cummulative path cost) 
    frontier = []
    heapq.heapify(frontier)

    # define the explored set
    explored = set()

    # store each state and its path cost
    state_cost = {initial_state: 0}
    
    # cummulative path cost
    path_cost = 0

    # variable to store unique value for each iteration 
    # it is used for if the queue has two nodes with same priority, then choose the first added one
    unique_id = 0

    # push the node to frontier
    heapq.heappush(frontier,(path_cost, unique_id ,initial_state, []))

    # loop while frontier is not empty
    while frontier:
            
        # pop the highest priority / lowest value node in frontier
        path_cost, _, state, path = heapq.heappop(frontier)

        # if the current state is not explored yet
        if state not in explored:

            # check if this new state is a goal
            if problem.is_goal(state):
                return path
            
            # if this state is not a goal, add it to the explored set
            explored.add(state)

            # loop over possible actions for the current state 
            for action in problem.get_actions(state):

                # get the next state based on the action
                new_state = problem.get_successor(state, action)

                # if the current state is not explored yet
                if new_state not in explored:

                    # get cummulative cost of the new state
                    new_path_cost = path_cost + problem.get_cost(state, action) 

                    # if the new state has lower cost than current state
                    if new_state not in state_cost or new_path_cost < state_cost[new_state]:
                        
                        # update the new state with its cummulative path cost
                        state_cost[new_state] = new_path_cost

                        # append this action to the path 
                        new_path = path + [action]
                        
                        # update the id
                        unique_id += 1

                        # push the new node into frontier
                        heapq.heappush(frontier,(new_path_cost, unique_id ,new_state, new_path))
                        
                        

    return None  


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    '''
    A* Search is a graph search algorithm that finds the path with the lowest total cost
    (total cost = cummulative path cost + heuristic value)
    (f(n) = g(n) + h(n))
    which takes advantage of both Uniform Cost Search and Best First Search strength points, 
    so it is optimal and efficient.
    '''

    # define the frontier -> Priority Queue based on lowest f function (cummulative path cost + heuristic) 
    frontier = []
    heapq.heapify(frontier)

    # define the explored set
    explored = set()
    
    # store each state and f value
    state_cost = {initial_state: 0}

    # cummulative path cost
    path_cost = 0

    # get heuristic value of the initial state 
    heuristic_cost = heuristic(problem, initial_state)

    # get f = g + h
    total_cost = path_cost + heuristic_cost

    # variable to store unique value for each iteration 
    # it is used for if the queue has two nodes with same priority, then choose the first added one
    unique_id = 0
    
    # push the node to frontier
    heapq.heappush(frontier,(total_cost, unique_id ,initial_state, []))

    # loop while frontier is not empty
    while frontier:
            
            # pop the highest priority / lowest value node in frontier
            total_cost, _ , state, path = heapq.heappop(frontier)
            
            # if the current state is not explored yet
            if state not in explored:

                # check if this new state is a goal
                if problem.is_goal(state):
                    return path
                
                # if this state is not a goal, add it to the explored set           
                explored.add(state)

                # loop over possible actions for the current state 
                for action in problem.get_actions(state):

                    # get the next state based on the action
                    new_state = problem.get_successor(state, action)

                    # if the current state is not explored yet
                    if new_state not in explored:
                        
                        # calculate the total cost = cummulative path cost + heuristic value
                        path_cost = total_cost - heuristic(problem, state)
                        new_path_cost = path_cost + problem.get_cost(state, action) 
                        new_total_cost = new_path_cost + heuristic(problem, new_state)

                        # if the new state has lower total cost than current state
                        if new_state not in state_cost or new_total_cost < state_cost[new_state]:
                            
                            # update the new state with its new total cost
                            state_cost[new_state] = new_total_cost 

                            # append this action to the path 
                            new_path = path + [action]
                            
                            # update the id                            
                            unique_id += 1
                            
                            # push the new node into frontier
                            heapq.heappush(frontier,(new_total_cost, unique_id ,new_state, new_path))
                            
    return None  

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    '''
    Best First Search is a graph search algorithm that finds the path with the lowest heuristic value
    which estimates how near we are from the goal. It is not necessarily guarantee an optimal solution 
    but is generally faster than other uninformed search algorithms.
    '''

    # define the frontier -> Priority Queue based on lowest h function (hueristic) 
    frontier = []
    heapq.heapify(frontier)

    # define the explored set
    explored = set()

    # get heuristic value of the initial state 
    heuristic_cost = heuristic(problem, initial_state)

    # store each state and its heuristic value
    state_cost = {initial_state: heuristic_cost}
    
    # variable to store unique value for each iteration 
    # it is used for if the queue has two nodes with same priority, then choose the first added one
    unique_id = 0

    # push the node to frontier
    heapq.heappush(frontier,(heuristic_cost, unique_id ,initial_state, []))

    # loop while frontier is not empty
    while frontier:
            
            # pop the highest priority / lowest value node in frontier
            _, _ , state, path = heapq.heappop(frontier)

            # if the current state is not explored yet
            if state not in explored:

                # check if this new state is a goal
                if problem.is_goal(state):
                    return path
                
                # if this state is not a goal, add it to the explored set           
                explored.add(state)

                # loop over possible actions for the current state 
                for action in problem.get_actions(state):
                    
                    # get the next state based on the action
                    new_state = problem.get_successor(state, action)
                    
                    # if the current state is not explored yet
                    if new_state not in explored:
                        
                        # get heuristic value of the new state 
                        new_heuristic_cost =  heuristic(problem, new_state)
                                    
                        # if the new state has lower heuristic value than current state
                        if new_state not in state_cost or new_heuristic_cost < state_cost[new_state]:
                                                    
                            # update the new state with its new heuristic value
                            state_cost[new_state] = new_heuristic_cost 

                            # append this action to the path 
                            new_path = path + [action]
                            
                            # update the id
                            unique_id += 1

                            # push the new node into frontier
                            heapq.heappush(frontier,(new_heuristic_cost, unique_id ,new_state, new_path))
                            
    return None  