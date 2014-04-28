'''
Created on 20 Apr 2014

@author: Emily
'''

import Reg as R

import pygame as pg


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
    
    def __init__(self, pos=(0,0), frames=None, sprite_pos = [0,0]):
        super(Sprite, self).__init__()
        self.frames = frames
        self.image = frames[sprite_pos[0]][sprite_pos[1]]
        self.rect = self.image.get_rect()
        self.animation = None #self.stand_animation()
        self.pos = pos
        self.depth = 0
                        
    def update(self, *args):
#         if self.animation is not None:
#             self.animation.next()
        pass
        
    def _get_pos(self):
        """check current pos of sprite on map"""
        #tiles are 100 wide, but buffer of 10 between them
        return (self.rect.x/R.MAP_TILE_WIDTH, self.rect.y/R.MAP_TILE_WIDTH)
    
    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""
#         if pos[0] > 0:
#             x_tens = pos[0]-1
#         else:
#             x_tens = 0
        self.rect.topleft = pos[0]*R.MAP_TILE_WIDTH, pos[1]*R.MAP_TILE_WIDTH
        
        self.depth = 0 #self.rect.midbottom[1]

    #define the property pos and let it have the above getters and setters.
    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
        
    def resize(self,width, height):
        """resize to W x H in pixels"""
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (int(round(width)) ,int(round(height))))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
class SpriteTile(Sprite):
    def __init__(self, pos=(0,0), frames=None, sprite_pos = [0,0]):
        Sprite.__init__(self, pos, frames, sprite_pos)
        
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*4,R.tile_size*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
    def _get_pos(self):
        """check current pos of sprite on map"""
        #tiles are 100 wide, but buffer of 10 between them
        return (self.rect.x/R.MAP_TILE_WIDTH, self.rect.y/R.MAP_TILE_WIDTH)
    
    def _set_pos(self, pos):
        """Set the position by the TILE POSITION X,Y """
#         if pos[0] > 0:
#             x_tens = pos[0]-1
#         else:
#             x_tens = 0
        self.rect.topleft = pos[0]*R.MAP_TILE_WIDTH, pos[1]*R.MAP_TILE_WIDTH
        
        self.depth = 0 #self.rect.midbottom[1]
        
   
class SpriteOther(Sprite): 
    def __init__(self, pos=(0,0), frames=None, sprite_pos = [0,0], scaling = 4):
        Sprite.__init__(self, pos, frames, sprite_pos)
        
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*scaling,R.tile_size*scaling))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
        
    def _get_pos(self):
        """check current pos of sprite on map"""
        #tiles are 100 wide, but buffer of 10 between them
        return (self.rect.x/R.MAP_TILE_WIDTH, self.rect.y/R.MAP_TILE_WIDTH)
    
    def _set_pos(self, pos):
        """Sets by the PIXEL LOCATION"""
        self.rect.topleft = pos[0], pos[1]
        
        self.depth = 0 #self.rect.midbottom[1]
 
 
 
class Block(Sprite):
    """ Solid colour rectangle"""
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, colour):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a colour.
        # This could also be an image loaded from the disk.
        self.image = pg.Surface([width, height])
        self.image.fill(colour)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        
        
class DummyObject(Sprite):
    def __init__(self, frames = None, pos=(0,0), sprite = [0,0]):
        Sprite.__init__(self, pos, frames)
        self.image = self.frames[sprite[0]][sprite[1]]
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*4,R.tile_size*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

