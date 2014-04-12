'''
Created on 12 Apr 2014

@author: james & emily
'''

import sys

import pygame as pg
import pygame.locals




class Game(object):
    
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.pressed_key = None
        self.game_over = False
        self.overlays = pygame.sprite.RenderUpdates
        
    
     
    def main(self):
        clock = pg.time.Clock()
        
        
        pg.display.flip()
        
        # main game loop
        while not self.game_over:
            black = 0, 0, 0
            self.screen.fill(black)
            
            pg.draw.rect(self.screen, (50,50,50), (10,10,50,100))
            clock.tick(15)
            pg.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game_over = True
                
    


if __name__=='__main__':
    pygame.init()
    pygame.display.set_mode((424,320))
    Game().main()