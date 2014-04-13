'''
Created on 12 Apr 2014

@author: james & emily
'''

import sys

from reg import *

import pygame as pg
import pygame.locals

import entity



class DummyObject(object):
    
    def __init__(self, colour, pos):
        self.colour = colour
        self.size = (100,100)
        self.pos = pos
        self.rect = pg.Rect(self.pos,self.size)
        
        
        
        self.melee_range = 1
        self.ranged_range = 3
        self.magic_range = 4
        
    def interact(self, *args):
        self.destroy_self()
        
    def destroy_self(self):
        #do somethign to notify I need to be removed from queue??!
        print "I gots killed"



class Game(object):
    
    def __init__(self):
        global player
        self.screen = pg.display.get_surface()
        self.pressed_key = None
        self.mouse_pressed = None
        self.mouse_pos = None
        self.game_over = False
        self.overlays = pygame.sprite.RenderUpdates
        
        player = entity.Player()
        
        for i in range(7):
            queue.append(entity.Creature((20,50,20), (200 + i * 110,110)))
        
    def controls(self):
        
        #keys = pg.key.get_pressed()
        
        
        def pressed(key):
            return self.pressed_key == key #or keys[key]
        
        def m_pressed(mouse):
            return self.mouse_pressed == mouse 
        
        if pressed(pg.K_j):
            print "Emily Loves James"
        if pressed(pg.K_q):
            entity.combat(player, queue[0]) 
            entity.combat(queue[0], player)   
        self.pressed_key = None
     
        if m_pressed(1):
            for thing in queue:
                if thing.rect.collidepoint(pg.mouse.get_pos()):
                    entity.combat(player, thing) 
                    entity.combat(thing, player)   
        self.mouse_pressed = None
        
        
  
    def main(self):
        global player
        
        clock = pg.time.Clock()
        
        
        pg.display.flip()
        
        # main game loop
        while not self.game_over:
            black = 0, 0, 0
            self.screen.fill(black)
            
            #check to see if we can do anything with the keys pressed or mouse pressed
            self.controls()
            
            
            pg.draw.rect(self.screen, player.colour, player.rect)
            
            for thing in queue:
                if thing.dead:
                    queue.remove(thing)
                    print "creature has died"
                    if len(queue) <= 0:
                        print "winner, winner, chicken dinner"
                        break
                    
            for i in range(len(queue)):
                thing.rect.left = 200 + i*110
                pg.draw.rect(self.screen, thing.colour, thing.rect)
                    
                    
            clock.tick(15)
            pg.display.flip()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                elif event.type == pg.KEYDOWN:
                    self.pressed_key = event.key
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed = event.button
                    self.mouse_pos = event.pos
                
    


if __name__=='__main__':
    pygame.init()
    pygame.display.set_mode((1024,768))
    Game().main()
    
    
    
    
    