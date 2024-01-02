from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed) # Initialize the random generator using the seed
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        # NotImplemented()

        # The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
        self.snake = [Point(self.width // 2, self.height // 2)]
        self.direction = Direction.LEFT

        # Generate an apple in a random position
        self.apple = self.generate_random_apple()
        
        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # TODO add your code here
        # a snake can wrap around the grid
        # NOTE: The action order does not matter
        # NotImplemented()

        # define a list for possible actions, and initiate it with the NONE direction 
        possible_actions = []
        possible_actions.append(Direction.NONE)

        # The action can not move the snake in the same direction 
        # The action can not move the snake in the opposite direction of its current direction.
        
        # so if right --> can't go right or left, and if left --> can't go left or right
        if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
            possible_actions.append(Direction.UP)
            possible_actions.append(Direction.DOWN)

        # Also if down --> can't go down or up, and if up --> can't go up or down
        if self.direction == Direction.DOWN or self.direction == Direction.UP:
            possible_actions.append(Direction.LEFT)
            possible_actions.append(Direction.RIGHT)
        
        return possible_actions
        

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # TODO Complete the following function
        # NotImplemented()

        done = False
        reward = 0

        # The head of the snake which is the first point of it
        head = self.snake[0]

        # observation1 = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        # print(observation1)
        # print('head: ', head)
        # print('action ', action)
        # print('snake: ', self.snake)
        
        # the updated head of the snake based on the taken action
        new_head = None

        # if no new action, just continue in the previous direction
        if action == Direction.NONE:
            action = self.direction
        
        # get the new head of the snake based on the direction where The snake can wrap around the grid
        if action == Direction.RIGHT:
            new_head = Point((head.x + 1) % self.width, head.y)
        elif action == Direction.UP:
            new_head = Point(head.x, (head.y - 1) % self.height)
        elif action == Direction.LEFT:
            new_head = Point((head.x - 1) % self.width, head.y)
        elif action == Direction.DOWN:
            new_head = Point(head.x, (head.y + 1) % self.height)

        # check if the snake bites itself (the snake head enters a cell occupied by its body)
        if new_head in self.snake[1:]:
            # if yes, you lose 
            done = True
            # Losing the game decreases the reward by 100.
            reward = -100
        else:
            # update the snake points by inserting this new head as the head 
            self.snake.insert(0, new_head)

            # check if the snake ate an apple
            if new_head == self.apple:
                # generate a new random apple if there is still possible empty points
                if len(self.snake) != self.width * self.height:
                    self.apple = self.generate_random_apple()

                # Eating an apple increases the reward by 1.
                reward += 1
            else:
                # snake didn't eat an apple, remove the tail (to still have the same length)
                self.snake.pop()

            # check if the snake body covers all of the level (there is no cell that is not occupied by the snake).
            if len(self.snake) == self.width * self.height:
                # if yes, you win
                done = True
                # Winning the game increases the reward by 100.
                reward += 100
            else:
                done = False

        # print('---snake: ', self.snake)

        # update the last direction with the taken action
        self.direction = action

        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        
        return observation, reward, done, {}

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]