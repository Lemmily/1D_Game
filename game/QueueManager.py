'''
Created on 14 Apr 2014

@author: Emily
'''
import pygame as pg

DEADTHINGS = pg.USEREVENT + 1

class QueueManager(object):
    def __init__(self):
        self.queue = []
        
        #TODO: When there are "themes" and prgression involved - the queue manager.... 
        # can know what kind of bg tile needs to be displayed under each queue position?
        self.theme_floor = [1 for i in range(10)] #hold a numerical value to represent the theme for the tile
        
        
    def add_entity(self, entity):
        #TODO: picks an object or enemy to add to the end of the queue
        #for now just posts what it's given into the queue
        
        self.queue.append(entity)
    
    def purge_the_dead(self):
        for thing in self.queue:
            the_dead = []
            if thing.dead:
                self.queue.remove(thing)
                the_dead.append(thing)
                print "creature has died"
        if len(the_dead) > 0:
            pg.event.post(pg.event.Event(DEADTHINGS, dead = the_dead))
            for i in xrange(len(self.queue)):
                thing = self.queue[i]
                pos = thing.pos
                if pos[0] != 220 + i*110 or pos[0] != 100:
                    thing.pos = i,1
    
    def enemy_turns(self, players_action_ap):
        #purge the dead things
        #self.purge_the_dead()
        the_dead = []
        for enemy in self.queue:
            
            enemyPos = self.queue.index(enemy) #get enemy queue position
            
            #TODO: needs to me moved to queue manager?
            #ask if the enemy has an action that is within range.
            #also -> an action could be to heal itself. so that would technically always in range.
            if enemy.in_range(enemyPos): 
                
                #TODO: does the enemy receive the ap before or after their move? doing before for now.
                enemy.add_action_points(players_action_ap)
                
                #enemy manages it's own AI choices? like which attack to use etc?
                enemy.take_turn(enemyPos)
                
            if enemy.dead:
                self.queue.remove(enemy)
                the_dead.append(enemy)
                print "creature has died"
        if len(the_dead) > 0:
            pg.event.post(pg.event.Event(DEADTHINGS, dead = the_dead))
            for i in xrange(len(self.queue)):
                thing = self.queue[i]
                pos = thing.pos
                if pos[0]-2 !=  i or pos[0] != 1:
                    thing.pos = 2 + i,1
            
                