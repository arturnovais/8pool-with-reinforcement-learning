import math
from utils.Ball import Ball
import torch
import utils.config as cfg

class CollisionDetector:
    '''
    Classe responsável por detectar e resolver colisões entre bolas e entre bolas e as bordas da mesa.
    
    Args:
        elasticidade (float): Fator de elasticidade que define quanto da energia é conservada após uma colisão. Padrão é 0.95.
    '''
    
    def __init__(self):
        '''
        Inicializa o detector de colisões com um fator de elasticidade.
        '''
        self.elasticidade = torch.tensor(cfg.elasticidade, device=cfg.device)

    def detectar_colisao_bolas(self, bola1: Ball, bola2: Ball) -> bool:
        '''
        Verifica se duas bolas colidiram.
        A colisão é detectada se a distância entre os centros das bolas for menor ou igual à soma de seus raios.
        
        Args:
            bola1 (Ball): Primeira bola a ser verificada.
            bola2 (Ball): Segunda bola a ser verificada.
        
        Returns:
            bool: True se as bolas colidirem, False caso contrário.
        '''
        dist_entre_bolas = bola1.posicao - bola2.posicao
        distancia = torch.sqrt(dist_entre_bolas.pow(2).sum())
        return distancia <= (bola1.raio + bola2.raio)
    
    
        """
    def resolver_colisao_bolas(self, bola1: Ball, bola2: Ball):
        '''
        Resolve a colisão entre duas bolas, ajustando suas velocidades de acordo com a conservação do momento linear e energia.
        A velocidade normal é trocada entre as bolas, enquanto a velocidade tangencial permanece a mesma. 
        Um fator de elasticidade é aplicado para reduzir a energia em colisões imperfeitas.
        
        Args:
            bola1 (Ball): Primeira bola envolvida na colisão.
            bola2 (Ball): Segunda bola envolvida na colisão.
        '''
        dist_x = bola1.posicao[0] - bola2.posicao[0]
        dist_y = bola1.posicao[1] - bola2.posicao[1]
        distancia = math.sqrt(dist_x**2 + dist_y**2)

        
        if distancia == 0:
            distancia = 0.01

        normal_x = dist_x / distancia
        normal_y = dist_y / distancia

        tangente_x = -normal_y
        tangente_y = normal_x

        v1_normal = bola1.velocidade[0] * normal_x + bola1.velocidade[1] * normal_y
        v2_normal = bola2.velocidade[0] * normal_x + bola2.velocidade[1] * normal_y

        v1_tangente = bola1.velocidade[0] * tangente_x + bola1.velocidade[1] * tangente_y
        v2_tangente = bola2.velocidade[0] * tangente_x + bola2.velocidade[1] * tangente_y

        v1_normal_final = (v1_normal * (bola1.massa - bola2.massa) + 2 * bola2.massa * v2_normal) / (bola1.massa + bola2.massa)
        v2_normal_final = (v2_normal * (bola2.massa - bola1.massa) + 2 * bola1.massa * v1_normal) / (bola1.massa + bola2.massa)

        bola1.velocidade = (
            v1_normal_final * normal_x + v1_tangente * tangente_x,
            v1_normal_final * normal_y + v1_tangente * tangente_y
        )

        bola2.velocidade = (
            v2_normal_final * normal_x + v2_tangente * tangente_x,
            v2_normal_final * normal_y + v2_tangente * tangente_y
        )

        bola1.velocidade = (
            bola1.velocidade[0] * self.elasticidade,
            bola1.velocidade[1] * self.elasticidade
        )

        bola2.velocidade = (
            bola2.velocidade[0] * self.elasticidade,
            bola2.velocidade[1] * self.elasticidade
        )

        overlap = bola1.raio + bola2.raio - distancia
        if overlap > 0:
            bola1.posicao = (
                bola1.posicao[0] + (overlap / 2) * normal_x,
                bola1.posicao[1] + (overlap / 2) * normal_y
            )
            bola2.posicao = (
                bola2.posicao[0] - (overlap / 2) * normal_x,
                bola2.posicao[1] - (overlap / 2) * normal_y
            )
        """
def resolver_colisao_bolas(self, bola1, bola2):
    """
    Resolve a colisão entre duas bolas, ajustando suas velocidades de acordo com a conservação do momento linear e energia.
    A velocidade normal é trocada entre as bolas, enquanto a velocidade tangencial permanece a mesma.
    Um fator de elasticidade é aplicado para reduzir a energia em colisões imperfeitas.

    Args:
        bola1: Objeto representando a primeira bola, com atributos posicao, velocidade, massa e raio.
        bola2: Objeto representando a segunda bola, com atributos posicao, velocidade, massa e raio.
    """
    # Calcula a diferença de posição e a distância entre os centros
    dist_entre_bolas = bola1.posicao - bola2.posicao
    distancia = torch.sqrt(dist_entre_bolas.pow(2).sum())
    
    # Evita divisão por zero
    if distancia == 0:
        distancia = 0.01

    # Vetor normal e tangente
    normal = dist_entre_bolas / distancia
    tangente = torch.tensor([-normal[1], normal[0]], device=bola1.posicao.device)
    
    # Componentes normal e tangente das velocidades
    v1_normal = bola1.velocidade @ normal
    v2_normal = bola2.velocidade @ normal

    v1_tangente = bola1.velocidade @ tangente
    v2_tangente = bola2.velocidade @ tangente
    
    # Velocidades normais após a colisão
    v1_normal_final = (v1_normal * (bola1.massa - bola2.massa) + 2 * bola2.massa * v2_normal) / (bola1.massa + bola2.massa)
    v2_normal_final = (v2_normal * (bola2.massa - bola1.massa) + 2 * bola1.massa * v1_normal) / (bola1.massa + bola2.massa)
    
    # Reconstrói as velocidades após a colisão
    bola1.velocidade = v1_normal_final * normal + v1_tangente * tangente
    bola2.velocidade = v2_normal_final * normal + v2_tangente * tangente
    
    
    # Aplica o fator de elasticidade
    bola1.velocidade *= self.elasticidade
    bola2.velocidade *= self.elasticidade
    
    # Correção para evitar sobreposição
    overlap = bola1.raio + bola2.raio - distancia
    if overlap > 0:
        bola1.posicao = bola1.posicao + (overlap / 2) * normal
        bola2.posicao = bola2.posicao - (overlap / 2) * normal


    def detectar_colisao_borda(self, bola: Ball, x_start: float, y_start: float, largura: float, altura: float):
        '''
        Verifica e resolve a colisão entre uma bola e as bordas da mesa.
        Caso a bola colida com as bordas, sua velocidade é invertida e o fator de elasticidade é aplicado, 
        reduzindo a energia da bola.
        
        Args:
            bola (Ball): A bola para verificar a colisão.
            x_start (float): Posição inicial no eixo x da mesa.
            y_start (float): Posição inicial no eixo y da mesa.
            largura (float): Largura da mesa.
            altura (float): Altura da mesa.
        '''
        
        if bola.posicao[0] - bola.raio < x_start:
            bola.posicao = torch.tensor(x_start + bola.raio, bola.posicao[1]) , cfg.device 
            bola.velocidade = torch.tensor(-bola.velocidade[0] * self.elasticidade, bola.velocidade[1], cfg.device)
                        
        elif bola.posicao[0] + bola.raio > x_start + largura:
            bola.posicao = torch.tensor(x_start + largura - bola.raio, bola.posicao[1]), cfg.device 
            bola.velocidade = torch.tensor(-bola.velocidade[0] * self.elasticidade, bola.velocidade[1], cfg.device)

        if bola.posicao[1] - bola.raio < y_start:
            bola.posicao = torch.tensor(bola.posicao[0], y_start + bola.raio, cfg.device)
            bola.velocidade = torch.tensor(bola.velocidade[0], -bola.velocidade[1] * self.elasticidade, cfg.device)

        elif bola.posicao[1] + bola.raio > y_start + altura:
            bola.posicao = torch.tensor(bola.posicao[0], y_start + altura - bola.raio, cfg.device)
            bola.velocidade = torch.tensor(bola.velocidade[0], -bola.velocidade[1] * self.elasticidade, cfg.device)
