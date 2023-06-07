from objeto import Objeto
from constantes import FANTASMA

class Fantasma(Objeto):
    
    def __init__(self) -> None:
        self.posicao_x = -1
        self.posicao_y = -1
        self.vivo: bool
        self.vulneravel: bool
        self.tipo = FANTASMA
        super().__init__()