from objeto import Objeto
from constantes import PACMAN

class Pacman(Objeto):
    
    def __init__(self) -> None:
        self.tipo = PACMAN
        super().__init__()