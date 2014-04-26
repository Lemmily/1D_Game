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
import Util


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



#Temp things
gamefont = None
stat_window_font = None
black = 0, 0, 0
white = 255, 255, 255
bg_colour = 33, 100, 117 
inv_bg_colour = 110, 110, 110

stat_page_one = None
stat_page_two = None

STATS_ONE = True

selected_monst = None
        
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
        global stat_page_one, stat_page_two
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
        
        self.inv_background = pygame.Surface((400, 500))
        self.inv_background.fill(inv_bg_colour)
        inv_slot = Render.DummyObject(R.SPRITE_CACHE["data/floor_tiles_x24.png"], (0,1), [0,0])
        self.inv_background.blit(inv_slot, (10,10))
        
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
        
        
        stat_page_one = pg.Surface((400,510))
        stat_page_one.fill((40,50,80))
        
        stat_page_two = pg.Surface((400,510))
        stat_page_two.fill((80,50,40))
        
        
        stat_page_two.blit(stat_page_one, pg.Rect((200,0),(200,30)),pg.Rect((200,0),(200,30)))
        stat_page_one.blit(stat_page_two, pg.Rect((0,0),(200,30)),pg.Rect((0,0),(200,30)))
        
        
    def controls(self):
        global selected_monst
        
        #keys = pg.key.get_pressed()
        
        
        def pressed(key):
            return self.pressed_key == key #or keys[key]
        
        def m_pressed(mouse):
            return self.mouse_pressed == mouse 
        
        #######
        # KEYBOARD PRESSES
        ####
        if pressed(pg.K_j):
            print "Emily Loves James lots"
            
        if pressed(pg.K_q):
            attack_next()
            
        if pressed(pg.K_h):
            if Entity.use(player, "hp potion"):
                Entity.heal(player, 10)
                ap = 3 # arbitrary number of ap for potion use
                man_queue.enemy_turns(ap)
                self.ap += ap
        
        if pressed(pg.K_s):
            pg.event.post(pg.event.Event(R.UIEVENT, stats = True, health = False))
        
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
        if m_pressed(1): #1 = mouse button left click
            for thing in queue:
                if thing.sprite.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    if queue.index(thing) == 0:
                        ap = player.base_attack_cost/player.stats.attr["dex"].value
                        Entity.combat(player, thing)
                        man_queue.enemy_turns(ap)
                    else:
                        ap = player.base_ranged_attack_cost/player.stats.attr["dex"].value
                        Entity.ranged_combat(player, thing)
                        man_queue.enemy_turns(ap)
                    break
        if m_pressed(3): #3 = mouse button right click
            for thing in queue:
                if thing.sprite.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    selected_monst = thing
                    pg.event.post(pg.event.Event(R.UIEVENT, health = False, stats=True))
                    print selected_monst
        self.mouse_pressed = None
        
        
  
    def main(self):
        clock = pg.time.Clock()
        
        #updates screen
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.inv_background, (450,250))
        write_info(self)
        write_inventory(self)
        pg.display.flip()
        # main game loop
        print self.screen.get_rect().height - 250 
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
            
            self.dirties =  [pg.Rect(0,100,1000, 140), pg.Rect((10,248),(400,510))] #entire area where monsters are and health bars.

            #self.dirties.append(pg.Rect(0,200,1000, 40))
     
            
            #check for input events
            self.handle_events()
            
                    
                   
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
    
    
    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                elif event.type == pg.KEYDOWN:
                    self.pressed_key = event.key
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed = event.button
                    self.mouse_pos = event.pos
                
                elif event.type == R.DEADTHINGSEVENT:
                    print "hello my pretties, welcome to death"
                    for obj in event.dead:
                        self.sprites.remove(obj.sprite, obj.health_bar)
                    for obj in event.new:
                        self.sprites.add(obj.sprite, obj.health_bar)
                        
                elif event.type == R.UIEVENT:
                    #TODO: give the event flags - what part of the ui is updating?
                    if event.health: #TODO: this is temporary flag. Will be broken up differently 
                        print "oh the health updated!"
                        #TODO: Crude explicit cleaning of the screen. How could this be done better?
                        cleaner = pg.Surface((400, 50))
                        cleaner.fill(bg_colour)
                        self.screen.blit(cleaner,pg.Rect((10,10),(400, 50)))
                        self.dirties.append(write_info(self)) #text print out.
                    
                    if event.stats:
                        cleaner = pg.Surface((400, 510))
                        cleaner.fill(bg_colour)
                        self.screen.blit(cleaner,pg.Rect((10,250),(400, 510)))
                        
                        self.dirties.append(write_stats_window(self))
                

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
    label = gamefont.render("Health Potions: " + str(player.inventory.count("health potion")), 1, (255,255,0))
    game.screen.blit(label, (10, 40))
    label = gamefont.render("Mana: " + str(player.mana), 1, (255,255,10))
    game.screen.blit(label, (180, 10))
    label = gamefont.render("Mana Potions: " + str(player.inventory.count("mana potion")), 1, (255,255,0))
    game.screen.blit(label, (180, 40))
    
    return pg.Rect((10,10),(400, 50))

def write_inventory(game):
    for i in player.inventory.get_inv():
        slot = pygame.Rect(1000,1000,30,30)
    

def write_stats_window(game):
    print selected_monst
    stat_page = pg.Surface(stat_page_one.get_rect().size)
    
    stat_page.blit(stat_page_one, (0, 0))
    label = gamefont.render("Health: " + str(player.hp) + "/" + str(player.max_hp), 1, (199,178,153))
    stat_page.blit(label, (10, 30))
    
    i = 0
    for stat in player.stats.attr.keys():
        attr = player.stats.attr[stat]
        label = gamefont.render(attr.name + ": " + str(attr.value), 1, (250,178,250))
        stat_page.blit(label, (10, 50 +i*20))
        i += 1
        
    if selected_monst is not None:
        label = gamefont.render("Health: " + str(selected_monst.hp) + "/" + str(selected_monst.max_hp), 1, (199,178,153))
        stat_page.blit(label, (200, 30))
        i = 0
        for stat in selected_monst.stats.attr.keys():
            attr = selected_monst.stats.attr[stat]
            label = gamefont.render(attr.name + ": " + str(attr.value), 1, (250,178,250))
            stat_page.blit(label, (200, 50 +i*20))
            i += 1
            
        
#    else:
#        stat_page.blit(stat_page_two, (0, 0))
#        label = gamefont.render("Health: " + str(player.hp) + "/" + str(player.base_hp), 1, (199,178,153))
#        stat_page.blit(label, (10, 30))
        
    game.screen.blit(stat_page, (10, 248))


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
    
    #load fonts
    gamefont = pg.font.SysFont("monospace", 15)
    stat_window_font = pg.font.SysFont("monospace", 12)
    
    
    #normal operation
    Game().main()
    
    #for profiling runs.
#     profiler = cProfile.run("Game().main()","profile")
#     #PRINTS OUT PROFILE INFO
#     p = pstats.Stats("profile")
#     p.sort_stats("calls", "cumulative")
#     p.print_stats()

    
    
    