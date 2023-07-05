from objeto import Objeto
from constantes import PACMAN

class Pacman(Objeto):
    
    def __init__(self) -> None:
        super().__init__()
        self.tipo = PACMAN