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
    
    def __init__(self, pos=(0,0), frames=None, sprite_pos = [0,0], t_size = R.MAP_TILE_WIDTH):
        super(Sprite, self).__init__()
        self.frames = frames
        if(self.frames != None):
            self.image = frames[sprite_pos[0]][sprite_pos[1]]
        else:
            self.image = pg.Surface([t_size, t_size])
            self.image.fill((100,20,20))
        self.rect = self.image.get_rect()
        self.animation = None #self.stand_animation()
        self.tile_size = t_size
        self.pos = pos
        self.depth = 0
                        
    def update(self, *args):
#         if self.animation is not None:
#             self.animation.next()
        pass
        
    def _get_pos(self):
        """check current pos of sprite on map"""
        return (self.rect.x/self.tile_size, self.rect.y/self.tile_size)
    
    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""
        self.rect.topleft = pos[0]*self.tile_size, pos[1]*self.tile_size
        
        self.depth = 0 #self.rect.midbottom[1]

    #define the property pos and let it have the above getters and setters.
    pos = property(_get_pos, _set_pos)
    
#     def _get_tile_size(self):
#         return self._tilesize
#     def _set_tile_size(self, size):
#         self._tile_size = size
#          
#     tile_size = property(_get_tile_size, _set_tile_size)

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
    def __init__(self, pos=(0,0), frames=None, sprite_pos = [0,0], padding = 0, scaling = 4, offsetX = 0, offsetY = 0, t_size = R.MAP_TILE_WIDTH):
        
        self.padding = padding
        self.offsetX = offsetX
        self.offsetY = offsetY
        
        Sprite.__init__(self, pos, frames, sprite_pos, t_size)
        
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*scaling,R.tile_size*scaling))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
      
    def _get_tile_pos(self):
        """returns as TILE position, IGNORING the offset. position offsetX, offsetY is considered zero"""
        #return (self.offsetX + self.rect.x/(R.MAP_TILE_WIDTH+self.padding), self.offsetY + self.rect.y/(R.MAP_TILE_WIDTH + self.padding))
        return ( self.rect.x/(self.tile_size+self.padding), self.rect.y/(self.tile_size + self.padding))
    
    def _set_tile_pos(self, pos):
        """Stores the position of the PIXEL POSITION X,Y with INCLUDED padding AND offset FROM the given TILE position. """
        self.rect.topleft = (self.offsetX + pos[0]*(self.tile_size + self.padding), #x
                                        self.offsetY  + pos[1]*(self.tile_size + self.padding)) #y
        
    tile_pos = property(_get_tile_pos, _set_tile_pos)
    
    def _get_pix_pos(self):
        """check current pos of sprite on map, returns as PIXEL position"""
        #return (self.offset + self.rect.x/(R.MAP_TILE_WIDTH+self.padding), self.offset + self.rect.y/(R.MAP_TILE_WIDTH + self.padding))
        #return ( (self.rect.x - self.offsetX )/(R.MAP_TILE_WIDTH+self.padding), (self.rect.y - self.offsetY)/(R.MAP_TILE_WIDTH + self.padding))
        return (self.rect.x + self.offsetX, self.rect.y + self.offsetY)
    
    def _set_pix_pos(self, pos):
        """Set the position by the PIXEL POSITION X,Y with INCLUDED padding AND offset FROM the given PIXEL position. """
        self.rect.topleft = (pos[0]*(self.tile_size + self.padding), #x
                                        pos[1]*(self.tile_size + self.padding)) #y
        
        self.depth = 0 #self.rect.midbottom[1] # not used
        
    pos = property(_get_pix_pos, _set_pix_pos)
    
#     @property
#     def tile_size(self):
#         return self._tilesize;
#     
#     @tile_size.setter
#     def _set_tile_size(self, size):
#         self._tile_size = size;
        
   
class SpriteOther(Sprite): 
    def __init__(self, pos=(0,0), frames=None, sprite_pos = [0,0], scaling = 4):
        Sprite.__init__(self, pos, frames, sprite_pos)
        
        topleft = self.rect.topleft
        self.image = pg.transform.scale(self.image, (R.tile_size*scaling,R.tile_size*scaling))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        
        
    def _get_pos(self):
        """check current pos of sprite on screen as a PIXEL LOCATION"""
        #tiles are 100 wide, but buffer of 10 between them
        return (self.rect.x, self.rect.y)
    
    def _set_pos(self, pos):
        """Sets by the PIXEL LOCATION"""
        self.rect.topleft = pos[0], pos[1]
        
        self.depth = 0 #self.rect.midbottom[1]
    pos = property(_get_pos, _set_pos)
 
    
#     def _get_tile_size(self):
#         return self._tilesize;
#     def _set_tile_size(self, size):
#         self._tile_size = size;
#     tile_size = property(_get_tile_size, _set_tile_size)
 
class SpriteGroup():
    """
    Want some kind of thing that can move the whole group of sprites and that you can position them relative to this.
    """
    def __init__(self):
        pass


class Block(Sprite):
    """ Solid colour rectangle
        to set its position do blockInstance.pos = (0,0)
    """
    # Constructor. Pass in the color of the block,
    # and its width and height position
    def __init__(self, width, height, colour):
        # Call the parent class (Sprite) constructor
        Sprite.__init__(self)
        
        
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

