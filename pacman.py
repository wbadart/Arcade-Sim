import pygame, sys, os, random
from pygame.locals import *

BLOWUP = 0
shooting = 0
MOVE_DISTANCE = 8
HIT_POINTS = 50
BLACK = (0,0,0)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_PATH = '~/paradigms/final/Arcade-Sim/img/'

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(IMG_PATH + 'pacman-d 1.gif').convert()
        self.rect = self.image.get_rect()




class gameSpace:
    def main(self):

        #Initialize Screen
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.size = (self.width, self.height)
        self.screen=pygame.display.set_mode((500,400),0,32)

        self.clock = pygame.time.Clock()

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()

            #for sprite in sprite_list:
                #sprite.tick()

            self.screen.fill(BLACK)
            pygame.display.flip()

if __name__=='__main__':
    gs = gameSpace()
    gs.main()