'''
Created on 26 Jun 2014

@author: Emily
'''

#TODO: Implement a way for status effects to be applied to the player - e.g., poison takes a while to be rid of.


def healing(entity_using):
    entity_using.stats.update_health(30, "holy") #TODO: tap into skills for scaling of this affect.
    
def poison(entity_using):
    entity_using.stats.update_health(-30, "poison") #TODO: tap into skills for scaling of this affect, eg poison resistance..

def perm_increase_health(entity_using):
    assert NotImplementedError #TODO: write in the capability to permanently increase health.