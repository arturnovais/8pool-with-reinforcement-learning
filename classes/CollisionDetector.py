import math
from Ball import Ball
from Table import Table

class CollisionDetector:
    def __init__(self, elasticidade: float = 0.95):
        """
        Inicializa o detector de colisões com um fator de elasticidade.

        Args:
            elasticidade (float): Fator que determina o quão elástica é a colisão (0 < elasticidade <= 1).
        """
        self.elasticidade = elasticidade  # Define o quão elástica é a colisão (1 = perfeitamente elástica)

    def detectar_colisao_bolas(self, bola1: Ball, bola2: Ball) -> bool:
        """
        Verifica se duas bolas colidiram.

        Args:
            bola1 (Ball): A primeira bola.
            bola2 (Ball): A segunda bola.

        Returns:
            bool: True se houve colisão, False caso contrário.
        """
        dist_x = bola1.posicao[0] - bola2.posicao[0]
        dist_y = bola1.posicao[1] - bola2.posicao[1]
        distancia = math.sqrt(dist_x**2 + dist_y**2)

        # Colisão ocorre se a distância entre os centros das bolas for menor que a soma dos raios
        return distancia <= (bola1.raio + bola2.raio)

    def resolver_colisao_bolas(self, bola1: Ball, bola2: Ball):
        """
        Resolve a colisão entre duas bolas, ajustando suas velocidades de acordo com a conservação do momento.

        Args:
            bola1 (Ball): A primeira bola.
            bola2 (Ball): A segunda bola.
        """
        # Vetor normal entre os centros das bolas
        dist_x = bola1.posicao[0] - bola2.posicao[0]
        dist_y = bola1.posicao[1] - bola2.posicao[1]
        distancia = math.sqrt(dist_x**2 + dist_y**2)

        if distancia == 0:
            distancia = 0.01  # Evitar divisão por zero

        # Normaliza o vetor de direção
        normal_x = dist_x / distancia
        normal_y = dist_y / distancia

        # Vetor tangente
        tangente_x = -normal_y
        tangente_y = normal_x

        # Decomposição das velocidades ao longo dos eixos normal e tangente
        v1_normal = bola1.velocidade[0] * normal_x + bola1.velocidade[1] * normal_y
        v1_tangente = bola1.velocidade[0] * tangente_x + bola1.velocidade[1] * tangente_y
        v2_normal = bola2.velocidade[0] * normal_x + bola2.velocidade[1] * normal_y
        v2_tangente = bola2.velocidade[0] * tangente_x + bola2.velocidade[1] * tangente_y

        # Troca de velocidades normais (conservação do momento em colisões perfeitamente elásticas)
        v1_normal_final = (v1_normal * (bola1.massa - bola2.massa) + 2 * bola2.massa * v2_normal) / (bola1.massa + bola2.massa)
        v2_normal_final = (v2_normal * (bola2.massa - bola1.massa) + 2 * bola1.massa * v1_normal) / (bola1.massa + bola2.massa)

        # Atualiza as velocidades finais das bolas (velocidade tangencial permanece a mesma)
        bola1.velocidade = (
            v1_normal_final * normal_x + v1_tangente * tangente_x,
            v1_normal_final * normal_y + v1_tangente * tangente_y
        )

        bola2.velocidade = (
            v2_normal_final * normal_x + v2_tangente * tangente_x,
            v2_normal_final * normal_y + v2_tangente * tangente_y
        )

        # Aplicar o fator de elasticidade
        bola1.velocidade = (bola1.velocidade[0] * self.elasticidade, bola1.velocidade[1] * self.elasticidade)
        bola2.velocidade = (bola2.velocidade[0] * self.elasticidade, bola2.velocidade[1] * self.elasticidade)

    def detectar_colisao_borda(self, bola: Ball, mesa: Table):
        """
        Verifica e resolve a colisão entre uma bola e as bordas da mesa.

        Args:
            bola (Ball): A bola para verificar a colisão.
            mesa (Table): A mesa em que a bola está se movendo.
        """
        if bola.posicao[0] - bola.raio < 0 or bola.posicao[0] + bola.raio > mesa.largura:
            # Colisão com as bordas verticais (esquerda ou direita)
            bola.velocidade = (-bola.velocidade[0] * self.elasticidade, bola.velocidade[1])
        
        if bola.posicao[1] - bola.raio < 0 or bola.posicao[1] + bola.raio > mesa.altura:
            # Colisão com as bordas horizontais (superior ou inferior)
            bola.velocidade = (bola.velocidade[0], -bola.velocidade[1] * self.elasticidade)
