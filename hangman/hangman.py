import random
import string

VOWELS = {"a", "e", "i", "o", "u"}
UNKNOWN_LETTER = "_ "
HINT_SYMBOL = "*"
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

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """ This function checks if secret_word is guessed, 
    with letters_guessed as set of letters.

    Args:
        secret_word (string): the word the user is guessing
        letters_guessed (set): set with guessed letters

    Returns:
        boolean: True if all the letters of secret_word are in letters_guessed;
    """
    # Looking for each letter from secret_word:
    for letter in secret_word:
        
        # If at least one letter is not guessed:
        if not(letter in letters_guessed):
            return False

        # If or letters are guessed - return false:
    return True


def get_guessed_word(secret_word, letters_guessed):
    """ Makes word with underlines on places of unknown words 
    from secret_word and letters_guessed.

    Args:
        secret_word (string): the word the user is guessing
        letters_guessed (set): set with guessed letters

    Returns:
        string: comprised of letters, underscores (_), and spaces that represents
                which letters in secret_word have been guessed so far.
    """
    # Creating list, that will be join in our word.
    guessed_word = []
    # Adding letters, or "_ " characters in list.
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            guessed_word.append(secret_word[i])
        else:
            guessed_word.append(UNKNOWN_LETTER)  
    # Join our list into string and return it.
    return "".join(guessed_word).strip()


def get_available_letters(letters_guessed):
    """ This function makes string with unknown words.

    Args:
        letters_guessed (set): set with guessed letters

    Returns:
        string: comprised of letters that represents which letters have not
                yet been guessed.
    """
    # Make list only with available letters.
    available_letters = [letter for letter in string.ascii_lowercase if letter not in letters_guessed]
    # Join our list into string and return it.
    return "".join(available_letters)


def print_game_start(secret_word):
    """ This function prints start message

    Args:
        secret_word (string): word to guess
    """
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")


def print_guesses_remaining(letters_guessed, guesses_remaining):
    """ This function prints message,
    that comes with each new try to guess. 
    Prints number of remaining guesses and remaining letters.

    Args:
        letters_guessed (set): set with guessed letters
        guesses_remaining (integer): How many guesses are remaining
    """
    print("------------")
    print(f"You have {guesses_remaining} guesses left.")
    print(f"Available letters: {get_available_letters(letters_guessed)}")


def letter_checker(letter, letters_guessed, guesses_remaining, warnings_remaining):
    """ Checks if letter is in appropriate format for guessing

    Args:
        letter (string): Letters, that`s need to be checked
        letters_guessed (set): set with guessed letters
        guesses_remaining (integer): How many guesses are remaining
        warnings_remaining (integer): How many warnins are remaining

    Returns:
        tuple: tuple with results:
                integer: new value of guesses, 
                integer: new value of warnings,
                boolean: True if word is correct, 
                string: message to show
    """
    # Defining different messages for different cases.
    msg_not_valid = "Oops! That is not a valid letter. You have {} warnings left: {}"
    msg_nv_no_w_left = "Oops! That is not a valid letter. You have {} warnings left so you lose one guess: {}"
    msg_repeated = "Oops! You've already guessed that letter. You now have {} warnings: {}"
    msg_nv_no_w_left = "Oops! You've already guessed that letter. You have {} warnings left so you lose one guess: {}"
    

    # If letter is not in alphabet.
    if letter not in set(string.ascii_lowercase):

        # If there are some warnings - subtract it.
        if warnings_remaining != 0:
            warnings_remaining -= 1 
            return (guesses_remaining, warnings_remaining, False, msg_not_valid)

        # If there are not any warnings - subtract guesses.
        else:
            guesses_remaining -= 1
            return (guesses_remaining, warnings_remaining, False, msg_nv_no_w_left)

    # Checking if letter is already named.
    elif letter in letters_guessed:
        
        # If there are no warnings left - subtract guesses
        if warnings_remaining == 0:
            guesses_remaining -= 1
            return (guesses_remaining, warnings_remaining, False, msg_nv_no_w_left)

        # If there are warnings - subtract one
        warnings_remaining -=1
        return (guesses_remaining, warnings_remaining, False, msg_repeated)

    # If letter was not already named.
    else:
        return (guesses_remaining, warnings_remaining, True, None)


def guessing(secret_word, letter, letters_guessed, guesses_remaining):
    """ Tries to guess a letter and returns a result.
    Args:
        secret_word (string): word to guess
        letter (string): Letters, that`s we trying to guess
        letters_guessed (set): set with guessed letters
        guesses_remaining (integer): How many guesses are remaining

    Returns:
        tuple: results of guessing:
        integer: new amount of guesses
        set: new set of guessed letters, 
        string: message to print.
    """
    # Defining messages to show later.
    msg_good = "Good guess: {}"
    msg_bad = "Oops! That letter is not in my word: {}"

    # Adding new letter to our set of already guessed letters.
    letters_guessed.add(letter)

    # If guess is good - return good msg.
    if letter in secret_word:
        return (guesses_remaining, letters_guessed, msg_good)

    # If guess was wrong - return bad msg and substract guesses. 
    elif letter in VOWELS:
        guesses_remaining -= 2
        return (guesses_remaining, letters_guessed, msg_bad)
    else:
        guesses_remaining -= 1
        return (guesses_remaining, letters_guessed, msg_bad)

def get_score(secret_word, guesses_remaining):
    """ Function calculates a score of game 
    with given word and remaining guesses.

    Args:
        secret_word (string): word to guess
        guesses_remaining (integer): How many guesses are remaining

    Returns:
        integer: score of current game
    """
    return guesses_remaining * len(set(secret_word))


def print_game_ending(secret_word, letters_guessed, guesses_remaining):
    """ This function prints result of hangman game.

    Args:
        secret_word (string): word to guess
        letters_guessed (set): set with guessed letters
        guesses_remaining (integer): How many guesses are remaining
    """
    # If word was guessed:
    if is_word_guessed(secret_word, letters_guessed):
        print("------------")
        print()
        print("Congratulations, you won!",
            f"Your total score for this game is: {get_score(secret_word, guesses_remaining)}",
            )
    
    # If word was not guessed:
    else:
        print("------------")
        print(f"Sorry, you ran out of guesses. The word was {secret_word}")



def match_with_gaps(my_word, other_word):
    """ This functions checks if my_word with gaps is mathching to other_word.

    Args:
        my_word (string): current guess of secret word with "_" characters
        other_word (string): regular English word

    Returns:
        boolean: True if all the actual letters of my_word match the 
                 corresponding letters of other_word, or the letter is the special symbol
                 _ , and my_word and other_word are of the same length;
                 False otherwise.
    """

    # Check if length of my_word and other_word is same:
    if len(my_word) != len(other_word):
        return False
    
    # If length is same
    for i in range(len(my_word)):
        # Check if letters on same positions are different (except positions with"_",
        # and check if we have similar case as: comparing a_bc and abbc)
        if (my_word[i] != UNKNOWN_LETTER.strip()) and (my_word[i] != other_word[i]):
            return False
        elif (my_word[i] == UNKNOWN_LETTER.strip()) and (other_word[i] in my_word):
            return False
    return True


def show_possible_matches(my_word):
    """ This function prints out every word in wordlist that matches my_word

    Args:
        my_word (string): current guess of secret word with "_ " characters
    """
    # Creating blank list where we will be containing our matches
    list_with_mathes = []

    # Delete all spaces, to work more convenient
    my_word = my_word.replace(" ", "")

    # Adding all of our matching words in cycle
    for word_from_list in wordlist:

        # If word is matching
        if match_with_gaps(my_word, word_from_list):
            list_with_mathes.append(word_from_list)

    # Print result
    if list_with_mathes == []:
        print("No matches found")
    else:
        print("Possible word matches are:", *list_with_mathes)
    


# Hangman function.  If you want to play with hints: give True as a second argument.
def hangman(secret_word, hints_on=False, guesses_remaining=6, warnings_remaining=3 ):
    """ Starts up Hangman game.

    Args:
        secret_word (string): word to guess
        hints_on (bool, optional): True, if you want to play with hints. Defaults to False.
        guesses_remaining (int, optional): the number of guesses. Defaults to 6.
        warnings_remaining (int, optional):  The number of warnings.. Defaults to 3.
    """
    # Printing hello message.
    print_game_start(secret_word)
    
    # Create blank set for containing guessed letters,
    letters_guessed = set()
    
    # Playing while there are remaning guesses, or word isn`t guessed
    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):

        # Printing message about guesses remaining
        print_guesses_remaining(letters_guessed, guesses_remaining)

        # Asking for new letter
        letter = input("Please guess a letter: ").lower()

        # Activating hints
        if letter == HINT_SYMBOL and hints_on:
            # Printing possible matches
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        
        # Checking if this is really letter, not another symbol, then update remaining warnings and guesses
        guesses_remaining, warnings_remaining, letter_is_correct, msg = (
            letter_checker(letter, letters_guessed, guesses_remaining, warnings_remaining))

        # Printing about inappropriate format
        if not letter_is_correct:
            print(msg.format(warnings_remaining, get_guessed_word(secret_word, letters_guessed)))

        # If all right - trying to guess
        else:
            guesses_remaining, letters_guessed, msg = guessing(secret_word, letter, letters_guessed, guesses_remaining)
            print(msg.format(get_guessed_word(secret_word, letters_guessed)))

    # Printing result
    print_game_ending(secret_word, letters_guessed, guesses_remaining)



if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word, hints_on=True)