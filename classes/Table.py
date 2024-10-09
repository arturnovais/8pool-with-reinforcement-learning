
from classes.PhysicsEnvironment import PhysicsEnvironment
from classes.Ball import Ball
from classes.Pocket import Pocket
import pygame

class Table:
    def __init__(self, largura: float, altura: float, ambiente_fisico: PhysicsEnvironment):
        """
        Inicializa a mesa de sinuca com suas dimensões e o ambiente físico.

        Args:
            largura (float): A largura da mesa de sinuca (em metros).
            altura (float): A altura da mesa de sinuca (em metros).
            ambiente_fisico (PhysicsEnvironment): O ambiente físico que afeta as bolas na mesa.
        """
        
        self.x_start = 100
        self.y_start = 100     
        self.largura = largura
        self.altura = altura
        
        
        self.ambiente_fisico = ambiente_fisico  # Ambiente físico da mesa (atrito, resistência do ar, etc.)
        self.buracos = self.definir_buracos()  # Definir os buracos como instâncias da classe Pocket
        self.bolas = []
        
        
    def definir_buracos(self) -> list:
        """
        Define as posições e tamanhos dos buracos da mesa de sinuca (geralmente 6 buracos).

        Returns:
            list: Uma lista com as instâncias de Pocket representando os buracos.
        """
        raio_buraco = 15  # Raio padrão de um buraco de sinuca
        return [
            Pocket(posicao=(self.x_start                      , self.y_start), raio=raio_buraco),  # Canto superior esquerdo
            Pocket(posicao=(self.x_start+ (self.largura / 2)    , self.y_start+ 0), raio=raio_buraco),  # Meio superior
            Pocket(posicao=(self.x_start+ self.largura        , self.y_start+ 0), raio=raio_buraco),  # Canto superior direito
            Pocket(posicao=(self.x_start,                       self.y_start+ self.altura), raio=raio_buraco),  # Canto inferior esquerdo
            Pocket(posicao=(self.x_start+ self.largura / 2    , self.y_start+ self.altura), raio=raio_buraco),  # Meio inferior
            Pocket(posicao=(self.x_start+ self.largura        , self.y_start+ self.altura), raio=raio_buraco)  # Canto inferior direito
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
        pygame.draw.rect(screen, cor_mesa, (self.x_start, 
                                            self.x_start, 
                                            self.largura, self.altura))
        
        # desenha as caçapas em cinza
        for buraco in self.buracos:
            pygame.draw.circle(screen, (128, 128, 128),  (int(buraco.posicao[0]), int(buraco.posicao[1])),  int(buraco.raio))
            
    
        # computa a velocidade da bola
        for bola in self.bolas:
            bola.atualizar_posicao(1, self.ambiente_fisico)
            
        atrito_parede = 0.999

        # verifica se alguma bola bateu na parede
        for bola in self.bolas:
            if (bola.posicao[0] - bola.raio < self.x_start) or (bola.posicao[0] + bola.raio > self.x_start + self.largura):
                bola.velocidade = (-bola.velocidade[0]*atrito_parede, bola.velocidade[1]*atrito_parede)
                
                
            if bola.posicao[1] - bola.raio < self.y_start or bola.posicao[1] + bola.raio > self.y_start + self.altura:
                bola.velocidade = (bola.velocidade[0]*atrito_parede, -bola.velocidade[1]*atrito_parede)
                
        
        
        for bola in self.bolas:
            pygame.draw.circle(screen, bola.cor, (int(bola.posicao[0]), int(bola.posicao[1])), int(bola.raio))
            
        