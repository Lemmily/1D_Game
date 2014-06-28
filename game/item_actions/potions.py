'''
Created on 26 Jun 2014

@author: Emily
'''


def healing(entity_using):
    entity_using.stats.update_health(30, "holy") #TODO: tap into skills for scaling of this affect.
    
def poison(entity_using):
    entity_using.stats.update_health(-30, "poison") #TODO: tap into skills for scaling of this affect, eg posion resistance..