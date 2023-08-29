from objeto import Objeto
from constantes import FRUTA

class Fruta(Objeto):
    
    def __init__(self) -> None:
        super().__init__()
        self.tipo = FRUTA
        self.carregar_imagem('cereja.png', self.tamanho)