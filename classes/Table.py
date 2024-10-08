
from classes.PhysicsEnvironment import PhysicsEnvironment
from classes.Ball import Ball
from classes.Pocket import Pocket
import pygame

class Table:
    def __init__(self, largura: float, altura: float, ambiente_fisico: PhysicsEnvironment, height, width):
        """
        Inicializa a mesa de sinuca com suas dimensões e o ambiente físico.

        Args:
            largura (float): A largura da mesa de sinuca (em metros).
            altura (float): A altura da mesa de sinuca (em metros).
            ambiente_fisico (PhysicsEnvironment): O ambiente físico que afeta as bolas na mesa.
        """
        
        self.largura = largura
        self.altura = altura
        self.ambiente_fisico = ambiente_fisico  # Ambiente físico da mesa (atrito, resistência do ar, etc.)
        self.buracos = self.definir_buracos()  # Definir os buracos como instâncias da classe Pocket
        self.height = height
        self.width = width

        self.top_left = (100,100) # x,y
        self.buttom_right = (self.width - 200, self.height - 200) # x,y
        
        
        
    def definir_buracos(self) -> list:
        """
        Define as posições e tamanhos dos buracos da mesa de sinuca (geralmente 6 buracos).

        Returns:
            list: Uma lista com as instâncias de Pocket representando os buracos.
        """
        raio_buraco = 0.07  # Raio padrão de um buraco de sinuca
        return [
            Pocket(posicao=(0, 0), raio=raio_buraco),  # Canto superior esquerdo
            Pocket(posicao=(self.largura / 2, 0), raio=raio_buraco),  # Meio superior
            Pocket(posicao=(self.largura, 0), raio=raio_buraco),  # Canto superior direito
            Pocket(posicao=(0, self.altura), raio=raio_buraco),  # Canto inferior esquerdo
            Pocket(posicao=(self.largura / 2, self.altura), raio=raio_buraco),  # Meio inferior
            Pocket(posicao=(self.largura, self.altura), raio=raio_buraco)  # Canto inferior direito
        ]

    def detectar_buraco(self, bola: Ball) -> bool:
        """
        Verifica se a bola caiu em um dos buracos.

        Args:
            bola (Ball): A bola que está sendo verificada.

        Returns:
            bool: True se a bola caiu em um buraco, False caso contrário.
        """
        for buraco in self.buracos:
            if buraco.verificar_bola_no_buraco(bola):
                return True
        return False


    def draw(self,screen: pygame.Surface):
        cor_mesa = (0, 128, 0)  # Verde
        
        
        # desenha um retângulo verde para representar a mesa
        pygame.draw.rect(screen, cor_mesa, (self.top_left[0], 
                                            self.top_left[1], 
                                            self.buttom_right[0], self.buttom_right[1]))
        
        # desenha as caçapas em cinza
        for buraco in self.buracos:
            pygame.draw.circle(screen, (128, 128, 128), (int(buraco.posicao[0] * self.width), 
                                                         int(buraco.posicao[1] * self.height)), 10)
            
        
        
        