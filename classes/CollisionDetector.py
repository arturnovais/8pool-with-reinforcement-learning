import math
from classes.Ball import Ball

class CollisionDetector:
    def __init__(self, elasticidade: float = 0.95):
        """
        Inicializa o detector de colisões com um fator de elasticidade.
        """
        self.elasticidade = elasticidade

    def detectar_colisao_bolas(self, bola1: Ball, bola2: Ball) -> bool:
        """
        Verifica se duas bolas colidiram.
        A colisão é detectada se a distância entre os centros das bolas
        for menor ou igual à soma de seus raios.
        """
        dist_x = bola1.posicao[0] - bola2.posicao[0]
        dist_y = bola1.posicao[1] - bola2.posicao[1]
        distancia = math.sqrt(dist_x**2 + dist_y**2)
        return distancia <= (bola1.raio + bola2.raio)

    def resolver_colisao_bolas(self, bola1: Ball, bola2: Ball):
        """
        Resolve a colisão entre duas bolas, ajustando suas velocidades
        de acordo com a conservação do momento linear e energia.
        A velocidade normal é trocada entre as bolas, enquanto a
        velocidade tangencial permanece a mesma. Um fator de elasticidade
        é aplicado para reduzir a energia em colisões imperfeitas.
        """
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

    def detectar_colisao_borda(self, bola: Ball, x_start: float, y_start: float, largura: float, altura: float):
        """
        Verifica e resolve a colisão entre uma bola e as bordas da mesa.
        Caso a bola colida com as bordas, sua velocidade é invertida e
        o fator de elasticidade é aplicado, reduzindo a energia da bola.

        Args:
            bola (Ball): A bola para verificar a colisão.
            x_start (float): Posição inicial no eixo x da mesa.
            y_start (float): Posição inicial no eixo y da mesa.
            largura (float): Largura da mesa.
            altura (float): Altura da mesa.
        """
        
        if bola.posicao[0] - bola.raio < x_start:
            bola.posicao = (x_start + bola.raio, bola.posicao[1])  
            bola.velocidade = (-bola.velocidade[0] * self.elasticidade, bola.velocidade[1])
            
        elif bola.posicao[0] + bola.raio > x_start + largura:
            bola.posicao = (x_start + largura - bola.raio, bola.posicao[1]) 
            bola.velocidade = (-bola.velocidade[0] * self.elasticidade, bola.velocidade[1])

        if bola.posicao[1] - bola.raio < y_start:
            bola.posicao = (bola.posicao[0], y_start + bola.raio)
            bola.velocidade = (bola.velocidade[0], -bola.velocidade[1] * self.elasticidade)

        elif bola.posicao[1] + bola.raio > y_start + altura:
            bola.posicao = (bola.posicao[0], y_start + altura - bola.raio)
            bola.velocidade = (bola.velocidade[0], -bola.velocidade[1] * self.elasticidade)
