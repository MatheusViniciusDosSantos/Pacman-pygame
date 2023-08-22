from objeto import Objeto
import random
from constantes import FANTASMA, PAREDE
from direcao import direcao

class Fantasma(Objeto):
    
    def __init__(self) -> None:
        super().__init__()
        self.posicao_x = -1
        self.posicao_y = -1
        self.vivo: bool
        self.vulneravel: bool
        self.tipo = FANTASMA
        self.cor = 0
        self.tempo_espera = 10
        self.quantidade_casas_andar = 0

    def define_proxima_direcao(self, tamanho_bloco_trilha, limiar, velocidade_base, matriz):
        if (self.tempo_espera == 0):
            celula_x = int(self.posicao_x / tamanho_bloco_trilha)
            meio_celula_x = (celula_x + 0.5) * tamanho_bloco_trilha
            meio_maior_bloco_x = meio_celula_x + limiar
            meio_menor_bloco_x = meio_celula_x - limiar

            celula_y = int(self.posicao_y / tamanho_bloco_trilha)
            meio_celula_y = (celula_y + 0.5) * tamanho_bloco_trilha
            meio_maior_bloco_y = meio_celula_y + limiar
            meio_menor_bloco_y = meio_celula_y - limiar

            vetor_proxima_direcao = self.monta_vetor_proxima_direcao(
                esquerda=matriz[celula_y][celula_x - 1],
                direita=matriz[celula_y][celula_x + 1],
                cima=matriz[celula_y - 1][celula_x],
                baixo=matriz[celula_y + 1][celula_x],
                meio_maior_bloco_x=meio_maior_bloco_x,
                meio_menor_bloco_x=meio_menor_bloco_x,
                meio_maior_bloco_y=meio_maior_bloco_y,
                meio_menor_bloco_y=meio_menor_bloco_y
            )

            proxima_direcao = random.choice(vetor_proxima_direcao)

            self.muda_direcao(proxima_direcao=proxima_direcao, velocidade_base=velocidade_base)

            self.tempo_espera = 10

        elif(self.tempo_espera > 0) :
            self.tempo_espera -= 1

    def muda_direcao(self, proxima_direcao, velocidade_base):
        if (proxima_direcao == direcao.CIMA):
            self.velocidade_y = -velocidade_base
            self.velocidade_x = 0

        elif (proxima_direcao == direcao.BAIXO):
            self.velocidade_y = velocidade_base
            self.velocidade_x = 0

        elif (proxima_direcao == direcao.ESQUERDA):
            self.velocidade_x = -velocidade_base
            self.velocidade_y = 0

        elif (proxima_direcao == direcao.DIREITA):
            self.velocidade_x = velocidade_base
            self.velocidade_y = 0

    def monta_vetor_proxima_direcao(
        self, esquerda, direita, cima, baixo, meio_maior_bloco_x,
        meio_menor_bloco_x, meio_maior_bloco_y, meio_menor_bloco_y
    ):
        posicoes_possiveis_proxima_direcao = []
        if (self.velocidade_x != 0.0):
            if (esquerda != PAREDE and self.velocidade_x < 0.0):
                posicoes_possiveis_proxima_direcao.extend([direcao.ESQUERDA, direcao.ESQUERDA, direcao.ESQUERDA, direcao.ESQUERDA])
            if (direita != PAREDE and self.velocidade_x > 0.0):
                posicoes_possiveis_proxima_direcao.extend([direcao.DIREITA, direcao.DIREITA, direcao.DIREITA, direcao.DIREITA])
        if (self.velocidade_y != 0.0):
            if (cima != PAREDE and self.velocidade_y < 0.0):
                posicoes_possiveis_proxima_direcao.extend([direcao.CIMA, direcao.CIMA, direcao.CIMA, direcao.CIMA])
            if (baixo != PAREDE and self.velocidade_y > 0.0):
                posicoes_possiveis_proxima_direcao.extend([direcao.BAIXO, direcao.BAIXO, direcao.BAIXO, direcao.BAIXO])

        if (cima != PAREDE  and (
            meio_maior_bloco_x > self.posicao_x > meio_menor_bloco_x
            )):
            posicoes_possiveis_proxima_direcao.append(direcao.CIMA)
        if (baixo != PAREDE and (
            meio_maior_bloco_x > self.posicao_x > meio_menor_bloco_x
            )):
            posicoes_possiveis_proxima_direcao.append(direcao.BAIXO)
        if (esquerda != PAREDE and (
            meio_maior_bloco_y > self.posicao_y > meio_menor_bloco_y
            )):
                posicoes_possiveis_proxima_direcao.append(direcao.ESQUERDA)
        if (direita != PAREDE and (
            meio_maior_bloco_y > self.posicao_y > meio_menor_bloco_y
            )):
            posicoes_possiveis_proxima_direcao.append(direcao.DIREITA)

        return posicoes_possiveis_proxima_direcao