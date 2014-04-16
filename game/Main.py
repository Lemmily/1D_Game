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


    



gamefont = None
black = 0, 0, 0
white = 255, 255, 255


############################]
# 
# 
# TESTING STUFF
#
#
###################

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
        image = pygame.image.load(filename).convert()
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
    
class SortedUpdates(pygame.sprite.RenderUpdates):
    """A sprite group that sorts them by depth."""

    def sprites(self):
        """The list of sprites in the group, sorted by depth."""

        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)


class Sprite(pygame.sprite.Sprite):
    is_player = False
    def __init__(self, pos=(0,0), frames=None):
        super(Sprite, self).__init__()
        self.frames = frames
        self.image = frames[0][0]
        self.rect = self.image.get_rect()
        self.animation = None #self.stand_animation()
        self.pos = pos
        
    def stand_animation(self):
        while True:
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None
                
    def update(self, *args):
        if self.animation is not None:
            self.animation.next()
        
    def _get_pos(self):
        """check current pos of sprite on map"""
        
        return (self.rect.midbottom[0]-R.MAP_TILE_WIDTH/2)/R.MAP_TILE_WIDTH, (self.rect.midbottom[1]-R.MAP_TILE_HEIGHT)/R.MAP_TILE_HEIGHT
    
    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""

        self.rect.midbottom = pos[0]*R.MAP_TILE_WIDTH+R.MAP_TILE_WIDTH/2, pos[1]*R.MAP_TILE_HEIGHT+R.MAP_TILE_HEIGHT
        self.depth = self.rect.midbottom[1]

    #define the property pos and let it have the above getters and setters.
    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
 
 
class DummyObject(Sprite):
    def __init__(self, pos=(0,0)):
        self.frames = SPRITE_CACHE["data/all_potions_x24.png"]
        Sprite.__init__(self, pos, self.frames)
        self.image = self.frames[0][0]
        
        
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
        self.sprites = SortedUpdates()
        
        sprite = DummyObject()
        self.sprites.add(sprite)
        
        self.background = pygame.Surface((1024, 768))
        self.background.fill(black)
        
        R.player = player = Entity.Player()
        R.man_queue = man_queue = QueueManager.QueueManager()
        R.queue = queue = []
        for i in range(7):
            R.queue.append(Entity.Creature((20,50,20), (200 + i * 110,110)))
        
        
        
        
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
        
        # main game loop
        while not self.game_over:
            #clear screen
            self.screen.fill(black)
#             self.sprites.clear(self.screen, self.background) #test
#             self.sprites.update() #test
#             dirty = self.sprites.draw(self.screen) #test
            
            write_health(self) #text print out.
            write_mana(self)
            
            #check to see if we can do anything with the keys pressed or mouse pressed
            self.controls()
            pg.draw.rect(self.screen, player.colour, player.rect)
            
            #TODO: needs to me moved to queue manager?
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
#             pg.display.update(dirty) #test
            pg.display.flip()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                elif event.type == pg.KEYDOWN:
                    self.pressed_key = event.key
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed = event.button
                    self.mouse_pos = event.pos
                
    
def write_health(game):
    label = gamefont.render("Health: " + str(player.hp), 1, (255,255,10))
    game.screen.blit(label, (10, 10))
    label = gamefont.render("Health Potions: " + str(player.inventory.count("hp potion")), 1, (255,255,0))
    game.screen.blit(label, (10, 40))
    
    
def write_mana(game):
    label = gamefont.render("Mana: " + str(player.mana), 1, (255,255,10))
    game.screen.blit(label, (180, 10))
    label = gamefont.render("Mana Potions: " + str(player.inventory.count("mana potion")), 1, (255,255,0))
    game.screen.blit(label, (180, 40))

if __name__=='__main__':
    SPRITE_CACHE = TileCache()
    
    pg.init()
    pg.display.set_mode((1024,768))
    pg.display.set_caption('1D_RL')
    
    #load font
    gamefont = pygame.font.SysFont("monospace", 15)
    Game().main()
    
    
    
    
    