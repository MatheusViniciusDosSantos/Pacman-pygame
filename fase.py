from constantes import *
from pacman import Pacman
from fantasma import Fantasma
from parede import Parede
from trilha import Trilha
from fruta import Fruta

class Fase():
    
    def __init__(self) -> None:
        self.concluida = False
    
    def populaObjetosMatriz(self, matriz):
        self.pacman = Pacman()
        self.fantasmas = {FANTASMA_AZUL: [], FANTASMA_ROSA: [], FANTASMA_ROSA: [], FANTASMA_LARANJA: []}
        self.paredes = []
        self.trilhas = []
        self.fruta = Fruta()

        for linha in matriz:
            for coluna in linha:
                if coluna == PACMAN:
                    self.pacman.posicao_atual = [linha, coluna]
                elif coluna == FANTASMA:
                    for fantasma in self.fantasmas:
                        if fantasma == []:
                            fantasma = [linha, coluna]
                            break
                elif coluna == TRILHA:
                    self.trilhas.append([linha, coluna])
                elif coluna == PAREDE:
                    self.paredes.append([linha, coluna])
                elif coluna == FRUTA:
                    self.fruta.posicao_atual = [linha, coluna]
        
        return self.pacman, self.fantasmas, self.paredes, self.trilhas, self.fruta
                        