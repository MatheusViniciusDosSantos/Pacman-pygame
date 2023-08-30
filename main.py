import pygame
from enum import Enum
from direcao import direcao
from pygame.locals import *
from fruta import Fruta
from pacman import Pacman
from fantasma import *
from constantes import *
from fase import Fase
from constantes import FANTASMA, FANTASMA_ROSA, FANTASMA_AZUL, FANTASMA_LARANJA, FANTASMA_VERMELHO, PAREDE
from trilha import Trilha

class App():
    def __init__(self):
        pygame.init()
        self.largura = LARGURA
        self.altura = ALTURA
        self.tamanho_bloco_trilha = TAMANHO_BLOCO_TRILHA
        
        self.velocidade_base = VELOCIDADE_BASE
        self.fps = FPS
        self.tempo_frame = TEMPO_FRAME
        
        self.limiar = LIMIAR
        
        self.tempo_espera_fantasma_vermelho = 10
        self.tempo_espera_fantasma_laranja = 10
        self.tempo_espera_fantasma_azul = 10
        self.tempo_espera_fantasma_rosa = 10

        self._tela_do_jogo = pygame.display.set_mode((self.largura, self.altura), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._tela_do_jogo.fill((255, 255, 255))
        pygame.display.set_caption("PacMan")
        
        self._rodando_jogo = True
        self.color = (255,255,255)
        self.rect_color = (255,0,0)
        
        self.proxima_direcao: direcao = direcao.NENHUMA
        
        self.pacman = Pacman()
        self.pacman.carregar_imagem('pacman-gif.gif', self.pacman.tamanho)
        self.vermelho = Fantasma()
        self.vermelho.carregar_imagem('vermelho.png', self.vermelho.tamanho)
        self.vermelho.cor = FANTASMA_VERMELHO
        self.azul = Fantasma()
        self.azul.carregar_imagem('azul.png', self.azul.tamanho)
        self.azul.cor = FANTASMA_AZUL
        self.rosa = Fantasma()
        self.rosa.carregar_imagem('rosa.png', self.rosa.tamanho)
        self.rosa.cor = FANTASMA_ROSA
        self.laranja = Fantasma()
        self.laranja.carregar_imagem('laranja.png', self.laranja.tamanho)
        self.laranja.cor = FANTASMA_LARANJA
        self.fruta = [Fruta(), Fruta(), Fruta(), Fruta()]
        self.trilha = []
        for i in range(174):
            self.trilha.append(Trilha())

        self.paredes = []
        self.lista_obj = []
        
        self.fase_1 = Fase()
        self.fase_2 = Fase()
        self.fase_3 = Fase()
        self.fase_4 = Fase()
    
    def ao_iniciar(self):
        self._rodando_jogo = True
        pygame.mixer.music.load('sons/intro.mp3')
        pygame.mixer.music.play(-1)
    
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
        contador_fruta = 0
        contador_trilha = 0
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
                
                if(self.matriz[i][j] == FRUTA):
                    self.verifica_carregou_posicao_fruta(x=j, y=i, contador_fruta=contador_fruta)
                    contador_fruta += 1

                if(self.matriz[i][j] == TRILHA):
                    self.verifica_carregou_posicao_trilha(x=j, y=i, contador_trilha=contador_trilha)
                    contador_trilha += 1
    
    def verifica_carregou_posicao_fantasma(self, x, y, contador_fantasma):
        if(contador_fantasma == 0):
            self.azul.posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.azul.posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.azul)

        elif(contador_fantasma == 1):
            self.laranja.posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.laranja.posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.laranja)

        elif(contador_fantasma == 2):
            self.vermelho.posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.vermelho.posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.vermelho)

        elif(contador_fantasma == 3):
            self.rosa.posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.rosa.posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.rosa)
    
    def verifica_carregou_posicao_trilha(self, x, y, contador_trilha):
        if(contador_trilha):
            self.trilha[contador_trilha ].posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.trilha[contador_trilha ].posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.trilha[contador_trilha ])

    def verifica_carregou_posicao_fruta(self, x, y, contador_fruta):
        if(contador_fruta == 0):
            self.fruta[0].posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.fruta[0].posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.fruta[0])

        elif(contador_fruta == 1):
            self.fruta[1].posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.fruta[1].posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.fruta[1])

        elif(contador_fruta == 2):
            self.fruta[2].posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.fruta[2].posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.fruta[2])

        elif(contador_fruta == 3):
            self.fruta[3].posicao_x = x*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.fruta[3].posicao_y = y*self.tamanho_bloco_trilha + self.tamanho_bloco_trilha/2
            self.adicionar_obj(self.fruta[3])

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
            self.proxima_direcao = direcao.ESQUERDA
            
            
        elif event.key == pygame.K_RIGHT:
            self.proxima_direcao = direcao.DIREITA
            

        elif event.key == pygame.K_DOWN:
            self.proxima_direcao = direcao.BAIXO
            
            
        elif event.key == pygame.K_UP:
            self.proxima_direcao = direcao.CIMA
            
    
    def validar_posicoes (self, obj):
        celula_x = int(obj.posicao_x / self.tamanho_bloco_trilha)
        celula_y = int(obj.posicao_y / self.tamanho_bloco_trilha)
        posicao_interna_x = obj.posicao_x % self.tamanho_bloco_trilha
        posicao_interna_y = obj.posicao_y % self.tamanho_bloco_trilha
        if (posicao_interna_x < (self.tamanho_bloco_trilha / 2)):
            if self.matriz[celula_y][celula_x - 1] == PAREDE:
                obj.velocidade_x = 0
                obj.posicao_x = (celula_x + 0.5) * self.tamanho_bloco_trilha
                
        if (posicao_interna_x > (self.tamanho_bloco_trilha / 2)):
            if self.matriz[celula_y][celula_x + 1] == PAREDE:
                obj.velocidade_x = 0
                obj.posicao_x = (celula_x + 0.5) * self.tamanho_bloco_trilha
        
        if (posicao_interna_y < (self.tamanho_bloco_trilha / 2)):
            if self.matriz[celula_y - 1][celula_x] == PAREDE:
                obj.velocidade_y = 0
                obj.posicao_y = (celula_y + 0.5) * self.tamanho_bloco_trilha
                
        if (posicao_interna_y > (self.tamanho_bloco_trilha / 2)):
            if self.matriz[celula_y + 1][celula_x] == PAREDE:
                obj.velocidade_y = 0
                obj.posicao_y = (celula_y + 0.5) * self.tamanho_bloco_trilha
    
    def calculos_fisica(self):
        dt = pygame.time.Clock().tick(self.fps)/1000
        for obj in self.lista_obj:
            obj.definirPosicoes(dt)
            self.mudar_posicao_pacman()
            self.validar_obj_mudar_posica_fantasma(obj=obj)
            self.validar_posicoes(obj)
        self.collision()
    
    def objectsInCollision(self, obj: Objeto, obj_2: Objeto):
        return (abs((obj.posicao_x + self.tamanho_bloco_trilha/2.0) - (obj_2.posicao_x + self.tamanho_bloco_trilha/2.0)) < ((self.tamanho_bloco_trilha + self.tamanho_bloco_trilha) / 2.0) and abs((obj.posicao_y + self.tamanho_bloco_trilha/2.0) - (obj_2.posicao_y + self.tamanho_bloco_trilha/2.0)) < ((self.tamanho_bloco_trilha + self.tamanho_bloco_trilha) / 2.0))


    def objectsCollided(self, obj: Objeto, obj_2: Objeto):
        if (obj.tipo == FANTASMA and obj_2.tipo == PACMAN):
            self.colisao_fantasma(pacman=obj_2)
        elif (obj.tipo == PACMAN and obj_2.tipo == FANTASMA):
            self.colisao_fantasma(pacman=obj)
        elif (obj.tipo == FRUTA and obj_2.tipo == PACMAN):
            self.colisao_fruta(fruta=obj)
        elif (obj.tipo == PACMAN and obj_2.tipo == FRUTA):
            self.colisao_fruta(fruta=obj_2)
        elif (obj.tipo == TRILHA and obj_2.tipo == PACMAN):
            self.colisao_trilha(trilha=obj)
        elif (obj.tipo == PACMAN and obj_2.tipo == TRILHA):
            self.colisao_trilha(trilha=obj_2)

    def collision(self):
        for i in range(0, len(self.lista_obj) - 1):
            for j in range(i+1, len(self.lista_obj)):
                if (self.objectsInCollision(self.lista_obj[j], self.lista_obj[i])):
                    self.objectsCollided(self.lista_obj[j], self.lista_obj[i])
                    break

    def colisao_fantasma(self, pacman: Pacman):
            pacman.ativo = False
            self.lista_obj.remove(pacman)
            exit()

    def colisao_fruta(self, fruta: Fruta):

        if (fruta.ativo == True):
            fruta.carregar_imagem('fundo.png', fruta.tamanho)
            fruta.ativo = False

    def colisao_trilha(self, trilha: Trilha):

        if (trilha.ativo == True):
            trilha.carregar_imagem('fundo.png', trilha.tamanho)
            trilha.ativo = False

    def validar_obj_mudar_posica_fantasma(self, obj):
        if (obj.tipo == FANTASMA):
            obj.define_proxima_direcao(self.tamanho_bloco_trilha, self.limiar, self.velocidade_base, self.matriz)

    def mudar_posicao_pacman(self):
        celula_x = int(self.pacman.posicao_x / self.tamanho_bloco_trilha)
        meio_celula_x = (celula_x + 0.5) * self.tamanho_bloco_trilha
        meio_maior_bloco_x = meio_celula_x + self.limiar
        meio_menor_bloco_x = meio_celula_x - self.limiar
        
        celula_y = int(self.pacman.posicao_y / self.tamanho_bloco_trilha)
        meio_celula_y = (celula_y + 0.5) * self.tamanho_bloco_trilha
        meio_maior_bloco_y = meio_celula_y + self.limiar
        meio_menor_bloco_y = meio_celula_y - self.limiar
        
        if (self.proxima_direcao == direcao.CIMA and (
            meio_maior_bloco_x > self.pacman.posicao_x > meio_menor_bloco_x
            ) and self.matriz[celula_y - 1][celula_x] != PAREDE):
            self.pacman.posicao_x = (celula_x + 0.5) * self.tamanho_bloco_trilha
            self.pacman.velocidade_y = -self.velocidade_base
            self.pacman.velocidade_x = 0
            
        elif (self.proxima_direcao == direcao.BAIXO and (
            meio_maior_bloco_x > self.pacman.posicao_x > meio_menor_bloco_x
            ) and self.matriz[celula_y + 1][celula_x] != PAREDE):
            self.pacman.velocidade_y = self.velocidade_base
            self.pacman.velocidade_x = 0
            
        elif (self.proxima_direcao == direcao.ESQUERDA and (
            meio_maior_bloco_y > self.pacman.posicao_y > meio_menor_bloco_y
            ) and self.matriz[celula_y][celula_x - 1] != PAREDE):
            self.pacman.velocidade_x = -self.velocidade_base
            self.pacman.velocidade_y = 0
        elif (self.proxima_direcao == direcao.DIREITA and (
            meio_maior_bloco_y > self.pacman.posicao_y > meio_menor_bloco_y
            ) and self.matriz[celula_y][celula_x + 1] != PAREDE):
            self.pacman.velocidade_x = self.velocidade_base
            self.pacman.velocidade_y = 0

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