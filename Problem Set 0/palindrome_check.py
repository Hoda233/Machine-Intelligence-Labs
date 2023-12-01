import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    new_string: str = string.lower()

    length: int = len(new_string)-1
    
    for i in range(length): 
        if new_string[i] != new_string[length - i]:
            return False
    return True


