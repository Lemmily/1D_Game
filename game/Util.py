'''
Created on 23 Apr 2014

@author: james
'''
from random import randint

def roll_dice(size):
    return randint(1,size)

def multi_roll_dice(num,size):
    sum = 0
    for dice in xrange(num):
        sum += roll_dice(size)
    return sum

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
        


best_of_roll(6,6,4)  