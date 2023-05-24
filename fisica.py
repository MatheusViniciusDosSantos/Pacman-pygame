class Fisica:
        
    def calcularVelocidade(self, posicao_inicial, posicao_final, deslocamento_tempo):
        return ((posicao_final - posicao_inicial)/deslocamento_tempo)
    
    def calculoDeslocamento(self, posicao_inicial, velocidade, deslocamento_tempo):
        return posicao_inicial + (velocidade * deslocamento_tempo)
