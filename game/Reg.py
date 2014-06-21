'''
Created on 13 Apr 2014

@author: Emily
'''
import pygame as pg


tile_size = 24
MAP_TILE_WIDTH = 96
MAP_TILE_HEIGHT = 96

INV_TILE = 50

player = None


man_queue = None


tes = None



SPRITE_CACHE = None

MONSTER_INFO = {}

ITEM_INFO = {}

## USER EVENTS

DEADTHINGSEVENT = pg.USEREVENT + 1
UIEVENT = pg.USEREVENT + 2 #FLAGS: health, stats


