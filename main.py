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
        self.largura = 800
        self.altura = 800
        self.tamanho_bloco_trilha = self.largura/16
        self._tela_do_jogo = pygame.display.set_mode((self.largura, self.altura), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._tela_do_jogo.fill((255, 255, 255))
        pygame.display.set_caption("PacMan")
        
        self._rodando_jogo = True
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
    
    def ao_iniciar(self):
        self._rodando_jogo = True
    
    def ao_executar(self):
        self.carregar()
        if self.ao_iniciar() == False:
            self._rodando_jogo = False

        while( self._rodando_jogo ):
            
            for event in pygame.event.get():
                self.no_evento(event)
            self.calculos_fisica()
            self.renderizar()

            # self._display_game.blit(image, (0, 0))
            # pygame.draw.rect(self._display_game, (255, 0, 0), (self.pacman.posicao_x, self.pacman.posicao_y, self.width, self.height))

            pygame.display.update()
        self.ao_finalizar()
    
    def carregar(self):
        self.matriz = FASE_1
        self.carregar_fase()
    
    def carregar_fase(self):
        contador_fantasma = 0
        frameAtual = 0
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                if(self.matriz[i][j] == 1):
                    self.pacman.posicao_x = j*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
                    self.pacman.posicao_y = i*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
                    self.matriz[i][j] = TRILHA
                    
                    self.adicionar_obj(self.pacman)
                    
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
            self.adicionar_obj(self.azul)

        elif(contador_fantasma == 1):
            self.laranja.posicao_x = x 
            self.laranja.posicao_y = y
            self.adicionar_obj(self.laranja)

        elif(contador_fantasma == 2):
            self.vermelho.posicao_x = x 
            self.vermelho.posicao_y = y
            self.adicionar_obj(self.vermelho)

        elif(contador_fantasma == 3):
            self.rosa.posicao_x = x 
            self.rosa.posicao_y = y
            self.adicionar_obj(self.rosa)
    
    def no_evento(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                self._rodando_jogo = False
            else:
                self.click_botoes(event=event)

            print(str(self.pacman.posicao_x) + "é o x")
            print(self.pacman.posicao_y)
            pygame.display.update()

        if event.type == pygame.QUIT:
            self._rodando_jogo = False
    
    def click_botoes(self, event):
        if event.key == pygame.K_LEFT:
            self.pacman.velocidade_x = -self.tamanho_bloco_trilha/25
            self.pacman.velocidade_y = 0
            
        elif event.key == pygame.K_RIGHT:
            self.pacman.velocidade_x = self.tamanho_bloco_trilha/25
            self.pacman.velocidade_y = 0

        elif event.key == pygame.K_DOWN:
            self.pacman.velocidade_y = self.tamanho_bloco_trilha/25
            self.pacman.velocidade_x = 0
            
        elif event.key == pygame.K_UP:
            self.pacman.velocidade_y = -self.tamanho_bloco_trilha/25
            self.pacman.velocidade_x = 0
    
    def validar_posicoes (self):
        pass
    
    def calculos_fisica(self):
        dt = pygame.time.Clock().tick(100)/10.0
        for obj in self.lista_obj:
            obj.definirPosicoes(dt)
        self.validar_posicoes()


    def renderizar(self):
        self._tela_do_jogo.fill((0, 0, 0))

        self.renderizar_matriz(matriz=self.matriz, matriz_x=16, matriz_y=16)

        for obj in self.lista_obj:
            obj.imprimirObj(display_game=self._tela_do_jogo)
    
    def renderizar_matriz(self, matriz, matriz_x, matriz_y):

        if(matriz_x != matriz_y):
            self.imprimir_erro_finalizar_jogo("Matiz x diferente de y")
        
        if(self.largura != self.altura):
            self.imprimir_erro_finalizar_jogo("Tamanho da tela não é um quadrado")

        for i in range(matriz_y):
            for j in range(matriz_x):
                y = i*self.tamanho_bloco_trilha
                x = j*self.tamanho_bloco_trilha
                if(matriz[i][j] == 4):
                    # pygame.draw.circle(self._display_game, (0, 0, 255), (250, 250), 75)
                    pygame.draw.rect(self._tela_do_jogo, (255, 0, 0), (x, y, self.tamanho_bloco_trilha, self.tamanho_bloco_trilha))
                    
                if(matriz[i][j] == 3):
                    pygame.draw.rect(self._tela_do_jogo, (0, 0, 255), (x, y, self.tamanho_bloco_trilha, self.tamanho_bloco_trilha))
    
    def imprimir_erro_finalizar_jogo(self, mensagem):
        print(mensagem)
        self._rodando_jogo = False
    
    def adicionar_obj(self, obj):
        self.lista_obj.append(obj)

    def ao_finalizar(self):
        pygame.quit()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.ao_executar()