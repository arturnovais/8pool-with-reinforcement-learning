from utils.PhysicsEnvironment import PhysicsEnvironment

class Ball:
    '''
    Classe que representa uma bola de sinuca com características como número, raio, massa, posição,
    velocidade e rotação. A bola pode ser movimentada aplicando forças e é afetada por efeitos físicos como atrito.
    
    Args:
        numero (int): O número da bola (ex: 1-15 para bolas coloridas).
        raio (float): O raio da bola (em metros).
        massa (float): A massa da bola (em kg).
        posicao (tuple): Posição inicial da bola na mesa, no formato (x, y).
        velocidade (tuple): Velocidade inicial da bola, com componentes (vx, vy). Padrão é (0, 0).
        rotação (float): Rotação inicial da bola (em radianos).
    '''
    
    def __init__(self, numero: int, raio: float, massa: float, posicao: tuple, velocidade: tuple = (0, 0), rotação: float = 0):
        self.numero = numero
        self.raio = raio
        self.massa = massa
        self.posicao = posicao
        self.velocidade = velocidade
        self.aceleracao = (0, 0)
        self.rotação = rotação
        self.spin = 0

    def aplicar_forca(self, forca: tuple, dt: float):
        '''
        Aplica uma força à bola, ajustando sua aceleração e velocidade de acordo com a segunda lei de Newton.
        
        Args:
            forca (tuple): Força aplicada à bola nas direções (fx, fy), em Newtons.
            dt (float): Intervalo de tempo em segundos durante o qual a força é aplicada.
        '''
        ax = forca[0] / self.massa
        ay = forca[1] / self.massa
        self.aceleracao = (ax, ay)
        
        self.velocidade = (
            self.velocidade[0] + self.aceleracao[0] * dt,
            self.velocidade[1] + self.aceleracao[1] * dt
        )
    
    def atualizar_posicao(self, dt: float, ambiente_fisico: PhysicsEnvironment):
        '''
        Atualiza a posição da bola levando em consideração a velocidade atual, o atrito e a resistência do ar.
        
        Args:
            dt (float): Intervalo de tempo para atualização, em segundos.
            ambiente_fisico (PhysicsEnvironment): Ambiente físico que define atrito e resistência.
        '''
        self.velocidade = ambiente_fisico.aplicar_atrito(self.velocidade)
        self.velocidade = ambiente_fisico.aplicar_resistencia_ar(self.velocidade)

        if self.velocidade[0] ** 2 + self.velocidade[1] ** 2 < 0.01:
            self.velocidade = (0, 0)

        self.posicao = (
            self.posicao[0] + self.velocidade[0] * dt,
            self.posicao[1] + self.velocidade[1] * dt
        )

        self.aplicar_spin(dt)

    def aplicar_spin(self, dt: float):
        '''
        Aplica o efeito de rotação (spin) no movimento da bola, alterando levemente sua trajetória.
        
        Args:
            dt (float): Intervalo de tempo para aplicar o spin, em segundos.
        '''
        spin_efeito = self.spin * 0.05
        self.velocidade = (
            self.velocidade[0] + spin_efeito * dt,
            self.velocidade[1] - spin_efeito * dt
        )


def criar_bolas(table):
    '''
    Inicializa as bolas de sinuca e as posiciona em formato triangular no canto superior direito da mesa.
    Cada bola recebe uma cor e é adicionada à mesa de jogo.
    
    Args:
        table (Table): A mesa de sinuca onde as bolas serão posicionadas.
    '''
    cores = [
        (255, 255, 0),    # Amarelo
        (255, 0, 0),      # Vermelho
        (0, 255, 0),      # Verde
        (0, 0, 255),      # Azul
        (255, 20, 147),   # Rosa
        (0, 0, 0),        # Preto
        (255, 165, 0),    # Laranja
        (139, 69, 19),    # Marrom
        (255, 255, 255),  # Bola Branca
        (255, 192, 203),  # Listrada rosa
        (0, 128, 128),    # Listrada ciano
        (128, 0, 128),    # Listrada roxa
    ]

    raio_bola = 10
    massa_bola = 1
    espaco_entre_bolas = 2

    # Coordenadas ajustadas para centralizar no eixo y e deslocar um pouco mais à direita no eixo x
    x_inicial = table.x_start + table.largura * 0.7
    y_inicial = table.y_start + table.altura / 2 - (3 * raio_bola)

    contador_bola = 0
    for linha in range(5):
        for i in range(linha + 1):
            x_pos = x_inicial + (linha * (raio_bola * 2 + espaco_entre_bolas))
            y_pos = y_inicial + (i * (raio_bola * 2 + espaco_entre_bolas)) + (linha * raio_bola)
            bola = Ball(numero=contador_bola + 1, raio=raio_bola, massa=massa_bola, posicao=(x_pos, y_pos))
            bola.velocidade = (0, 0)
            bola.cor = cores[contador_bola % len(cores)]
            table.bolas.append(bola)
            contador_bola += 1


def iniciar_bola_branca(table):
    '''
    Inicializa a bola branca em uma posição específica na mesa e define sua velocidade inicial.
    
    Args:
        table (Table): A mesa onde a bola branca será posicionada.
    '''
    bola_branca = Ball(numero=0, raio=10, massa=1.05, posicao=(150, 500))
    bola_branca.velocidade = (100, 100)
    bola_branca.cor = (255, 255, 255)
    table.bolas.append(bola_branca)
    table.bola_branca = bola_branca
