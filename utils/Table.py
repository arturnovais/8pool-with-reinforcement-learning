from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.Ball import Ball
from utils.Pocket import Pocket
from utils.CollisionDetector import CollisionDetector
import pygame

class Table:
    '''
    Classe que representa a mesa de sinuca, incluindo buracos, bolas e o ambiente físico.
    
    Args:
        largura (float): A largura da mesa de sinuca.
        altura (float): A altura da mesa de sinuca.
        ambiente_fisico (PhysicsEnvironment): Instância que controla o ambiente físico (através de atrito, resistência do ar, etc.).
        display_width (int): Largura da tela de exibição (em pixels).
        display_height (int): Altura da tela de exibição (em pixels).
    '''
    
    def __init__(self, largura: float, altura: float, ambiente_fisico: PhysicsEnvironment, display_width, display_height):
        '''
        Inicializa a mesa de sinuca com suas dimensões, o ambiente físico, e define os buracos e as bolas.
        '''
        self.x_start = display_width / 2 - largura / 2
        self.y_start = display_height / 2 - altura / 2
        self.largura = largura
        self.altura = altura
        
        self.detecttor_colisao = CollisionDetector()
        self.ambiente_fisico = ambiente_fisico
        self.buracos = self.definir_buracos()
        self.bolas = []
        self.bola_branca = None

    def definir_buracos(self) -> list:
        '''
        Define as posições e tamanhos dos seis buracos da mesa de sinuca.
        
        Returns:
            list: Lista de instâncias de Pocket representando os buracos da mesa.
        '''
        raio_buraco = 15
        return [
            Pocket(posicao=(self.x_start                     , self.y_start), raio=raio_buraco),
            Pocket(posicao=(self.x_start + (self.largura / 2), self.y_start), raio=raio_buraco),
            Pocket(posicao=(self.x_start + self.largura      , self.y_start), raio=raio_buraco),
            Pocket(posicao=(self.x_start                     , self.y_start + self.altura), raio=raio_buraco),
            Pocket(posicao=(self.x_start + (self.largura / 2), self.y_start + self.altura), raio=raio_buraco),
            Pocket(posicao=(self.x_start + self.largura      , self.y_start + self.altura), raio=raio_buraco)
        ]

    def atualizar_estado_bola(self, bola: Ball, dt: float):
        '''
        Atualiza a posição da bola considerando as forças de atrito e resistência do ar.
        
        Args:
            bola (Ball): A bola cujo estado será atualizado.
            dt (float): Intervalo de tempo (em segundos) para atualização.
        '''
        bola.velocidade = self.ambiente_fisico.aplicar_atrito(bola.velocidade)
        bola.velocidade = self.ambiente_fisico.aplicar_resistencia_ar(bola.velocidade)

        bola.posicao = (
            bola.posicao[0] + bola.velocidade[0] * dt,
            bola.posicao[1] + bola.velocidade[1] * dt
        )

    def detectar_buraco(self, bola: Ball) -> bool:
        '''
        Verifica se a bola caiu em um dos buracos da mesa.
        
        Args:
            bola (Ball): A bola a ser verificada.
        
        Returns:
            bool: True se a bola caiu em um buraco, False caso contrário.
        '''
        return any(buraco.verificar_bola_no_buraco(bola) for buraco in self.buracos)

    def draw(self, screen: pygame.Surface):
        '''
        Desenha a mesa de sinuca, buracos e bolas, além de atualizar as posições das bolas e tratar as colisões.
        
        Args:
            screen (pygame.Surface): Superfície onde a mesa será desenhada.
        '''
        cor_mesa = (0, 128, 0)
        pygame.draw.rect(screen, cor_mesa, (self.x_start, self.y_start, self.largura, self.altura))

        for buraco in self.buracos:
            pygame.draw.circle(screen, (128, 128, 128), (int(buraco.posicao[0]), int(buraco.posicao[1])), int(buraco.raio))

        bolas_para_remover = []

        for bola in self.bolas:
            bola.atualizar_posicao(1, self.ambiente_fisico)
            self.detecttor_colisao.detectar_colisao_borda(bola, self.x_start, self.y_start, self.largura, self.altura)

            if self.detectar_buraco(bola):
                bolas_para_remover.append(bola)

        for i in range(len(self.bolas)):
            for j in range(i + 1, len(self.bolas)):
                if self.detecttor_colisao.detectar_colisao_bolas(self.bolas[i], self.bolas[j]):
                    self.detecttor_colisao.resolver_colisao_bolas(self.bolas[i], self.bolas[j])

        for bola in bolas_para_remover:
            self.bolas.remove(bola)

        for bola in self.bolas:
            pygame.draw.circle(screen, bola.cor, (int(bola.posicao[0]), int(bola.posicao[1])), int(bola.raio))
