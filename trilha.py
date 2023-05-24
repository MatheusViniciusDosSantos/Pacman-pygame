from objeto import Objeto
from constantes import TRILHA

class Trilha(Objeto):
    def __init__(self) -> None:
        self.tem_ponto: bool
        self.ponto_melhoria: bool
        self.tipo = TRILHA
        super().__init__()