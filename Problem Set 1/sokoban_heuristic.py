from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use

def calculate_manhattan_distance(crate, goal):
    return abs(crate.x - goal.x) + abs(crate.y - goal.y)

def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # NotImplemented()

    
    # total distance
    distance = 0

    # penalty for deadlocks to be avoided in exploration because it will have high heuristic value
    penalty = float('inf')

    # just for simplicity
    goals = state.layout.goals
    crates = state.crates
    walkable = state.layout.walkable
    width = state.layout.width
    height = state.layout.height
    
    # check if the current state is a goal state
    if goals == crates:
        return 0

    # loop over all crates
    for crate in crates:
        
        # check if the current crate is already in a goal position
        if crate in goals:
            continue
        
        # check for deadlocks 

        # check for corners 
        # (left of right) and (up or down)

        '''
        ##    ##    #$   $#
        #$    $#    ##   ##
        '''
        if (
            (Point(crate.x + 1, crate.y) not in walkable or Point(crate.x - 1, crate.y) not in walkable) and 
            (Point(crate.x , crate.y + 1) not in walkable or Point(crate.x, crate.y - 1) not in walkable)
        ):
            return penalty   
        
        # check for adjacent crates and it is at start or end (next to border) 
        # trapped by crate and border
        '''
        start (crate me) or (crate me) end

        start (me crate) or (me crate) end
        
        start
        (crate
        me)
        or
        (crate
        me)
        end

        start
        (me
        crate)
        or
        (me
        crate)
        end

        '''
        if (
            Point(crate.x - 1, crate.y) in crates and (crate.x - 2 == 0 or crate.x + 1 == width - 1) or
            Point(crate.x + 1, crate.y) in crates and (crate.x - 1 == 0 or crate.x + 2 == width - 1) or
            Point(crate.x, crate.y - 1) in crates and (crate.y - 2 == 0 or crate.y + 1 == height - 1) or
            Point(crate.x, crate.y + 1) in crates and (crate.y - 1 == 0 or crate.y + 2 == height - 1)
        ):
            return penalty  
        
        # check if crate next to border and no goals can be reached
        '''
        start me (can't move horizontally) and no goals vertically on same column
        me end and no goals vertically on same column

        srart
        me 
        (can't move vertically)
        and no goals horizontally on same row

        me
        end 
        (can't move vertically)
        and no goals horizontally on same row
        '''
            
        if(
            (crate.x + 1 == width - 1  and len([goal for goal in goals if goal.x == width - 2]) == 0) or
            (crate.x == 1              and len([goal for goal in goals if goal.x == 1]) == 0) or
            (crate.y - 1 == height - 1 and len([goal for goal in goals if goal.y == height - 2]) == 0) or
            (crate.y == 1              and len([goal for goal in goals if goal.y == 1]) == 0)
        ):
            return penalty 

        # check if trapped at least 3 sides 
        # wall or crate or border 
        sides = 0
        if (Point(crate.x - 1, crate.y) not in walkable or Point(crate.x - 1, crate.y) in crates or crate.x - 1 == 0):
            sides += 1
        if(Point(crate.x + 1, crate.y) not in walkable or Point(crate.x + 1, crate.y) in crates or crate.x + 1 == width - 1):
            sides += 1
        if(Point(crate.x , crate.y + 1) not in walkable or Point(crate.x, crate.y + 1) in crates or crate.y - 1 == 0):
            sides += 1
        if(Point(crate.x , crate.y - 1) not in walkable or Point(crate.x, crate.y - 1) in crates or crate.y + 1 == height - 1):
            sides += 1

        if(sides >=3):
            return penalty

        
        # no deadlocks -> calculate the distance between crate and all goals 
        # then get the distance to the closest goal and add it to the total distance
        min_dist = min(abs(crate.x - goal.x) + abs(crate.y - goal.y) for goal in goals)
        distance += min_dist

    return distance