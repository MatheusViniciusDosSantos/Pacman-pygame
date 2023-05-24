import pygame

from pygame.locals import *
from pacman import Pacman
from fantasma import Fantasma
from parede import Parede
from trilha import Trilha
from fase import Fase

class App:
    def __init__(self):
        self._running = True
        self._display_game = None
        self.size = self.weight, self.height = 1200, 800
        self.color = (255,255,255)
        self.rect_color = (255,0,0)
        
        self.pacman = Pacman()
        self.vermelho = Fantasma()
        self.azul = Fantasma()
        self.rosa = Fantasma()
        self.laranja = Fantasma()
        self.paredes = []
        self.trilha = []
        
        self.fase_1 = Fase()
        self.fase_2 = Fase()
        self.fase_3 = Fase()
        self.fase_4 = Fase()

    def on_init(self):
        pygame.init()
        self._display_game = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("PacMan")
        self._running = True

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_UP:
                pass

        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        
            pygame.display.update()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()