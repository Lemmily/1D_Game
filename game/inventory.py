'''
Created on 13 Apr 2014

@author: Emily
'''



class Inventory(object):
    
    def __init__(self):
        self.contents = {}
        
    def get(self, _type):
        if self.contents.has_key(_type) and self.contents[_type] > 0:
            self.contents[_type] -= 1
            return True
        else:
            return False
    
    def has(self, _type):
        if self.contents.has_key(_type) and self.contents[_type] > 0:
            return True
        else:
            return False
        
    def drop(self, _type):
        #temporarily does the same thing as the get function.
        if self.contents.has_key(_type) and self.contents[_type] > 0:
            self.contents[_type] -= 1
            return True
        else:
            return False
        
        
    
    
    