from objeto import Objeto
from constantes import TRILHA

class Trilha(Objeto):
    def __init__(self) -> None:
        super().__init__()
        self.tipo = TRILHA
        self.carregar_imagem('trilha.png', self.tamanho)