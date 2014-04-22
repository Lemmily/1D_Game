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

import Render

from random import randint


###
##SAVEGAME TESTING
###
import pickle 
import shelve


###
# PROFILING THINGS
###
import pstats
import cProfile


gamefont = None
black = 0, 0, 0
white = 255, 255, 255
bg_colour = 33, 100, 117 


        
def attack_next():
    if len(queue) > 0:
        ap = player.base_attack_cost
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
        self.sprites = Render.SortedUpdates()
        self.tiles = Render.SortedUpdates()
        
        
        self.ap = 0
        
        self.background = pygame.Surface((1024, 768))
        self.background.fill(bg_colour)
        
        self.dirties = None #holds the dirty bits for updating when rendered.
        
        R.player = player = Entity.Player()
        self.sprites.add(player.sprite, player.health_bar)
        R.man_queue = man_queue = QueueManager.QueueManager()
        man_queue.queue = queue = []
        
        square = Render.DummyObject(R.SPRITE_CACHE["data/floor_tiles_x24.png"], (0, 1), [0,0])
        self.background.blit(square.image, square.rect.topleft)
        
        for i in range(7):
            square = Render.DummyObject(R.SPRITE_CACHE["data/floor_tiles_x24.png"], (2 + i ,1), [0,0])
            creature = Entity.Creature([randint(0,2), 0], (2 + i ,1))
            man_queue.add_entity(creature)
            self.background.blit(square.image, square.rect.topleft)
            self.sprites.add(creature.sprite, creature.health_bar)
        
        
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
                for thing in queue:
                    ap = 3 # arbitrary number of ap for potion use
                    man_queue.enemy_turns(ap)
                    self.ap += ap
                    break
                    
        if pressed(pg.K_g):
            if player.mana > player.heal_spell_cost:
                heal = randint(5,10)
                Entity.heal(player, heal)
                player.update_mana(-30)
                print "You cast your healing spell. Regaining "+ str(heal) + " health."
                        
        self.pressed_key = None
     
        #######
        # MOUSE PRESSES
        #####
        if m_pressed(1): #1 = mouse button 1
            for thing in queue:
                if thing.sprite.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    if queue.index(thing) == 0:
                        ap = player.base_attack_cost/player.stats.attr["dex"].value
                        Entity.combat(player, thing)
                        man_queue.enemy_turns(ap)
                        break
                    else:
                        ap = player.base_ranged_attack_cost/player.stats.attr["dex"].value
                        Entity.ranged_combat(player, thing)
                        man_queue.enemy_turns(ap)
                        break
                    break
        self.mouse_pressed = None
        
        
  
    def main(self):
        
        clock = pg.time.Clock()
        
        #updates screen
        self.screen.blit(self.background, (0,0))
        write_info(self)
        pg.display.flip()
        # main game loop
        while not self.game_over:
            #clear screen
            self.sprites.clear(self.screen, self.background) #test
            #self.screen.fill(bg_colour)
            #self.screen.blit(self.background,(0,0))
            
            cleaner = pg.Surface((1000, 40))
            cleaner.fill(bg_colour)
            self.screen.blit(cleaner, pg.Rect((10,200),(1000, 40)))
             
            self.sprites.update() 
            self.sprites.draw(self.screen)
            
            #check to see if we can do anything with the keys pressed or mouse pressed
            self.controls()
            
            self.dirties =  [pg.Rect(0,100,1000, 140)] #entire area where monsters are and health bars.

            #self.dirties.append(pg.Rect(0,200,1000, 40))
     
            
            #check for input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                elif event.type == pg.KEYDOWN:
                    self.pressed_key = event.key
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed = event.button
                    self.mouse_pos = event.pos
                
                elif event.type == R.DEADTHINGSEVENT:
                    print "hello my pretties"
                    for obj in event.dead:
                        self.sprites.remove(obj.sprite, obj.health_bar)
                    for obj in event.new:
                        self.sprites.add(obj.sprite, obj.health_bar)
                        
                elif event.type == R.UIEVENT:
                    
                    #TODO: give the event flags - what part of the ui is updating?
                    print "oh the health updated!"
                    #TODO: Crude explicit cleaning of the screen. How could this be done better?
                    cleaner = pg.Surface((400, 50))
                    cleaner.fill(bg_colour)
                    self.screen.blit(cleaner,pg.Rect((10,10),(400, 50)))
                    self.dirties.append(write_info(self)) #text print out.
                    
                   
            clock.tick(15) 
            #update screen with changes
            pg.display.update(self.dirties) 
                    
            #check for a win
            if len(queue) <= 0:
                print "winner, winner, chicken dinner, you killed: " + str(man_queue.killed)
                self.game_over = True
                
            if player.check_alive() == False:
                print "LOOOOOO-SER, you only killed: " + str(man_queue.killed)
                self.game_over = True
                
            self.dirties = []
            
        return 0
                

def write_info(game):
    '''
    writes all player health related info to the screen.
    numerical values for health points and number of health potions remaining
    graphical bar representing percentage of health remaining, similar to the creep health bars
    writes all player related mana info to the screen,
    numerical values for mana points and number of mana potions remaining
    graphical representation of percentage of mana remaining ---not yet implemented
    '''
    
    label = gamefont.render("Health: " + str(player.hp), 1, (199,178,153))
    game.screen.blit(label, (10, 10))
    label = gamefont.render("Mana: " + str(player.mana), 1, (255,255,10))
    game.screen.blit(label, (180, 10))
    label = gamefont.render("Mana Potions: " + str(player.inventory.count("mana potion")), 1, (255,255,0))
    game.screen.blit(label, (180, 40))
    
    return pg.Rect((10,10),(400, 50))
    
    
def write_ap(game):
    '''
    writes a count of the total action_points spent by player to the screen
    '''
    label = gamefont.render("AP spent: " + str(game.ap), 1, (255,255,10))
    game.screen.blit(label, (10, 70))


if __name__=='__main__':
    #create sprite cache to hold images later
    R.SPRITE_CACHE = Render.TileCache()
    
    pg.init()
    #set the window size
    pg.display.set_mode((1024,768))
    #set the window title
    pg.display.set_caption('1D_RL')
    
    #load a font
    gamefont = pg.font.SysFont("monospace", 15)
    
    
    #normal operation
    Game().main()
    
    #for profiling runs.
#     profiler = cProfile.run("Game().main()","profile")
#     #PRINTS OUT PROFILE INFO
#     p = pstats.Stats("profile")
#     p.sort_stats("calls", "cumulative")
#     p.print_stats()

    
    
    