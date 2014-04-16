'''
Created on 12 Apr 2014

@author: James & Emily
'''
import pygame as pg
from random import randint

from Inventory import *


import Reg

class Entity(object):
    
    def __init__(self, colour, pos):
        self.hp = 10
        self.max_hp = 10
        self.mana = 10
        self.max_mana = 10
        
        
        self.melee_attack_dmg = 4
        self.ranged_attack_dmg = 1
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
            
    def check_alive(self):
        if self.get_health() <= 0:
            self.dead = True
            
    def update_mana(self, change):
        self.mana += change
        
    def get_health(self):
        return self.hp
    
        
    ###### 
    ###
    #     Alll these below will be affected by the stats changes.
    ###   TODO: Deploy stat changes.
    ######
    def get_attack(self):
        return self.melee_attack_dmg    
    
    def get_ranged_damage(self):
        return self.ranged_attack_dmg
    
        

    def get_range(self):
        return 0, 1



class Player(Entity):
    def __init__(self):
        Entity.__init__(self, (255,255,255), (10,110))

        self.hp = 100
        self.max_hp = 100
        self.mana = 12
        self.max_mana = 12
        self.inventory = Inventory()
        self.inventory.pick_up("hp potion", 3)
       
       
        #TEMP: attack_cost
        self.attack_cost = 15
        
        
       
        
class Creature(Entity):
    
    def __init__(self, colour, pos):
        Entity.__init__(self, colour, pos)
        self.action_points = randint(0,30)
        
        
        self.melee_cost = 30
        
        if randint(0,1) == 1:
            self.has_ranged = True
            self.ranged_cost = 40
            self.ranged_attack_dmg = randint(1,5)
        
    def get_action_points(self):
        return self.action_points
    
    def add_action_points(self, ap):
        self.action_points += ap
        
    def check_action_points(self, cost):
        if cost <= self.action_points:
            return True
        else:
            return False    
    
    def use_action_points(self, cost):
        if self.check_action_points(cost):
            self.action_points -= cost
        else:
            print "Error: not enough AP" 
        
    def in_range(self, current_range):
        if (self.has_melee and current_range <= 1) or (self.has_ranged and current_range <= 5):
            return True
        else:
            return False
        
    def take_turn(self, q_position):
        #TODO: decision making.
        #check from shortest -> longest range for now, and just do whatever it can do
        
        #need a way to store actions, action cost, action range
        if q_position <= 1 and self.action_points > self.melee_cost:
            self.do_melee_attack(q_position)
        elif self.has_ranged and q_position <= 5 and self.action_points > self.ranged_cost:
            self.do_ranged_attack(q_position)
        
        
    def do_ranged_attack(self, q_position):
        #TODO: possibly abstarct this back an inheritence level - currently *always* attacks player.
        
        #TODO: attack calculations
        self.use_action_points(self.ranged_cost)
        if randint(0,5) <= 3:
            damage = self.get_ranged_damage()
            Reg.player.update_health(-damage)
            print "Enemy " + str(q_position) + " fires it's bow and does " + str(damage)+ " leaving the player with " + str(Reg.player.hp) 
        else:
            print "Enemy " + str(q_position) + " fumbles its attack!"
            
    def do_melee_attack(self, q_position):
        #TODO: possibly abstarct this back an inheritence level - currently *always* attacks player.
        
        #TODO: attack calculations
        self.use_action_points(self.melee_cost)
        if randint(0,5) <= 3:
            damage = self.get_attack()
            Reg.player.update_health(-damage)
            print "Enemy " + str(q_position) + " swings it's sword and does " + str(damage)+ " leaving the player with " + str(Reg.player.hp)
            
        else:
            print "Enemy " + str(q_position) + " fumbles its attack!"
        
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
    #TODO: actual combat calculations - to hits etc 
    #TODO: this maybe needs to be put into queue manager? or something like that?
    
    defender.update_health(-attacker.get_attack())
    print defender.hp, "/", attacker.hp
    
    
def heal(Entity, amount):
    Entity.update_health(amount)
    
    
def use(Entity, item_type):
    if Entity.inventory:
        if Entity.inventory.get(item_type):
            return True
        else:
            return False
    else:
        return False
        
        
        
        
        
        
    
def ranged_combat(attacker, defender):
    defender.update_health(-attacker.get_ranged_damage())    

