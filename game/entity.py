'''
Created on 12 Apr 2014

@author: james
'''
import pygame as pg
from random import randint

from inventory import *

class Entity(object):
    
    def __init__(self, colour, pos):
        self.hp = 10
        self.max_hp = 10
        self.mana = 10
        self.max_mana = 10
        
        
        self.melee_attack_dmg = 4
        self.ranged_attack_dmg = 0
        self.colour = colour
        self.size = (100,100)
        self.pos = pos
        self.rect = pg.Rect(self.pos,self.size)
        self.dead = False
        self.has_melee = True
        self.has_ranged = False
        
    def update_health(self, change):
        
        #make sure you can't heal a dead guy.
        if not self.dead:
            self.hp += change
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            
            #check to see if it's dead
            self.check_alive()
            return self.hp
        return False
            
    def update_mana(self, change):
        self.mana += change
        
    def get_attack(self):
        return self.melee_attack_dmg    
    
    def get_ranged_damage(self):
        return self.ranged_attack_dmg
    
    def get_health(self):
        return self.hp
    
    def check_alive(self):
        if self.get_health() <= 0:
            self.dead = True
        



class Player(Entity):
    def __init__(self):
        Entity.__init__(self, (255,255,255), (10,110))

        self.hp = 100
        self.max_hp = 100
        self.mana = 12
        self.max_mana = 12
        self.inventory = Inventory()
        self.inventory.pick_up("hp potion", 3)
       
       
       
        
class Creature(Entity):
    
    def __init__(self, colour, pos):
        Entity.__init__(self, colour, pos)
        if randint(0,1) == 1:
            self.has_ranged = True
            self.ranged_attack_dmg = randint(1,5)
        
        
        
        
        
def hp_calc(strength):
    return strength * 2

def mp_calc(intelligence):
    return intelligence * 2

# time between attacks, decreases as dexterity increases
#def att_speed_calc(dexterity):
#    return att_speed_var / dexterity 

def melee_attack_damage(strength):
    return strength / 2.0

def combat(attacker, defender):
    #TODO: actual combat calculations - to hits etc.
    defender.update_health(-attacker.get_attack())
    print defender.hp, "/", attacker.hp
    
    
def heal(entity, amount):
    entity.update_health(amount)
    
    
def use(entity, item_type):
    if entity.inventory:
        if entity.inventory.get(item_type):
            return True
        else:
            return False
    else:
        return False
        
        
        
        
        
        
    
def ranged_combat(attacker, defender):
    defender.update_health(-attacker.get_ranged_damage())    

