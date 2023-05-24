from fisica import Fisica

class Objeto(Fisica):
    def __init__(self) -> None:
        self.id: int
        self.tipo: int
        self.posicao_atual = []
        self.velocidade_atual: float

        super().__init__()
