# Problem Set 2, hangman.py
# Name: Сhornyy Dmytro
# Collaborators: Made by myself (Can help others with some ideas)
# Time spent: 1 evening at 11.4.2020

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    #looking for each letter from secret_word
    for i in secret_word:
      #if at least one letter is not guessed
      if i not in letters_guessed:
        return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    #making blank string
    guessed_word = ''

    for i in secret_word:
      #if we already know the letter - add it. If not - add "_ "
      if i in letters_guessed:
        guessed_word += i
      else:
        guessed_word +="_ "
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    #get alphabet
    available_letters = string.ascii_lowercase
    #delete each already known letter from alphabet
    for i in letters_guessed:
      available_letters = available_letters.replace(i, "")
    return available_letters
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    #printing hello message
    print("Welcome to the game Hangman!\nI am thinking of a word that is {0} letters long.".format(len(secret_word)))
    #create blank letters list, new set of guesses and warnings
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3

    #repeat game until there are guesses or until word is not guessed
    while (not is_word_guessed(secret_word, letters_guessed)) and (guesses_remaining > 0):
      #print message about guesses and available letters
      print("------------", 
        "You have {0} guesses left.".format(guesses_remaining),
        "Available letters: {0}".format(get_available_letters(letters_guessed)),
        sep="\n"
      )
      #input new letter
      letter = input("Please guess a letter: ").lower()

      #check letter for appropriate format
      if len(letter) == 1 and str.isalpha(letter) and not(letter in letters_guessed):
        #memorize that this letter is already named
        letters_guessed.append(letter)
        #if guess is good
        if letter in secret_word:
          print("Good guess: {0}".format(get_guessed_word(secret_word, letters_guessed)))
        #if guess is bad
        else:
          print("Oops! That letter is not in my word: {0}".format(get_guessed_word(secret_word, letters_guessed)))
          #subtract guess according to letter 
          if letter in "aeiou":
            guesses_remaining -= 2
          else:
            guesses_remaining -= 1
      #if letter is already named
      elif letter in letters_guessed:
        print("Oops! You've already guessed that letter. You now have {0} warnings: {1}".format(warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
      #if format is not appropriate
      else:
        #subtract warnings or guesses
        if warnings_remaining != 0:
          warnings_remaining -= 1
        else:
          guesses_remaining -=1
        print("Oops! That is not a valid letter. You have {0} warnings left: {1}".format(warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
    #cycle is end, so if user guessed
    if is_word_guessed(secret_word, letters_guessed):
      print(
        "------------",
        "Congratulations, you won! Your total score for this game is: {0}".format(guesses_remaining*len(set(secret_word))),
        sep="\n"
      )
    #if guesses ended
    else:
      print(
        "------------",
        "Sorry, you ran out of guesses. The word was {0}".format(secret_word),
        sep="\n"
      )




    



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    #delete all spaces, to work more convenient
    my_word = my_word.replace(" ", "")
    #check if len is same
    if len(my_word)!=len(other_word):
      return False
    else:
      for i in range(len(my_word)):
        #check if letters on same positions are different (except positions with"_")
        if my_word[i] != "_" and my_word[i] != other_word[i]:
          return False
      return True





def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    #creating boolean list with length of wordlist( if match = True), than apply this list to wordlist and print it
    print(*[i for (i, v) in zip(wordlist, list(map(lambda x: match_with_gaps(my_word, x), wordlist))) if v])
    



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    #printing hello message
    print("Welcome to the game Hangman!\nI am thinking of a word that is {0} letters long.".format(len(secret_word)))
    #create blank letters list, new set of guesses and warnings
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3

    #repeat game until there are guesses or until word is not guessed
    while (not is_word_guessed(secret_word, letters_guessed)) and (guesses_remaining > 0):
      #print message about guesses and available letters
      print("------------", 
        "You have {0} guesses left.".format(guesses_remaining),
        "Available letters: {0}".format(get_available_letters(letters_guessed)),
        sep="\n"
      )
      #input new letter
      letter = input("Please guess a letter: ").lower()
      #cheking for hints
      if letter == "*":
        print("Possible word matches are: ", end="")
        show_possible_matches(get_guessed_word(secret_word, letters_guessed))
      #check letter for appropriate format
      elif len(letter) == 1 and str.isalpha(letter) and not(letter in letters_guessed):
        #memorize that this letter is already named
        letters_guessed.append(letter)
        #if guess is good
        if letter in secret_word:
          print("Good guess: {0}".format(get_guessed_word(secret_word, letters_guessed)))
        #if guess is bad
        else:
          print("Oops! That letter is not in my word: {0}".format(get_guessed_word(secret_word, letters_guessed)))
          #subtract guess according to letter 
          if letter in "aeiou":
            guesses_remaining -= 2
          else:
            guesses_remaining -= 1
      #if letter is already named
      elif letter in letters_guessed:
        print("Oops! You've already guessed that letter. You now have {0} warnings: {1}".format(warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
      #if format is not appropriate
      else:
        #subtract warnings or guesses
        if warnings_remaining != 0:
          warnings_remaining -= 1
        else:
          guesses_remaining -=1
        print("Oops! That is not a valid letter. You have {0} warnings left: {1}".format(warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
    #cycle is end, so if user guessed
    if is_word_guessed(secret_word, letters_guessed):
      print(
        "------------",
        "Congratulations, you won! Your total score for this game is: {0}".format(guesses_remaining*len(set(secret_word))),
        sep="\n"
      )
    #if guesses ended
    else:
      print(
        "------------",
        "Sorry, you ran out of guesses. The word was {0}".format(secret_word),
        sep="\n"
      )



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
    #show_possible_matches("t_ _ t")


    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
