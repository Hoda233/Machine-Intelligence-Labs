from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list
'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # utils.NotImplemented()

    ascii_offset: int = ord('a')

    list_count: List[int] = []

    # try all possible shifts
    for i in range(26):

        # decipher the cipher text (except spaces)
        plaintext: str = ""
        for s in range(len(ciphered)):
            if ciphered[s] != ' ':
                plaintext += chr((ord(ciphered[s]) - i - ascii_offset) % 26 + ascii_offset) 
            else:
                plaintext += " "

        
        # calculate number of words not in the dictionary
        plaintext_words: list[str] = plaintext.split()
        dictionary_words: set(str) = set(dictionary)
        count: int = sum(word not in dictionary_words for word in plaintext_words)
        list_count.append(count)

    # get results
    final_count: int = min(list_count)
    final_shift: int = list_count.index(min(list_count))

    # decipher with the shift which gives the least number of words not in dictionary
    final_plaintext: str = ""
    for s in range(len(ciphered)):
        if ciphered[s] != ' ':
            final_plaintext += chr((ord(ciphered[s]) - final_shift - ascii_offset) % 26 + ascii_offset) 
        else:
            final_plaintext += " "

    return(final_plaintext, final_shift, final_count)


