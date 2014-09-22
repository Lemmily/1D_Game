'''
Created on 12 Apr 2014

@author: James & Emily

'''

import pygame as pg
import reg as R
from random import randint

from inventory import Inventory

import render
import util


class Entity(object):
    def __init__(self, pos=(0, 0), frames=None, sprite_pos=[0, 0]):
        """Base object for entities. Especially Player and Creature - may be used for map objects in future. but health type things will need to not be drawn.
        
        """
        # Sprite things
        self.sprite = render.SpriteTile(pos, frames, sprite_pos)
        self.health_bar = render.Block(96, 20, (100, 20, 20))
        self.health_bar.pos = pos[0], pos[1] + 1


        # ##
        # ALL THIS TO ~~ >END
        # might be moved to stats? things like damage 
        # would be better as an @property method to aggregate all sources - stats, weapons, buffs.
        # ##
        self.stats = Stats(0, 0)
        # self.xp_level = 1
        self.dead = False
        # self.base_hp = 10
        # self.hp = self.max_hp
        # self.melee_attack_dmg = 4
        # self.ranged_attack_dmg = 1

        ###
        #END
        ###

        self.has_melee = True
        self.has_ranged = False
        self.has_magic = False  #only given mana attributes if this is true ?

    def update_health(self, change, dmg_type="true"):  # TODO: dmg_type and resistances.
        print "updating health for " + self.__class__.__name__
        # make sure you can't heal a dead guy.
        if not self.dead and change != 0:
            self.stats.update_health(change)

        # check to see if it's dead
        self.check_alive()

        if not self.dead:
            self.health_bar.resize(96.0 / self.stats.max_hp * self.stats.hp, 20)

        return self.stats.hp

    @property
    def max_hp(self):
        try:
            con = self.stats.attr["con"].value
            value = self.base_hp
            value += ( max(con - 10, 0) / 2) * self.xp_level
            return value

        except:
            return self.stats.base_hp

    def check_alive(self):
        if self.stats.hp <= 0:
            self.dead = True
            return False
        return True

    def update_mana(self, change):
        if change != 0:
            self.mana += change
            # weird if else
            self.mana = self.mana if (self.mana < self.max_mana) else self.max_mana


    # #####
    # ##
    # Alll these below will be affected by the stats changes.
    ###   TODO: Deploy stat changes.
    ######
    def get_attack(self):
        #weapon damage - eg 1d6 , plus weapon attr modifier(Str/Dex) 

        return self.stats.melee_attack_dmg

    def get_ranged_damage(self):
        return self.ranged_attack_dmg


    def get_range(self):
        return 0, 1


class Player(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, (0, 1), R.SPRITE_CACHE["data/monsters_x24.png"], [1, 0])
        # self.sprite = Render.SpriteTile((0,1), R.SPRITE_CACHE["data/monsters_x24.png"], [1,0])

        self.type = kwargs.get("type")
        self.stats = Stats(8, 14)
        self.stats.attr["con"].value = 16
        self.stats.base_hp = util.multi_roll_dice(self.stats.attr["con"].value, 6) + self.stats.attr["con"].value
        self.stats.hp = self.max_hp
        self.max_mana = self.stats.attr["int"].value * 11
        self.mana = self.max_mana

        self.melee_attack_dmg = self.stats.attr["str"].value / 2
        self.ranged_attack_dmg = self.stats.attr["dex"].value / 3

        self.inventory = Inventory()
        self.inventory.pick_up("hp potion", 3)


        # TEMP: base_attack_cost
        self.base_attack_cost = 150
        self.base_ranged_attack_cost = 300

        self.heal_spell_cost = 40

    def update_health(self, change):
        Entity.update_health(self, change)
        pg.event.post(pg.event.Event(R.UIEVENT, health=True, stats=False))


class Creature(Entity):
    def __init__(self, pos, mons_dict):


        self.type = mons_dict["type"]
        tilesheet = mons_dict["tilesheet"]
        try:
            Entity.__init__(self, pos, R.SPRITE_CACHE[tilesheet], mons_dict["tile"])
        except:
            print "uhuhhhh " + tilesheet + "not there"
        # self.sprite = RenderSpriteTile(pos, R.SPRITE_CACHE["data/monsters_x24.png"], sprite_pos)

        stats = mons_dict["base_stats"]
        if len(stats) < 1:
            self.stats = Stats(3, 9)
        else:
            self.stats = Stats(base=stats)

        self.stats.base_hp = util.multi_roll_dice(self.stats.attr["con"].value, 5) + self.stats.attr["con"].value
        self.stats.hp = self.stats.max_hp
        self.max_mana = util.multi_roll_dice(self.stats.attr["int"].value, 3)
        self.mana = self.max_mana

        self.action_points = randint(0, 30)  # will start with one attack worth of AP

        self.melee_cost = 30

        if randint(0, 1) == 1:
            self.has_ranged = True
            self.ranged_cost = 40
            self.ranged_attack_dmg = randint(1, 5)

        if randint(0, 5) == 1:
            self.has_magic = True
            self.max_mana = self.stats.attr["int"].value * 4
            self.mana = self.max_mana

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
        # TODO: decision making.
        # check from shortest -> longest range for now, and just do whatever it can do

        # need a way to store actions, action cost, action range
        if q_position <= 1 and self.action_points > self.melee_cost:
            self.do_melee_attack(q_position)
        elif self.has_ranged and q_position <= 5 and self.action_points > self.ranged_cost:
            self.do_ranged_attack(q_position)


    def do_ranged_attack(self, q_position):
        # TODO: possibly abstract this back an inheritence level - currently *always* attacks player.

        # TODO: attack calculations
        self.use_action_points(self.ranged_cost)
        if randint(0, 5) <= 3:
            damage = self.get_ranged_damage()
            R.player.update_health(-damage)
            print "Enemy " + str(q_position) + " fires it's bow and does " + str(
                damage) + " leaving the player with " + str(R.player.stats.hp)
        else:
            print "Enemy " + str(q_position) + " fumbles its attack!"

    def do_melee_attack(self, q_position):
        # TODO: possibly abstarct this back an inheritence level - currently *always* attacks player.

        # TODO: attack calculations
        self.use_action_points(self.melee_cost)
        if randint(0, 5) <= 3:
            damage = self.get_attack()
            R.player.update_health(-damage)
            print "Enemy " + str(q_position) + " swings it's sword and does " + str(
                damage) + " leaving the player with " + str(R.player.stats.hp)

        else:
            print "Enemy " + str(q_position) + " fumbles its attack!"


attributes = ["str", "con", "dex", "int", "cha", "wis", "luc"]


class Stats:
    def __init__(self, _min=0, _max=0, base=None):
        self.attr = {}
        if base != None:
            self.attr = self.from_base(base)
        else:
            for stat in attributes:
                self.attr[stat] = Attribute(stat, randint(_min, _max))

        self.xp_level = 1
        self.dead = False
        self.base_hp = 10
        self.hp = self.max_hp
        self.melee_attack_dmg = 4
        self.ranged_attack_dmg = 1

    @property
    def max_hp(self):
        try:
            con = self.attr["con"].value
            value = self.base_hp
            value += ( max(con - 10, 0) / 2) * self.xp_level
            return value

        except:
            return self.base_hp

    def update_health(self, change):
        self.hp = self.hp + change
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def from_base(self, base):
        """creates the stats from a set of base stats, these are stored in base in order of attributes."""
        # i = 0
        attr = {}
        for stat in attributes:
            attr[stat] = Attribute(stat, base[1] + randint(-2, 2))
            # i += 1
        return attr


class Attribute():
    def __init__(self, name, value):
        self.name = name
        self.value = value

        @property
        def modifier(self):
            if self.value <= 1:
                return -5
            elif self.value < 4:
                return -4
            elif self.value < 6:
                return -3
            elif self.value < 8:
                return -2
            elif self.value < 10:
                return -1
            elif self.value < 12:
                return 0
            elif self.value < 14:
                return 1
            elif self.value < 16:
                return 2
            elif self.value < 18:
                return 3
            elif self.value <= 20:
                return 5
            elif self.value > 20:
                return 6

    def increase(self, amount = 1):
        self.value += amount

    def increase(self, amount = 1):
        self.value -= 1
        #TODO: check for lower threshold, if stat too low - DEATH









##
#
# ACTIONS
#
##









def combat(attacker, defender):
    '''
    melee combat for attacker(player) and defender
    melee combat damage based on player strength attribute; weapon equipped; player skill points with chosen weapon; crit damage
    crit damage currently defaulted to 10*base damage -----to be refined
    crit chance currently 10% chance with modifier of player dexterity attribute ----to be refined
    '''
    # TODO: actual combat calculations - to hits etc
    # TODO: this maybe needs to be put into queue manager? or something like that?
    # damage = attacker damage + randint from weapon + weapon skill?
    crit = False
    crit_dmg = 0
    if randint(1, 100) + attacker.stats.attr["dex"].value > 90:
        crit = True
        crit_dmg = attacker.get_ranged_damage() * 10
    if crit:
        damage = attacker.get_attack() + randint(1, 10) + crit_dmg
        defender.update_health(-damage)
        print "You swing your weapon and crit, dealing " + str(damage) + " leaving the creature on " + str(defender.stats.hp)
    else:
        damage = attacker.get_attack() + randint(1, 10)
        defender.update_health(-damage)
        #print defender.hp, "/", attacker.hp
        print "You swing your weapon, dealing " + str(damage) + " leaving the creature on " + str(defender.stats.hp)


def ranged_combat(attacker, defender):
    '''
    ranged combat for attacker(player) and defender(creep in queue pos >0)
    ranged combat damage based on player dexterity attribute; weapon equipped; player skill points with chosen weapon; crit damage
    crit damage currently defaulted to 10*base damage -----to be refined
    crit chance currently 10% chance with modifier of player dexterity attribute ----to be refined
    '''
    # damage = attacker damage + randint from weapon + crit chance + weapon skill?
    crit = False
    crit_dmg = 0
    if randint(1, 100) + attacker.stats.attr["dex"].value > 90:
        crit = True
        crit_dmg = attacker.get_ranged_damage() * 10
    if crit:
        damage = attacker.get_ranged_damage() + randint(1, 10) + crit_dmg
        defender.update_health(-damage)
        # print defender.hp, "/", attacker.hp
        print "You fire your bow and crit, dealing " + str(damage) + ", leaving the creature on " + str(defender.stats.hp)
    else:
        damage = attacker.get_ranged_damage() + randint(1, 10) + crit_dmg
        defender.update_health(-damage)
        # print defender.hp, "/", attacker.hp
        print "You fire your bow, dealing " + str(damage) + ", leaving the creature on " + str(defender.stats.hp)



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




