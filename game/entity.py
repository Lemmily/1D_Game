'''
Created on 12 Apr 2014

@author: james
'''

att_speed_var = 60

class Entity(object):
    
    def __init__(self):
        self.health_points = 10
        self.mana_pool = 10
       # self.attack_speed = att_speed_calc(self.dexterity)
        self.melee_attack_dmg = 4
        
        def update_health(change):
            self.health_points += change
            
        def update_mana(change):
            self.mana_pool += change

class Player(Entity):
    '''
    classdocs
    '''
    
    def __init__(self):
        Entity.__init__(self)
        
       
        
class Creature(Entity):
    
    
    def __init__(self):
        Entity.__init__(self)
        
def hp_calc(strength):
    return strength * 2

def mp_calc(intelligence):
    return intelligence * 2

# time between attacks, decreases as dexterity increases
def att_speed_calc(dexterity):
    return att_speed_var / dexterity 

def melee_attack_damage(strength):
    return strength / 2.0

fat = Player()
print melee_attack_damage(5)