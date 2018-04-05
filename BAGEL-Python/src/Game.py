import pygame, sys
from pygame.locals import * # contains constants like QUIT, K_UP, etc.
from Sprite   import *
from Label    import *
from Input    import *
from Group    import *
from random   import * # contains randint function

class Game(object):

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.windowSize = (800, 600)
        self.windowMode = pygame.locals.DOUBLEBUF # much better than default (0)
        self.displaySurface = pygame.display.set_mode(self.windowSize, self.windowMode)
        self.running = True
        self.input = Input()
        self.group = Group()
        self.clearColor = (255,255,255)
        self.deltaTime = 0
        # display FPS
        self.fpsDisplay = False
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

    def setTitle(self, title):
        pygame.display.set_caption(title)

    def setWindowSize(self, width, height):
        pygame.display.set_mode( (width,height) )
        
    def create(self):
        pass # implement by extending class
        
    def update(self):
        pass # implement by extending class
        
    def run(self):
        self.create()
        self.gameloop()

    def gameloop(self):
        
        while self.running:

            # process input
            eventList = pygame.event.get()  # remove the events in the queue and return them inside a list
            self.input.update(eventList)
            for event in eventList:
                if event.type == pygame.locals.QUIT:
                    self.running = False

            # update game state
            self.update()
            self.group.act(self.deltaTime)

            # render images to screen
            self.displaySurface.fill( self.clearColor ) # clear screen
            self.group.draw( self.displaySurface ) # draw objects

            if (self.fpsDisplay): # display FPS
                font = pygame.font.Font(None, 24)
                fpsValue = int(self.fpsClock.get_fps())
                fps = font.render("FPS: " + str(fpsValue), True, pygame.Color('black'))
                self.displaySurface.blit(fps, (11, 11))
                fps = font.render("FPS: " + str(fpsValue), True, pygame.Color('red'))
                self.displaySurface.blit(fps, (10, 10))

            pygame.display.update() # similar to flip() - switches buffers
            
            # sleep according to desired frame rate
            self.deltaTime = self.fpsClock.tick(self.fps) / 1000.0
            
        pygame.quit()
        sys.exit()  
            
