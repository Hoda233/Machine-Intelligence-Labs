# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        # stochastic environment (with noise)
        # discount_factor = 0.9 close to 1
        "noise": 0.2,
        "discount_factor": 0.9,
        "living_reward": -2
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        # stochastic environment (with noise)
        # discount_factor = 0.2 close to 0, future rewards are considered insignificant
        "noise": 0.2,
        "discount_factor": 0.2,
        "living_reward": -2
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        # stochastic environment (with noise)
        # discount_factor = 1, immediate rewards as important as future rewards
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        # stochastic environment (with noise)
        # discount_factor = 1, immediate rewards as important as future rewards
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        # deterministic environment (without noise)
        # discount_factor = 1, immediate rewards as important as future rewards
        # living_reward is more than terminal state rewards
        "noise": 0.0,
        "discount_factor": 1,
        "living_reward": 20
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        # deterministic environment (without noise)
        # discount_factor = 1, immediate rewards as important as future rewards
        # living_reward is less than terminal state rewards
        "noise": 0.0,
        "discount_factor": 1,
        "living_reward": -20
    }