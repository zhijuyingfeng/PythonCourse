# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import re

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    word=word.lower()#将word所有字母转换为小写
    length=len(word)
    first=0
    for letter in word:
        first+=SCRABBLE_LETTER_VALUES[letter]#乘积的第一部分
    second=1
    second=max(second,7*length-3*(n-length))#乘积的第二部分
    return first*second


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))#元音字母占1/3，其中包括一个通配符
    hand['*']=1#通配符

    for i in range(1,num_vowels):#元音字母
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):#其他字母
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    hand_copy=hand.copy()
    word=word.lower()#将word所有字母转换为小写

    for letter in word:
        temp=hand_copy.get(letter,0)
        if temp>=1:#如果字典中有该键，且其值大于等于1
            hand_copy[letter]-=1#将其值减1
            if hand_copy[letter]==0:#若减1后值为0，将其从字典中去除
                hand_copy.pop(letter,0)
    
    return hand_copy

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    hand_copy=hand.copy()
    word=word.lower()#将word所有字母转换为小写
    for letter in word:
        temp=hand_copy.get(letter,0)
        if temp==0:#如果word中存在字典中没有的字母，直接返回False
            return False
        hand_copy[letter]-=1#如果这个字母在字典中存在，将其对应的值减1
    
    word=word.replace("*","[aeoiu]")#用[aeiou]替换*以进行正则表达式的匹配
    pattern=re.compile(word)#编译正则表达式

    for w in word_list:#对word_list中的每一个单词进行正则表达式的匹配
        if pattern.fullmatch(w):#如果可以完全匹配，则返回True
            return True
    return False#在word_list中没有找到与之匹配的单词，返回False

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):#计算hand中可用的字母数
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    sum=0
    for k,v in hand.items():#遍历键值对，对值求和
        sum+=v
    return sum

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

    total_score=0
    #hand=deal_hand(HAND_SIZE)
    while calculate_handlen(hand)>0:#当还有可用字母时继续循环
        print("​Current hand: ",end='')
        display_hand(hand)
        ans=input('Enter word, or "!!" to indicate that you are finished: ')#提示用户输入答案

        if '!!'==ans:
            break

        if is_valid_word(ans,hand,word_list):#如果答案合法
            score=get_word_score(ans,calculate_handlen(hand))#计算得分
            total_score+=score#更新总分
            print('"{}" earned {} points. Total: {} points\n'.format(ans,score,total_score))
        
        else:
            print("That is not a valid word. Please choose another word.\n")

        hand=update_hand(hand,ans)#无论用户答案合法与否，均扣除用户输入的字母
    
    if calculate_handlen(hand)==0:
        print("\nRan out of letters")
    #print("Total score: {} points".format(total_score))
    return total_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    hand_copy=hand.copy()#对hand的副本进行操作
    if 0==hand_copy.get(letter,0):#如果hand中没有字母，直接返回即可
        return hand_copy
    
    alphabet=string.ascii_lowercase#26个小写字母
    # alphabet='a'

    unused=''#保存hand中用过的字母
    for alpha in alphabet:
        if hand_copy.get(alpha,0)==0:#如果字母在hand中出现过，将其加入到unused中
            unused+=alpha
    
    char=random.choice(unused)#从未用过的字母中随机挑选一个
    hand_copy[char]=1#加入到hand_copy中
    hand_copy[letter]-=1#将原来的字母对应的值减1
    if hand_copy[letter]==0:#如果原来的字母对应的值降为0，将其从hand_copy中去除
        hand_copy.pop(letter,0)
    
    return hand_copy

def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    hand_number=0#可以进行的游戏轮数
    substitute_chance=1#可替换一个字母的剩余次数
    replay_chance=1#可以重玩一轮的剩余次数
    replay=False#表示该轮是否是重玩的
    scores=[]#表示每一轮的最高得分
    while True:
        inp=input("Enter total number of hands: ")#提示用户输入游戏轮数
        try:#简单的错误处理
            hand_number=int(inp)
            break
        except:
            print("Bad input, please try again!")
    
    hands=[]#每一轮游戏的字母集
    for i in range(hand_number):#随机获取每一轮游戏的字母集
        hands.append(deal_hand(HAND_SIZE))

    # hands.append({'a':1,'c':1,'i':1,'*':1,'p':1,'r':1,'t':1})
    # hands.append({'d':2,'*':1,'a':1,'o':1,'u':1,'t':1})

    i=0
    while i<hand_number:
        hand=hands[i]
        if not replay:
            print("Current hand: ",end='')
            display_hand(hand)
        op=''
        
        if substitute_chance>0 and not replay:#还有替换机会并且不是在重玩某一轮
            while True:#处理用户输入错误
                op=input("Would you like to substitute a letter?")
                if op=='no' or op=='n':
                    break
                elif op=='yes' or op=='y':
                    substitute_chance-=1#减去一次替换机会
                    letter=''#用户想要替换的字母

                    while True:#处理用户输入错误
                        letter=input("Which letter would you like to replace: ")#提示用户输入想要替换的字母
                        if len(letter)==1 and (letter=='*' or letter in string.ascii_lowercase):
                            break
                        else:
                            print("Bad input, please try again!")

					#更新该轮游戏的字母集
                    hand=substitute_hand(hand,letter)
                    hands[i]=hand
                    break
                else:
                    print("Bad input, please try again!")
        
        print()
        score=play_hand(hand,word_list)#展示该轮游戏得分

        #print('\nRan out of letters')
        print('Total score for this hand: %d'%score)
        print('----------')
        
        if len(scores)==i:
            scores.append(score)
        elif i<len(scores):#选取最高分
            scores[i]=max(score,scores[i])
        
        if replay_chance>0:#用户还有一次重玩机会时
            while True:#处理用户输入错误
                op=input("Would you like to replay the hand?")
                if op=='yes' or op=='y':
                    i-=1
                    replay_chance-=1#重玩机会减1
                    replay=True#表示下一轮游戏是重玩的
                    break
                elif op=='no' or op=='n':
                    replay=False#表示下一轮游戏不是重玩的
                    break
                else:
                    print("Bad input, please try again!")
        else:#表示下一轮游戏不是重玩的
            replay=False
        
        i+=1
    total_score=0
    for score in scores:#计算总分
        total_score+=score
    print("Total score over all hands: %d"%total_score)
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
