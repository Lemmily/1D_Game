'''
Created on 12 Apr 2014

@author: james & emily
'''

import sys

from Reg import *

import pygame as pg
import pygame.locals

import Entity


gamefont = None
black = 0, 0, 0
white = 255, 255, 255


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

def attack_next():
    if len(queue) > 0:
        Entity.combat(player, queue[0]) 
        Entity.combat(queue[0], player) 
        
        
class Game(object):
    
    def __init__(self):
        global player
        self.screen = pg.display.get_surface()
        self.pressed_key = None
        self.mouse_pressed = None
        self.mouse_pos = None
        self.game_over = False
        self.overlays = pygame.sprite.RenderUpdates
        
        player = Entity.Player()
        
        for i in range(7):
            queue.append(Entity.Creature((20,50,20), (200 + i * 110,110)))
        
    def controls(self):
        
        #keys = pg.key.get_pressed()
        
        
        def pressed(key):
            return self.pressed_key == key #or keys[key]
        
        def m_pressed(mouse):
            return self.mouse_pressed == mouse 
        
        if pressed(pg.K_j):
            print "Emily Loves James"
        if pressed(pg.K_q):
            attack_next()
            
        if pressed(pg.K_h):
            if Entity.use(player, "hp potion"):
                Entity.heal(player, 10)
        self.pressed_key = None
     
        if m_pressed(1):
            for thing in queue:
                if thing.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    Entity.combat(player, thing) 
                    Entity.combat(thing, player)   
                    break
        self.mouse_pressed = None
        
        
  
    def main(self):
        global player
        
        clock = pg.time.Clock()
        
        #updates screen
        pg.display.flip()
        
        # main game loop
        while not self.game_over:
            #clear screen
            self.screen.fill(black)
            
            #check to see if we can do anything with the keys pressed or mouse pressed
            self.controls()
            
            label = gamefont.render("Health: " + str(player.hp), 1, (255,255,10))
            self.screen.blit(label, (10, 10))
            label = gamefont.render("Health Potions: " + str(player.inventory.count("hp potion")), 1, (255,255,0))
            self.screen.blit(label, (10, 40))
            pg.draw.rect(self.screen, player.colour, player.rect)
            
            for thing in queue:
                if thing.dead:
                    queue.remove(thing)
                    print "creature has died"
                    if len(queue) <= 0:
                        print "winner, winner, chicken dinner"
                        break
                    
            for i in range(len(queue)):
                thing = queue[i]
                thing.rect.x = 200 + i*110
                thing.pos = (200 + i*110, 110)
                pg.draw.rect(self.screen, thing.colour, thing.rect)
                
                #draw a health bar
                health_per = 100/thing.max_hp * thing.hp
                pg.draw.rect(self.screen, (100,20,20), (thing.pos[0],thing.pos[1] + 105, health_per, 20))
                    
                    
            clock.tick(15)
            #update screen with changes
            pg.display.flip()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                elif event.type == pg.KEYDOWN:
                    self.pressed_key = event.key
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed = event.button
                    self.mouse_pos = event.pos
#                    print event.pos
#                    for thing in queue:
#                        print thing.pos
                
    


if __name__=='__main__':
    pg.init()
    pg.display.set_mode((1024,768))
    pg.display.set_caption('1D_RL')
    #load font
    gamefont = pygame.font.SysFont("monospace", 15)
    Game().main()
    
    
    
    
    