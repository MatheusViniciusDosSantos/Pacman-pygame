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

    def verificar_continua_mesma_direcao(self, tamanho_bloco_trilha, limiar, velocidade_base, matriz):
        if(self.quantidade_casas_andar == 0):
            self.gerar_novo_valor_aleatorio(tamanho_bloco_trilha, limiar, velocidade_base, matriz)
            self.quantidade_casas_andar = random.randint(1, 5)
        else:
            self.quantidade_casas_andar -= 1

    #TODO - BUG
    def gerar_novo_valor_aleatorio(self, tamanho_bloco_trilha, limiar, velocidade_base, matriz):
        posicao = random.randint(1, 4)
        if (self.tempo_espera == 0):
            self.mudar_posicao_fantasma(direcao(posicao), tamanho_bloco_trilha, limiar, velocidade_base, matriz)
            self.tempo_espera = 10
        elif(self.tempo_espera > 0) :
            self.tempo_espera -= 1


    def mudar_posicao_fantasma(self, proxima_direcao, tamanho_bloco_trilha, limiar, velocidade_base, matriz):
        celula_x = int(self.posicao_x / tamanho_bloco_trilha)
        meio_celula_x = (celula_x + 0.5) * tamanho_bloco_trilha
        meio_maior_bloco_x = meio_celula_x + limiar
        meio_menor_bloco_x = meio_celula_x - limiar
        print(proxima_direcao)
        
        celula_y = int(self.posicao_y / tamanho_bloco_trilha)
        meio_celula_y = (celula_y + 0.5) * tamanho_bloco_trilha
        meio_maior_bloco_y = meio_celula_y + limiar
        meio_menor_bloco_y = meio_celula_y - limiar
        
        if (proxima_direcao == direcao.CIMA and (
            meio_maior_bloco_x > self.posicao_x > meio_menor_bloco_x
            ) and matriz[celula_y - 1][celula_x] != PAREDE):
            self.posicao_x = (celula_x + 0.5) * tamanho_bloco_trilha
            self.velocidade_y = -velocidade_base
            self.velocidade_x = 0
            
        elif (proxima_direcao == direcao.BAIXO and (
            meio_maior_bloco_x > self.posicao_x > meio_menor_bloco_x
            ) and matriz[celula_y + 1][celula_x] != PAREDE):
            self.velocidade_y = velocidade_base
            self.velocidade_x = 0
            
        elif (proxima_direcao == direcao.ESQUERDA and (
            meio_maior_bloco_y > self.posicao_y > meio_menor_bloco_y
            ) and matriz[celula_y][celula_x - 1] != PAREDE):
            self.velocidade_x = -velocidade_base
            self.velocidade_y = 0
        elif (proxima_direcao == direcao.DIREITA and (
            meio_maior_bloco_y > self.posicao_y > meio_menor_bloco_y
            ) and matriz[celula_y][celula_x + 1] != PAREDE):
            self.velocidade_x = velocidade_base
            self.velocidade_y = 0