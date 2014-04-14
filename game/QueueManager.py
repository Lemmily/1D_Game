'''
Created on 14 Apr 2014

@author: Emily
'''

from reg import *


class QueueManager(object):
    def __init__(self):
        pass
        
    def give_AP(self, amount):
        for enemy in queue:
            if enemy.in_range(player):
                enemy.get_ap(amount)
            
            
    def add_entity(self):
        #TODO: picks an object or enemy to add to the end of the queue
        pass    