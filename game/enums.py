'''
Created on 27 Apr 2014

@author: Emily
'''


from enum import Enum

class MONS_ATTK(Enum):
    HAND1 = 0
    HAND2 = 1
    BOW = 2
    DART = 3
    MAGIC_DART = 4
    MAGIC_DRAIN = 5




class STATE(Enum):
    BLESSED = 27
    UNCURSED = 28
    CURSED = 29


class RUNE(Enum):
    SLAYING = 30
    FLAME = 31
    ICE = 32
    RUNE_LIGHTNING = 33
    RUNE_DRAIN = 34
    RUNE_PAIN = 35
    RUNE_FLATULENCE = 36



class EQ():
    BODY = 100
    LEGS= 101
    HELMET = 102
    GLOVES = 103
    
    WPN_1HAND = 110
    WPN_2HAND = 111
    
    
class POTION():
    HEAL_NORMAL = 200
    POISON = 201