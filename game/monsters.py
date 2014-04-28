'''
Created on 27 Apr 2014

@author: Emily
'''
from enums import *


monsters = {
    "ghost" : {
        "name" : "ghost",
        "type" : "undead",
        "tile" : (0, 0),
        "image" : "data/monsters_x24.png",
        "base_stats" : [4, 4, 8, 6, 4, 8, 4],
        "equipment_slots" : []
        },
    
    "pirate" : { 
        "name" : "pirate",
        "type" : "human",
        "tile" : (1, 0),
        "tilesheet" : "data/monsters_x24.png",
        "base_stats" : [7, 7, 11, 8, 10, 3, 9],
        "equipment_slots" : ["helmet","torso", "legs", "gloves", "left-hand", "right-hand"]
        },
    
    "slime" : {
        "name" : "slime",
        "type": "slime",
        "tile" :(2, 0),
        "tilesheet" : "data/monsters_x24.png",
        "base_stats" : [5, 5, 5, 2, 2, 2, 5],
        "equipment_slots" : []
        },
    
    "orc" : {
        "name" : "Orc",
        "type" : "orc",
        "tilesheet" : "data/monsters_2_x24.png",
        "tile" : (0,0),
        "base_stats" : [9, 10, 8, 4, 3, 4, 3],
        "equipment_slots" : ["helmet","torso", "legs", "gloves", "left-hand", "right-hand"], # etc
        "abilities" : [MONS_ATTK.HAND1, MONS_ATTK.HAND2, MONS_ATTK.DART, MONS_ATTK.BOW]
        },
    
    "goblin" : {
        "name" : "Goblin",
        "type" : "goblin",
        "tilesheet" : "data/monsters_2_x24.png",
        "tile" : (1,0),
        "base_stats" : [6, 5, 6, 6, 3, 4, 3],
        "equipment_slots" : ["helmet","torso", "legs", "gloves", "left-hand", "right-hand"], 
        "abilities" : [MONS_ATTK.HAND1, MONS_ATTK.DART, MONS_ATTK.BOW]
    }
}


