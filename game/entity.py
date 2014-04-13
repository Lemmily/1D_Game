'''
Created on 12 Apr 2014

@author: james
'''
import pygame as pg
from random import randint

class Entity(object):
    
    def __init__(self, colour, pos):
        self.health_points = 10
        self.mana_pool = 10
        # self.attack_speed = att_speed_calc(self.dexterity)
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
        self.health_points += change
        print self.health_points
        self.check_alive()
        return self.health_points
            
    def update_mana(self, change):
        self.mana_pool += change
        
    def get_attack(self):
        return self.melee_attack_dmg    
    
    def get_ranged_damage(self):
        return self.ranged_attack_dmg
    
    def get_health(self):
        return self.health_points
    
    def check_alive(self):
        if self.get_health() <= 0:
            self.dead = True
        

class Player(Entity):
    
    def __init__(self):
        Entity.__init__(self, (255,255,255), (10,110))
        self.health_points = 50
        self.mana_pool = 12
        self.ranged_attack_dmg = 4
        
       
        
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
    defender.update_health(-attacker.get_attack())
    
def ranged_combat(attacker, defender):
    defender.update_health(-attacker.get_ranged_damage())    

