from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point] # ParkingState is the positions the cars is in, which is a tuple of points

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the slot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()

        # the initial state: where each car is in the initial state -> cars attribute which refers to state (positions) of cars 
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        
        # state: Tuple[Point]     -> where the cars now              
        # slots: Dict[Point, int] -> where the cars should be
        
        # check if all cars in current state is in their own slots
        # check if all current state slots are in the expected slots, and each car is in its own expected slot
        # if at least one is not in its own slot, it will return false
        
        # loop over the current state (current cars positions)
        for i in range(len(state)): 

            # for each current car position, check if this position is an expected slot 
            if state[i] in self.slots:  # a slot
                
                # if this position is an expected slot, check if it is my own expected slot or not
                if self.slots[state[i]] != i: # but not mine
                    return False
                
            else: # not evan a slot
                return False
            
        return True

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()

        # list of the posible actions for the current state
        possible_actions: List[ParkingAction] = []

        # loop over the current state (current cars positions)
        for i in range(len(state)): 

            # check for each possible direction of the car to move (right, left, up, down)
            for dir in Direction:
                
                # try to move in the current direction by summing the current position and the direction vector
                new_position = state[i] + dir.to_vector()

                # check if this new position is available to the car to be in (not a wall which means in passages, there is not another car in it)
                if new_position in self.passages and new_position not in state:
                    possible_actions.append((i,dir))

        return possible_actions

    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()

        # action contains car index and direction
        # new_position = state[i] + dir.to_vector()
        # get the new position by summing the current position and the direction vector
        new_position =  state[action[0]] + action[1].to_vector()

        # convert tuple to list to be able to change it 
        updated_state = list(state) 

        # update the position of the car 
        updated_state[action[0]] = new_position

        state = tuple(updated_state) # convert back to tuple 
        
        return state


    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        
        cost = 0

        # get the new position of the car
        new_position =  state[action[0]] + action[1].to_vector()

        # check if this new position is the dedicated slot of any car but me, add 100
        # add cost based on ranking: A->26, B->25, ... , z->0
        
        if new_position in self.slots: # a slot 
            if self.slots[new_position] != action[0]: # but not mine
                cost += 100
        
        cost += (26 - action[0])

        return cost





    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
