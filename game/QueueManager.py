'''
Created on 14 Apr 2014

@author: Emily
'''

from Reg import *


class QueueManager(object):
    def __init__(self):
        pass
        
    def give_AP(self, entity, amount):
        entity.add_action_points(amount)
            
            
    def add_entity(self):
        #TODO: picks an object or enemy to add to the end of the queue
        pass    
    
    def enemy_turns(self, players_action_ap):
        for enemy in queue:
            enemyPos = queue.index(enemy) #get enemy queue position
            
            #ask if the enemy has an action that is within range.
            #also -> an action could be to heal itself. so that's always in range
            if enemy.in_range(enemyPos): 
                
                #TODO: does the enemy receive the ap before or after their move? doing before for now.
                enemy.add_action_points(players_action_ap)
                
                #enemy manages it's own AI choices? like which attack to use etc?
                enemy.take_turn()
                
                
                