'''
Created on 13 Apr 2014

@author: Emily
'''
import pygame as pg


tile_size = 24
MAP_TILE_WIDTH = 100
MAP_TILE_HEIGHT = 100


player = None


man_queue = None


tes = None



SPRITE_CACHE = None


## USER EVENTS

DEADTHINGSEVENT = pg.USEREVENT + 1
UIEVENT = pg.USEREVENT + 2