import pygame
from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.Ball import Ball
from utils.Pocket import Pocket
from utils.CollisionDetector import CollisionDetector

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
        raio_buraco = 13  # Buracos um pouco menores
        return [
            Pocket(posicao=(self.x_start + 5, self.y_start + 5), raio=raio_buraco),  # Canto superior esquerdo
            Pocket(posicao=(self.x_start + self.largura / 2, self.y_start + 5), raio=raio_buraco),  # Meio superior
            Pocket(posicao=(self.x_start + self.largura - 5, self.y_start + 5), raio=raio_buraco),  # Canto superior direito
            Pocket(posicao=(self.x_start + 5, self.y_start + self.altura - 5), raio=raio_buraco),  # Canto inferior esquerdo
            Pocket(posicao=(self.x_start + self.largura / 2, self.y_start + self.altura - 5), raio=raio_buraco),  # Meio inferior
            Pocket(posicao=(self.x_start + self.largura - 5, self.y_start + self.altura - 5), raio=raio_buraco)  # Canto inferior direito
        ]
        
    

    def desenhar_bordas(self, screen):
        '''
        Desenha as bordas arredondadas da mesa, simulando bordas de madeira.
        
        Args:
            screen (pygame.Surface): Superfície onde as bordas serão desenhadas.
        '''
        cor_borda = (139, 69, 19)  # Cor marrom para simular madeira
        espessura_borda = 30

        # Desenha bordas retangulares com cantos arredondados
        pygame.draw.rect(screen, cor_borda, (self.x_start - espessura_borda, self.y_start - espessura_borda,
                                             self.largura + 2 * espessura_borda, self.altura + 2 * espessura_borda), border_radius=15)

        # Adiciona efeito de profundidade nas bordas
        sombra_borda = (105, 53, 10)
        pygame.draw.rect(screen, sombra_borda, (self.x_start - espessura_borda + 10, self.y_start - espessura_borda + 10,
                                                self.largura + 2 * espessura_borda, self.altura + 2 * espessura_borda), border_radius=15)

    def desenhar_mesa_verde(self, screen):
        '''
        Desenha a área verde (tapete) da mesa.
        
        Args:
            screen (pygame.Surface): Superfície onde a área verde será desenhada.
        '''
        cor_verde_mesa = (34, 139, 34)  # Cor verde simulando o tecido de sinuca
        pygame.draw.rect(screen, cor_verde_mesa, (self.x_start, self.y_start, self.largura, self.altura))

    def desenhar_buracos(self, screen):
        '''
        Desenha os buracos pretos com contornos metálicos na mesa.
        
        Args:
            screen (pygame.Surface): Superfície onde os buracos serão desenhados.
        '''
        for buraco in self.buracos:
            # Contorno metálico
            pygame.draw.circle(screen, (169, 169, 169), (int(buraco.posicao[0]), int(buraco.posicao[1])), buraco.raio + 3)
            # Buraco preto
            pygame.draw.circle(screen, (0, 0, 0), (int(buraco.posicao[0]), int(buraco.posicao[1])), buraco.raio)

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
        Desenha a mesa de sinuca, buracos, bolas e as bordas, além de atualizar as posições das bolas e tratar as colisões.
        
        Args:
            screen (pygame.Surface): Superfície onde a mesa será desenhada.
        '''
        # Desenha as bordas de madeira da mesa
        self.desenhar_bordas(screen)

        # Desenha a parte verde da mesa
        self.desenhar_mesa_verde(screen)

        # Desenha os buracos da mesa
        self.desenhar_buracos(screen)

        # Gerencia o estado das bolas e as colisões
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

        # Remover bolas que caíram nos buracos
        for bola in bolas_para_remover:
            self.bolas.remove(bola)

        # Desenha as bolas na tela
        for bola in self.bolas:
            if bola.imagem:
                # Desenha a bola com a imagem ajustada, centralizando com base no novo tamanho visual
                visual_raio = bola.raio * 2  # Usando o dobro do raio para o tamanho visual
                screen.blit(bola.imagem, (bola.posicao[0] - visual_raio, bola.posicao[1] - visual_raio))
            else:
                # Se não houver imagem, desenha a bola como um círculo de cor
                pygame.draw.circle(screen, bola.cor, (int(bola.posicao[0]), int(bola.posicao[1])), int(bola.raio))
