'''
Created on 13 Apr 2014

@author: Emily
'''

import Entity

class Inventory(object):
    
    def __init__(self):
        ## not sure what kind of data structure to hold the items, 
        ##dict is easier to access and find stuff, list is easier to draw and "manage slots"
        self.contents = {}
        self.slots = [None for i in xrange(0,25)]
        
        #basic person type equipment for now.
        self.equipped = {
                         "torso": None, 
                         "legs": None, 
                         "head": None, 
                         "left hand": None, 
                         "right hand": None 
                         
                         } #rings, amulets, gloves, quiver, possible "spell slots"
        
        #could have a bool for if equipment changed. and only re-check modifiers if True(like AC and possible buffs) 
        
    def get(self, _type):
        if self.contents.has_key(_type) and self.contents[_type] > 0:
            self.contents[_type] -= 1
            return True
        else:
            return False
    
    def pick_up(self, _type, amount = 1):
        if self.contents.has_key(_type):
            self.contents[_type] += amount
        else:
            self.contents[_type] = amount
    
    
    def has(self, _type):
        if self.contents.has_key(_type) and self.contents[_type] > 0:
            return True
        else:
            return False
        
    def drop(self, _type):
        #temporarily does the same thing as the get function.
        if self.contents.has_key(_type) and self.contents[_type] > 0:
            self.contents[_type] -= 1
            return True
        else:
            return False
    
    def count(self, _type):
        if self.contents.has_key(_type):
            return self.contents[_type]
        else:
            return 0
        
        
class Item(object):
    def __init__(self):
        self.sprite = Render.Sprite()
    
    
    