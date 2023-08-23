from objeto import Objeto
from constantes import PACMAN
from sprites import PacmanSprites

class Pacman(Objeto):
    
    def __init__(self) -> None:
        super().__init__()
        self.tipo = PACMAN
        self.sprites = PacmanSprites(self)

    def update(self, dt):	
        self.sprites.update(dt)