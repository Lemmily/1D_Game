'''
Created on 13 Apr 2014

@author: Emily
'''

import Reg as R
import Render
from pygame.sprite import RenderUpdates

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
                         "left hand": None, # left weapon/item
                         "right hand": None, # right weapon/item
                         "back": None,
                         "backpack1": None,
                         "backpack2":None,
                         "belt": None,
                         "ring1": None,
                         "ring2": None,
                         "neck": None
                         
                         } #rings, amulets, gloves, quiver, possible "spell slots"
        
        #could have a bool for if equipment changed. and only re-check modifiers if True(like AC and possible buffs) 
        self.sprite_bag = []
        item = Item(R.ITEM_INFO["weapons"]["longsword"])
        self.sprite_bag.append(item)
        item = Item(R.ITEM_INFO["armour"]["robe"], posi = (1,0))
        self.sprite_bag.append(item)
        item = Item(R.ITEM_INFO["armour"]["leather"], posi = (2,0))
        self.sprite_bag.append(item)
        item = Item(R.ITEM_INFO["weapons"]["dagger"], posi = (3,0))
        self.sprite_bag.append(item)
        item = Item(R.ITEM_INFO["potions"]["healing"], posi = (((len(self.sprite_bag)-1)/ 5),((len(self.sprite_bag)-1 )%5)))
        self.sprite_bag.append(item)
        
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
        
    def get_inv_size(self):
        size = len(self.slots)
        return size
    
    def get_inv(self):
        return self.slots
        
    def get_item_pos(self, item):
        index = self.sprite_bag.index(item)
        #(((len(self.sprite_bag)-1)/ 5),((len(self.sprite_bag)-1 )%5)))
        x = 0
        y = 0
        return(x,y)
class Item(object):
    def __init__(self, dict, posi = (0,0), **kwargs):
        self.sprite = Render.SpriteTile(frames = R.SPRITE_CACHE[dict["tilesheet"]], sprite_pos = dict["tile"], 
                                        padding = 10, scaling = 2, pos = posi, offsetX = 460, offsetY = 260)
        
        for key, value in dict.iteritems():
            if key == "tilesheet" or key =="tile":#ignorable keys
                pass
            else:
                setattr(self, key, value)
        
        #print self
    