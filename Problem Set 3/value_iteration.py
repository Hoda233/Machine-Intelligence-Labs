from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()
        
        # if the state is terminal, return 0
        if self.mdp.is_terminal(state):
            return 0
        
        # U(s) = max(a) [ sum(s') [ P(s'|s,a)[R(s,a,s') + γU(s')] ] ]
        # U(s) = max( sum( P(s'|s,a)[R(s,a,s') + γU(s')] ] for s' in successors) for a in actions) 
        # where γ: discount factor
        utility = max(sum(self.mdp.get_successor(state,action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)) for action in self.mdp.get_actions(state))
        
        return utility
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # NotImplemented()

        # apply a single utility update
        updated_utilities = {state: self.compute_bellman(state) for state in self.mdp.get_states()}

        # get the max absolute utility change 
        max_utility_change = max(abs(updated_utilities[state] - self.utilities[state]) for state in self.mdp.get_states())
        
        # update the utilities
        self.utilities = {state: updated_utilities[state] for state in self.mdp.get_states()}

        # if the utilities has converged (the maximum utility change is less or equal the tolerance)
        if max_utility_change <= tolerance:
            return True
        return False
    
    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        # NotImplemented()

        # continue in training while iterations is None (not determined) or current iteration < determined number of iterations
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update(tolerance):
                break
        return iteration
            
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()
        
        # If the state is terminal, return None
        if self.mdp.is_terminal(state):
            return None   

        # get the best action to take from the current state with max utility of the successors
        # max ( P(s'|s,a)[R(s,a,s') + γU(s')] for s' in successors)
        action = max(self.mdp.get_actions(state), key = lambda action: sum(self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)))

        return action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
