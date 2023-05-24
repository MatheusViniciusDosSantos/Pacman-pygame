from objeto import Objeto
from constantes import PAREDE

class Parede(Objeto):
    
    def __init__(self) -> None:
        self.tipo = PAREDE
        super().__init__()