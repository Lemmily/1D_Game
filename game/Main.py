'''
Created on 12 Apr 2014

@author: James & Emily
'''

import Entity
import QueueManager
import Reg as R
import pygame as pg
import pygame.locals
import sys


from random import randint
    



gamefont = None
black = 0, 0, 0
white = 255, 255, 255
bg_colour = 33, 100, 117 

############################]
# 
# 
# TESTING STUFF
#
#
###################


        
#END TEST STUFF
############################################################       
        
def attack_next():
    if len(queue) > 0:
        ap = player.attack_cost
        Entity.combat(player, queue[0])
        man_queue.enemy_turns(ap)
        return True
    else:
        return False
    



class Game(object):
    
    def __init__(self):
        global man_queue, player, queue, tes, potion_ts
        self.screen = pg.display.get_surface()
        self.pressed_key = None
        self.mouse_pressed = None
        self.mouse_pos = None
        self.game_over = False
        self.overlays = pygame.sprite.RenderUpdates()
        self.sprites = Entity.SortedUpdates()
        
        sprite = Entity.Player()
        self.sprites.add(sprite)
        
        self.background = pygame.Surface((1024, 768))
        self.background.fill(bg_colour)
        
        
        self.dirties = None #holds the dirty bits for updating when rendered.
        
        R.player = player = Entity.Player()
        R.man_queue = man_queue = QueueManager.QueueManager()
        man_queue.queue = queue = []
        for i in range(7):
            creature = Entity.Creature([randint(0,2), 0], (2 + i ,1))
            man_queue.add_entity(creature)
            self.sprites.add(creature)
        
        
    def controls(self):
        
        #keys = pg.key.get_pressed()
        
        
        def pressed(key):
            return self.pressed_key == key #or keys[key]
        
        def m_pressed(mouse):
            return self.mouse_pressed == mouse 
        
        #######
        # KEYBOARD PRESSES
        ####
        if pressed(pg.K_j):
            print "Emily Loves James"
            
        if pressed(pg.K_q):
            attack_next()
            
        if pressed(pg.K_h):
            if Entity.use(player, "hp potion"):
                Entity.heal(player, 10)
        self.pressed_key = None
     
        #####
        # MOUSE PRESSES
        #####
        if m_pressed(1): #1 = mouse button 1
            for thing in queue:
                if thing.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    ap = player.attack_cost
                    Entity.combat(player, thing)
                    man_queue.enemy_turns(ap)
                    break
        self.mouse_pressed = None
        
        
  
    def main(self):
        
        clock = pg.time.Clock()
        
        #updates screen
        pg.display.flip()
        
        self.screen.fill(bg_colour)
        pg.display.flip()
        # main game loop
        while not self.game_over:
            #clear screen
#             self.screen.fill(black)
            
            
            self.sprites.clear(self.screen, self.background) #test
            self.sprites.update() #test
            self.dirties = self.sprites.draw(self.screen) #test
            
            write_health(self) #text print out.
            write_mana(self)
            
            #check to see if we can do anything with the keys pressed or mouse pressed
            self.controls()
            
            
            
            if len(queue) <= 0:
                print "winner, winner, chicken dinner"
                self.game_over = True
                    
#           ##OLD STUFF#
            ##Draw the player and it's health bar.S
#             pg.draw.rect(self.screen, player.colour, player.rect)
#             health_per = 100.0/player.max_hp * player.hp
#             pg.draw.rect(self.screen, (100,20,20), (player.pos[0],player.pos[1] + 105, health_per, 20))

#             for i in range(len(queue)):
#                 thing = queue[i]
#                 thing.rect.x = 200 + i*110
#                 thing.pos = (200 + i*110, 110)
#                 pg.draw.rect(self.screen, thing.colour, thing.rect)
#                 
#                 #draw a health bar
#                 health_per = 100.0/thing.max_hp * thing.hp
#                 pg.draw.rect(self.screen, (100,20,20), (thing.pos[0],thing.pos[1] + 105, health_per, 20))
                    
                    
            clock.tick(15)
            #update screen with changes
            pg.display.update(self.dirties) #test
#             pg.display.flip()
            
            #check for input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                elif event.type == pg.KEYDOWN:
                    self.pressed_key = event.key
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed = event.button
                    self.mouse_pos = event.pos
                
    
def write_health(game):
    label = gamefont.render("Health: " + str(player.hp), 1, (199,178,153))
    game.screen.blit(label, (10, 10))
    label = gamefont.render("Health Potions: " + str(player.inventory.count("hp potion")), 1, (255,255,0))
    game.screen.blit(label, (10, 40))
    game.dirties.append(pg.Rect((10,10),(155, 50)))
    
    
def write_mana(game):
    label = gamefont.render("Mana: " + str(player.mana), 1, (255,255,10))
    game.screen.blit(label, (180, 10))
    label = gamefont.render("Mana Potions: " + str(player.inventory.count("mana potion")), 1, (255,255,0))
    game.screen.blit(label, (180, 40))

if __name__=='__main__':
    R.SPRITE_CACHE = Entity.TileCache()
    
    pg.init()
    pg.display.set_mode((1024,768))
    pg.display.set_caption('1D_RL')
    
    #load font
    gamefont = pg.font.SysFont("monospace", 15)
    Game().main()
    
    
    
    
    