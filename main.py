import os
import pygame

from pygame.locals import *
from pacman import Pacman
from fantasma import Fantasma
from parede import Parede
from trilha import Trilha
from constantes import *
from fase import Fase
from fases.fase_1 import Fase1
from fases.fase_2 import Fase2
from fases.fase_3 import Fase3
from fases.fase_4 import Fase4


class App():
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 800, 800
        self._display_game = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_game.fill((255, 255, 255))
        pygame.display.set_caption("PacMan")
        
        self._running = True
        self.color = (255,255,255)
        self.rect_color = (255,0,0)
        
        self.pacman = Pacman()
        self.vermelho = Fantasma()
        self.azul = Fantasma()
        self.rosa = Fantasma()
        self.laranja = Fantasma()
        self.paredes = []
        self.trilha = []
        self.lista_obj = []
        
        self.fase_1 = Fase()
        self.fase_2 = Fase()
        self.fase_3 = Fase()
        self.fase_4 = Fase()
        
    
    def panic(self, mensagem):
        print(mensagem)
        self._running = False
    
    def adicionar_obj(self, obj):
        self.lista_obj.append(obj)
    
    def render_matrix(self, matriz, matriz_x, matriz_y):
        # print(matriz)
        # print(matriz_x)
        # print(matriz_y)
        if(matriz_x != matriz_y):
            self.panic("Matiz x diferente de y")
        
        if(self.width != self.height):
            self.panic("Tamanho da tela não é um quadrado")
        
        s = self.width/matriz_x
        self.size = s
        
        # print(s)
        for i in range(matriz_y):
            for j in range(matriz_x):
                y = i*s
                x = j*s
                if(matriz[i][j] == 4):
                    # pygame.draw.circle(self._display_game, (0, 0, 255), (250, 250), 75)
                    pygame.draw.rect(self._display_game, (255, 0, 0), (x, y, s, s))
                    
                if(matriz[i][j] == 3):
                    pygame.draw.rect(self._display_game, (0, 0, 255), (x, y, s, s))
                    
    def carregar_fase(self):
        contador_fantasma = 0
        frameAtual = 0
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                if(self.matriz[i][j] == 1):
                    self.pacman.posicao_x = j*self.size
                    self.pacman.posicao_y = i*self.size
                    self.matriz[i][j] = TRILHA
                    
                    self.lista_obj.append(self.pacman)
                    
                    print(self.pacman.posicao_x)
                    print(self.pacman.posicao_y)
                    # imagemPacman = self.pacman.loadGIF("./imagens/pacman-gif.gif")
                    # rect = imagemPacman[frameAtual].get_rect(center = (self.pacman.posicao_x, self.pacman.posicao_y))
                    # self._display_game.blit(imagemPacman[frameAtual], rect)
                    # frameAtual = (frameAtual + 1) % len(imagemPacman)


                if(self.matriz[i][j] == 2):
                    self.verifica_carregou_posicao_fantasma(x=j, y=i, contador_fantasma=contador_fantasma)
                    contador_fantasma += 1
        
    def verifica_carregou_posicao_fantasma(self, x, y, contador_fantasma):
        if(contador_fantasma == 0):
            self.azul.posicao_x = x
            self.azul.posicao_y = y
            self.lista_obj.append(self.azul)

        elif(contador_fantasma == 1):
            self.laranja.posicao_x = x 
            self.laranja.posicao_y = y
            self.lista_obj.append(self.laranja)

        elif(contador_fantasma == 2):
            self.vermelho.posicao_x = x 
            self.vermelho.posicao_y = y
            self.lista_obj.append(self.vermelho)

        elif(contador_fantasma == 3):
            self.rosa.posicao_x = x 
            self.rosa.posicao_y = y
            self.lista_obj.append(self.rosa)


    def on_init(self):
        
        self._running = True
        
        # self.fase_1.populaObjetosMatriz(matriz=Fase1.get_matriz())

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                self._running = False
            else:
                self.click_botoes(event=event)


            print(self.pacman.posicao_x)
            print(self.pacman.posicao_y)
            pygame.display.update()

        if event.type == pygame.QUIT:
            self._running = False

    def click_botoes(self, event):
        
        if event.key == pygame.K_LEFT:
            if(self.matriz[int(self.pacman.posicao_y/self.size)][int(self.pacman.posicao_x/self.size) - 1] != PAREDE):
                self.pacman.velocidade_x = -self.size
                self.pacman.velocidade_y = 0
            
        elif event.key == pygame.K_RIGHT:
            if(self.matriz[int(self.pacman.posicao_y/self.size)][int(self.pacman.posicao_x/self.size) + 1] != 4):
                self.pacman.velocidade_x = self.size
                self.pacman.velocidade_y = 0

        elif event.key == pygame.K_DOWN:
            if(self.matriz[int(self.pacman.posicao_y/self.size) + 1][int(self.pacman.posicao_x/self.size)] != 4):
                self.pacman.velocidade_y = self.size
                self.pacman.velocidade_x = 0
            
        elif event.key == pygame.K_UP:
            if(self.matriz[int(self.pacman.posicao_y/self.size) - 1][int(self.pacman.posicao_x/self.size)] != 4):
                self.pacman.velocidade_y = -self.size
                self.pacman.velocidade_x = 0

    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
    
    def renderizar(self):
        self.fps = pygame.time.Clock().tick(3)/1000.0
        for obj in self.lista_obj:
            obj.definirPosicoes()
            
        self._display_game.fill((0, 0, 0))
        self.matriz = FASE_1
        self.render_matrix(matriz=self.matriz, matriz_x=16, matriz_y=16)
        self.carregar_fase()
        for obj in self.lista_obj:
            obj.imprimirObj(display_game=self._display_game)
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            
            
            
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.renderizar()
            
            
            # self._display_game.blit(image, (0, 0))
            # pygame.draw.rect(self._display_game, (255, 0, 0), (self.pacman.posicao_x, self.pacman.posicao_y, self.width, self.height))
        
            pygame.display.update()
        self.on_cleanup()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()