class Fisica:
        
    def calcularVelocidade(self, posicao_inicial, posicao_final, tempo_inicial, tempo_final):
        return ((posicao_final - posicao_inicial)/(tempo_final - tempo_inicial))
    
    def calculoDeslocamento(self, posicao_inicial, velocidade, tempo_inicial, tempo_final):
        return posicao_inicial + (velocidade * (tempo_final - tempo_inicial))
    
    matriz = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0],
    ]