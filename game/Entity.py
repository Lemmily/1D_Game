'''
Created on 12 Apr 2014

@author: James & Emily
'''
import pygame as pg
from random import randint

from Inventory import *


import Reg as R


class TileCache:
    """Load the tilesets lazily into global cache"""
    
    def __init__(self, width = R.tile_size, height = None):
        self.width = width
        self.height = height or width
        self.cache = {}
        
    
    def __getitem__(self, filename):
        """Return a table of files, load it from disk if needed"""
        
        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width, self.height)
            
            self.cache[key] = tile_table
            return tile_table
    
    
    def _load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""
        image = pg.image.load(filename).convert_alpha()
        #image.
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table
    
class SortedUpdates(pg.sprite.RenderUpdates):
    """A sprite group that sorts them by depth."""

    def sprites(self):
        """The list of sprites in the group, sorted by depth."""

        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)


class Sprite(pg.sprite.Sprite):
    is_player = False
    def __init__(self, pos=(0,0), frames=None):
        super(Sprite, self).__init__()
        self.frames = frames
        self.image = frames[0][0]
        self.rect = self.image.get_rect()
        self.animation = None #self.stand_animation()
        self.pos = pos
        self.depth = 0
        
    def stand_animation(self):
        while True:
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None
                
    def update(self, *args):
        pass
        
    @property
    def pos(self):
        self.pos[0], self.pos[1]
        
    def _get_pos(self):
        """check current pos of sprite on map"""
        return (self.rect.x/R.MAP_TILE_WIDTH, self.rect.y/R.MAP_TILE_WIDTH)
        #return (self.pos[0], self.pos[1])
        #return (self.rect.midbottom[0]-R.MAP_TILE_WIDTH/2)/R.MAP_TILE_WIDTH, (self.rect.midbottom[1]-R.MAP_TILE_HEIGHT)/R.MAP_TILE_HEIGHT
    
    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""

        self.rect.topleft = pos[0]*110, pos[1]*R.MAP_TILE_WIDTH  
        
        self.depth = 0 #self.rect.midbottom[1]

    #define the property pos and let it have the above getters and setters.
    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
 
 
class DummyObject(Sprite):
    def __init__(self, frames = None, pos=(0,0), sprite = [0,0]):
        Sprite.__init__(self, pos, self.frames)
        self.image = self.frames[sprite[0]][sprite[1]]
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*4,R.tile_size*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
        
class Entity(Sprite):
    
    def __init__(self, frames = None, pos=(0,0), sprite = [0,0]):
        Sprite.__init__(self, pos, frames)
        ##################
        ##
        ## SPRITE THINGS
        ##
        ####################
        self.image = self.frames[sprite[0]][sprite[1]]
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*4,R.tile_size*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
        
        self.hp = 10
        self.max_hp = 10
        self.mana = 10
        self.max_mana = 10
        

        self.melee_attack_dmg = 4
        self.ranged_attack_dmg = 1
#         self.colour = colour
#         self.size = (100,100)
#         self.pos = pos
#         self.rect = pg.Rect(self.pos,self.size)
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
        Entity.__init__(self, frames = R.SPRITE_CACHE["data/monsters_x24.png"], pos=(0,1), sprite = [1,0])

        self.stats = Stats(8,14)
        self.max_hp = self.stats.attr["con"].value*11
        self.hp = self.max_hp
        self.max_mana = self.stats.attr["int"].value*11
        self.mana = self.max_mana
        
        self.inventory = Inventory()
        self.inventory.pick_up("hp potion", 3)
       
       
        #TEMP: attack_cost
        self.attack_cost = 15
        
        
       
        
class Creature(Entity):
    
    def __init__(self, sprite_loc, pos):
        Entity.__init__(self, R.SPRITE_CACHE["data/monsters_x24.png"], pos, sprite_loc)
        
        self.stats = Stats(3,9)
        self.action_points = randint(0,30)  #will start with one attack worth of AP
        
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
            R.player.update_health(-damage)
            print "Enemy " + str(q_position) + " fires it's bow and does " + str(damage)+ " leaving the player with " + str(R.player.hp) 
        else:
            print "Enemy " + str(q_position) + " fumbles its attack!"
            
    def do_melee_attack(self, q_position):
        #TODO: possibly abstarct this back an inheritence level - currently *always* attacks player.
        
        #TODO: attack calculations
        self.use_action_points(self.melee_cost)
        if randint(0,5) <= 3:
            damage = self.get_attack()
            R.player.update_health(-damage)
            print "Enemy " + str(q_position) + " swings it's sword and does " + str(damage)+ " leaving the player with " + str(R.player.hp)
            
        else:
            print "Enemy " + str(q_position) + " fumbles its attack!"
            
            
attributes = ["str","con","dex","int","cha","wis", "luc"]
            
class Stats:
    def __init__(self, min, max):
        self.attr = {}
        for stat in attributes:
            self.attr[stat] = Attribute(stat,randint(min,max))
            
class Attribute():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
        @property
        def modifier(self):
            if self.value <= 1: return -5
            elif self.value < 4: return -4
            elif self.value < 6: return -3
            elif self.value < 8: return -2
            elif self.value < 10: return -1
            elif self.value < 12: return 0
            elif self.value < 14: return 1
            elif self.value < 16: return 2
            elif self.value < 18: return 3
            elif self.value <= 20: return 5
            elif self.value > 20: return 6
            
        
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

