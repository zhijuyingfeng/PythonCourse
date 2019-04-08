# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import re

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
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for i in range(len(secret_word)):
      if not secret_word[i] in letters_guessed:
        return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    temp=''
    for i in range(len(secret_word)):
      if secret_word[i] in letters_guessed:
        temp=temp+secret_word[i]
      else:
        temp=temp+'_ '
    return temp


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    res=''
    alpha=string.ascii_lowercase
    for letter in alpha:
      if not letter in letters_guessed:
        res=res+letter
    return res
    
    

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
    print('\nI am thinking of a word that is {} letters long.'.format(len(secret_word)))
    print('You have 3 warnings left.\n')
    print('-------------')
    guesses_left=6
    warnings_left=3
    letters_guessed=[]
    output=''
    right_letters=[]

    while guesses_left>0:
      print('You have {} guesses left.'.format(guesses_left))
      print('Available letters:',get_available_letters(letters_guessed))

      letter=input('Please guess a letter:')
      if len(letter)==1 and letter.isalpha() and not letter in letters_guessed:
        letter=letter.lower()
        letters_guessed.append(letter)
        if letter in secret_word:
          output=get_guessed_word(secret_word,letters_guessed)
          right_letters.append(letter)
          print('Good guess: ',output)
          if not '_' in output:
            print('\n-----------\n')
            break
        else:
          guesses_left-=1
          if letter in ['a','e','i','o','u']:
            guesses_left-=1
          print('Oops! That letter is not in my word: ',output)
      
      else:
        if letter in letters_guessed:
          print("Oops! You've already guessed that letter.",end='')
        else:
          print('Oops! That is not a valid letter.',end='')

        if warnings_left>0:
          warnings_left-=1
          print('You have {} warning(s) left: '.format(warnings_left),output)

        else:
          guesses_left-=1
          print('You have no warnings left, so you lose one guess: ',output)

      print('\n-----------\n')

    if guesses_left>0:
      print('Congratulations, you won!')
      print('Your total score for this game is: ',guesses_left*len(right_letters))
    else:
      print('Sorry, you ran out of guesses. The word was {}.'.format(secret_word))



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
    i=0
    j=0
    tmp=[]
    while i<len(my_word) and j<len(other_word):
      if my_word[i]=='_':
        i+=2
        tmp.append(other_word[j])
        j+=1
        continue
      elif not my_word[i]==other_word[j]:
        return False
      i+=1
      j+=1
    for letter in tmp:
      if letter in my_word:
        return False
    if not i==len(my_word) or not j==len(other_word):
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
    if not '_ ' in my_word:
      print(my_word)
    
    cnt=0
    # for i in range(len(my_word)):
    #   if my_word[i]==' ':
    #     cnt+=1
    #pattern='^'+my_word.replace('_ ','.')+'$'
    for word in wordlist:
      #if not re.match(pattern,word)==None:
      if match_with_gaps(my_word,word): 
        print(word,end=' ')
        cnt+=1
    if cnt==0:
      print('No matches found')
    print('')


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
    print('\nI am thinking of a word that is {} letters long.'.format(len(secret_word)))
    print('You have 3 warnings left.\n')
    print('-------------')
    guesses_left=6
    warnings_left=3
    letters_guessed=[]
    output='_ '*len(secret_word)
    right_letters=[]

    while guesses_left>0:
      print('You have {} guesses left.'.format(guesses_left))
      print('Available letters:',get_available_letters(letters_guessed))

      letter=input('Please guess a letter:')
      if letter=='*':
        show_possible_matches(output)
        
      elif len(letter)==1 and letter.isalpha() and not letter in letters_guessed:
        letter=letter.lower()
        letters_guessed.append(letter)
        if letter in secret_word:
          output=get_guessed_word(secret_word,letters_guessed)
          right_letters.append(letter)
          print('Good guess: ',output)
          if not '_' in output:
            print('\n-----------\n')
            break
        else:
          guesses_left-=1
          if letter in ['a','e','i','o','u']:
            guesses_left-=1
          print('Oops! That letter is not in my word: ',output)
      
      else:
        if letter in letters_guessed:
          print("Oops! You've already guessed that letter.",end='')
        else:
          print('Oops! That is not a valid letter.',end='')

        if warnings_left>0:
          warnings_left-=1
          print('You have {} warning(s) left: '.format(warnings_left),output)

        else:
          guesses_left-=1
          print('You have no warnings left, so you lose one guess: ',output)

      print('\n-----------\n')

    if guesses_left>0:
      print('Congratulations, you won!')
      print('Your total score for this game is: ',guesses_left*len(right_letters))
    else:
      print('Sorry, you ran out of guesses. The word was {}.'.format(secret_word))




# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # print("Welcome to the game Hangman!")
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
