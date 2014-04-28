'''
Created on 23 Apr 2014

@author: james
'''
from random import randint
import ConfigParser

def random_choice(chances_dict):
    #choose one option from a dictionary of chances, returning the key.

    chances = chances_dict.values() # all the values
    strings = chances_dict.keys() #all the keys

    return strings[rand_choice_index(chances)]

def rand_choice_index(chances): #choose one option from the list of chances, returning its index
    #the dice will land on some number between 1 and the sum of all the chances.
    dice = randint(1, sum(chances)) #libtcod.random_get_int(0, 1, sum(chances))

    #go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w
        #sees if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1
        
def coin_filp():
    if randint(0,1) == 1: 
        return True
        
    else: 
        return False
        
def roll_dice(size):
    return randint(1,size)

def multi_roll_dice(num,size):
    _sum = 0
    for dice in xrange(num):
        _sum += roll_dice(size)
    return _sum

def best_of_roll(num,size,keep):
    rolls = []
    best = 0
    for dice in xrange(num):
        rolls.append(roll_dice(size))
    rolls.sort()
    print rolls     # see the rolls
    for dice in xrange(keep):
        best += rolls.pop()
    print best      # check best total
    return best    
        

def load_files(filename = "data/monsters"):
    
    parser = ConfigParser.ConfigParser()
    parser.read(filename)
    monsters = {}
    
    for section in parser.sections():
        desc = dict(parser.items(section))
        monsters[section] = desc
        
    return monsters
    