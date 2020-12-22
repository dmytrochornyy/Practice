# Name          : Chornyy Dmytro
# Collaborators : None
# Time spent    : 2 evenings 
# I`m not sure in last tast the most

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = "*"

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, WILDCARD: 0
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    # Making list of lowercase letters from our word
    word_lst = list(word.lower())
    # Calculate first component
    first_component = sum(list(map(lambda x: SCRABBLE_LETTER_VALUES[x], word_lst)))
    # Calculate second component
    second_component = max(1, 7 * len(word_lst) - 3 * (n - len(word_lst)))
    # Return product
    return first_component * second_component
    
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    hand: dictionary (string -> int)
    """
    print("Current hand: ", end="")
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand[WILDCARD] = 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # Making copy of hand
    new_hand = hand.copy()
    for letter in word.lower():
        if letter in new_hand.keys():
            if new_hand[letter] == 1:
                # If there are only one letter left - delete letter from hand
                del new_hand[letter]
            else:
                # If letter in our hand - reduce one from letter counter
                new_hand[letter] -= 1
    return new_hand
        

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    # Making a list with all of our letters in hand, in format - ["h", "e", "l", "l", "o"]
    hand_lst = list("".join([k * v for k, v in hand.copy().items()]))
    # Checking if word can be made from our letters
    for letter in word.lower():
        if letter in hand_lst:
            hand_lst.remove(letter)
        else:
            return False

    # Checking if we can find word in word_list
    if WILDCARD in word.lower():
        # Checking if we can find word with replaceing "*" with vowels
        for vowel in VOWELS:
            if word.replace(WILDCARD, vowel) in word_list:
                return True
        return False
    # Or just looking for word in list
    elif word.lower() in word_list:
        return True
    return False

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(hand.values())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
      returns: the total score for the hand
      
    """
    # Intitiate score
    score = 0
    # As long as there are still letters left in the hand:
    while hand != {}:
        # Display the hand
        display_hand(hand)
        # Ask user for input
        word = input("Enter word, or “!!” to indicate that you are finished: ")
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            print()
            break

            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Updated total score
                word_score = get_word_score(word, calculate_handlen(hand))
                score += word_score
                # Tell the user how many points the word earned
                print(f"“{word}” earned {word_score} points. Total: {score} points")

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("This is not a valid word. Please choose another word.")
                
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
            print()
            

    # Game is over (user entered '!!' or ran out of letters),
    if hand == {}:
        print("Ran out of letters")
    # so tell user the total score
    print(f"Total score for this hand: {score} points")
    # Print hand separator
    print("--------")
    # Return the total score as result of function
    return score

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # Checking if letter in our hand
    if letter not in hand.keys():
        return hand
    # Making set of possible to add in hand
    posible_letters = list(list(VOWELS+CONSONANTS) - hand.keys())
    # Choose new letter
    new_letter = random.choice(posible_letters)
    # Savind specific index (to leave replased letter onto previous place)
    index_in_dict = list(hand).index(letter)
    # Making new hand in form of list of tuples
    list_of_pairs = list(hand.items())
    # Replase tuple with old letter with tuple with new
    list_of_pairs[index_in_dict] = (new_letter, hand[letter])
    #Return new hand in a form of dictionary
    return dict(list_of_pairs)
    
def ask_for_num_of_hands():
    """Ask player for number of hands player want to play

    Returns:
        integer: number of hands
    """
    try:
        # Ask player for number
        num = int(input("Enter total number of hands: "))
        if num < 1:
            raise ValueError
        # If it`s positive integer - return it
        return num
    except ValueError:
        # If it`s not positive integer - don`t return it
        print("Incorrect input. Please, enter positive integer")
        # And ask again
        return ask_for_num_of_hands()

def ask_substitution_letter():
    """Ask player if substitution of letter if wanted, and asks letter if so.

    Returns:
        tuple: First position boolean - True if substitution is wanted 
    """
    # Asks if substitution is wanted
    inp = input("Would you like to substitute a letter? ")
    # If isn`t wanted return False
    if inp.lower() == 'no':
        return (False, None)
    # If is wanted: asks for letter
    elif inp.lower() == "yes":
        inp_letter = input("Which letter would you like to replace: ")
        return (True, inp_letter)
    # If input is not correct - ask again
    else:
        print("Incorrect input. Please, enter 'yes' or 'no'.")
        return ask_substitution_letter()

def regame(hand_score, is_regame_availible, hand, word_list):
    """Makes regame if is_regame_availivle is true

    Args:
        hand_score (int): previous hand score
        is_regame_availible (bool): if regame is availible
        hand (dict): current hand
        word_list (list): list of correct words
    Returns:
        tuple: first: integer -greater of two scores - hand_score, of hand_score of new game
               second: boolean - new value of is_regame_availible
    """
    # If regame is not availible - just return previous game score
    if not is_regame_availible:
        return (hand_score, False)
    # Asking player
    inp = input("Would you like to replay the hand? ")
    # If player want to regame
    if inp.lower() == "yes":
        # Play new game with previous hand
        new_score = play_hand(hand, word_list)
        # Return max of both scores
        return (max(new_score, hand_score), False)
    # If player doesn`t want to regame
    elif inp.lower() == "no": 
        return (hand_score, is_regame_availible)
    # If input is incorrect - try again
    else:
        print("Incorrect input. Please, enter 'yes' or 'no'.")
        return regame(hand_score, is_regame_availible, hand, word_list)

def play_game(word_list):
    """
    Allow the user to play a series of hands

    word_list: list of lowercase strings
    """
    # Asking for num of hands
    num_of_hands = ask_for_num_of_hands()
    # Initiating total score
    total_score = 0
    # Initiating availible try to regame
    is_regame_availible = True
    for _ in range(num_of_hands):
        # Dealing new hand
        hand = deal_hand(HAND_SIZE)
        # Display current hand
        display_hand(hand)
        # Asking if substitution is needed, if True - replase letter
        tuple_substitution = ask_substitution_letter()
        if tuple_substitution[0]:
            hand = substitute_hand(hand, tuple_substitution[1])
        print()
        # Play hand
        hand_score = play_hand(hand, word_list)
        # Asking for regame
        hand_score, is_regame_availible = regame(hand_score, is_regame_availible, hand, word_list)
        # Adding hand score to total
        total_score += hand_score
    # Print total score
    print(f"Total score over all hands: {total_score}")

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)