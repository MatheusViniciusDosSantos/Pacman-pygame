import os
import pygame
from fisica import Fisica
from pygame import Surface
from PIL import Image, ImageSequence

class Objeto(Fisica, pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.id: int
        self.tipo: int
        self.posicao_x: float
        self.posicao_y: float
        self.tamanho: float = 50.0
        self.velocidade_x: float = 0.0
        self.velocidade_y: float = 0.0
        self.foto: Surface
        super().__init__()
    
    def carregar_imagem(self, nome, tamanho): 
        """carrega uma imagem na memoria"""
        caminho = os.path.join("imagens", nome)
        try: 
            imagem = pygame.image.load(caminho).convert_alpha()
            self.tamanho = tamanho
            self.foto = pygame.transform.scale(imagem, (tamanho,tamanho))
        except pygame.error as e: 
            print(e)
            print("Impossível carregar a imagem:" + caminho)
            raise SystemExit
        return imagem, imagem.get_rect()

    def loadGIF(self, caminho):
        pilImage = Image.open(caminho)
        frames = []
        if pilImage.format == 'GIF' and pilImage.is_animated:
            for frame in ImageSequence.Iterator(pilImage):
                pygameImage = self.transformaPilImageParaSurface(frame.convert('RGBA'))
                frames.append(pygameImage)
        else:
            frames.append(self.transformaPilImageParaSurface(pilImage))
        return frames

    def transformaPilImageParaSurface(self, pilImage):
        mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()

    def definirPosicoes(self, tempo):
        self.posicao_x += (self.velocidade_x * tempo)
        self.posicao_y += (self.velocidade_y * tempo)
    
    def imprimirObj(self, display_game):
        display_game.blit(self.foto, (self.posicao_x-25, self.posicao_y-25))