'''
Created on 27 Apr 2014

@author: Emily
'''

from enums import *

weapons = {
    "longsword":{
                    "tilesheet": "data/items_x24.png",
                    "tile": (0,0),
                    "wearable": { "2hand": ("str", 4), "1hand" : ("str", 6) },
                    "slot": [EQ.WPN_1HAND, EQ.WPN_2HAND],
                    "status": [STATE.CURSED, STATE.UNCURSED],
                    "enchantments": [],
                    "damage": (2,6,2) #(num of dice, size of dice, potential guaranteed extra)
                },
    "dagger": {   
                    #how it can be worn and what restrictions. eg strength has to be at least 3
                    "tilesheet": "data/items_x24.png",
                    "tile": (0,0),
                    "wearable": { "1hand" : ("str", 3) }, 
                    "slot": [EQ.WPN_1HAND], #possible equipment slots
                    "status": [STATE.CURSED, STATE.UNCURSED], #possible states
                    "enchantments": [],
                    "damage": (1,3,2) #(num of dice, size of dice, potential guaranteed extra)
                }
}

armour = {
    "robe":     {
                    "tilesheet": "data/oryx_16bit_fantasy_items_trans.png",
                    "tile": (4,10),
                    "wearable": { "torso": ("str", 3)},
                    "slot": [EQ.BODY], 
                    "status": [STATE.CURSED, STATE.UNCURSED],
                    "enchantments": [],
                    "armour": 2
                },
          
    "leather":{
                    "tilesheet": "data/oryx_16bit_fantasy_items_trans.png",
                    "tile": (1,10),
                    "wearable": { "torso": ("str", 8)},
                    "slot": [EQ.BODY], 
                    "status": [STATE.CURSED, STATE.UNCURSED],
                    "enchantments": [],
                    "armour": 6
                    },
          
    "trousers":{
                    "tilesheet": "data/items_x24.png",
                    "tile": (0,0),
                    "wearable": { "legs": ("str", 5)},
                    "slot": [EQ.LEGS], 
                    "status": [STATE.CURSED, STATE.UNCURSED],
                    "enchantments": [],
                    "armour": 3
                    },
    "hat":{
                    "tilesheet": "data/items_x24.png",
                    "tile": (0,0),
                    "wearable": { "helmet": ("str", 2)},
                    "slot": [EQ.HELMET], 
                    "status": [STATE.CURSED, STATE.UNCURSED],
                    "enchantments": [],
                    "armour": 3
                    }
}

potions = {
           
        "healing": {
                    "tilesheet": "data/all_potions_x24.png",
                    "tile": (0,0),
                    "wearable": {},
                    "slot": None,
                    "status": [STATE.CURSED, STATE.UNCURSED, STATE.BLESSED],
                    "on use": POTION.HEAL_NORMAL
                    }
           }