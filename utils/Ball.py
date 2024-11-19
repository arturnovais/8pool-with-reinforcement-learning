import pygame
from utils.PhysicsEnvironment import PhysicsEnvironment
import utils.config as  cfg

class Ball:
    '''
    Classe que representa uma bola de sinuca com características como número, raio, massa, posição,
    velocidade, rotação e imagem associada.
    
    Args:
        numero (int): O número da bola (ex: 1-15 para bolas coloridas).
        raio (float): O raio da bola (em metros).
        massa (float): A massa da bola (em kg).
        posicao (tuple): Posição inicial da bola na mesa, no formato (x, y).
        imagem (pygame.Surface): A imagem da bola.
        velocidade (tuple): Velocidade inicial da bola, com componentes (vx, vy). Padrão é (0, 0).
        rotação (float): Rotação inicial da bola (em radianos).
    '''
    
    def __init__(self, numero: int, raio: float, massa: float, posicao: tuple, imagem=None, velocidade: tuple = (0, 0), rotação: float = 0):
        self.numero = numero
        self.raio = raio
        self.massa = massa
        self.posicao = posicao
        self.velocidade = velocidade
        self.aceleracao = (0, 0)
        self.rotação = rotação
        self.spin = 0

        self.visual_raio = raio * 2  # Raio visual para o dobro do tamanho
        if imagem is not None:
            # Redimensiona a imagem para o dobro do tamanho da bola (baseado no raio visual)
            self.imagem = pygame.transform.scale(imagem, (int(self.visual_raio * 2), int(self.visual_raio * 2)))
        else:
            self.imagem = None

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

def carregar_imagem_bola(numero):
        '''
        Carrega a imagem correspondente à bola com o número fornecido.
        
        Args:
            numero (int): Número da bola para carregar a imagem.
        
        Returns:
            pygame.Surface: A imagem da bola carregada.
        '''
        caminho_imagem = f"imgs/ball{numero}.png"  # Assumindo que as imagens estão em "imagens/ballX.png"
        return pygame.image.load(caminho_imagem).convert_alpha()  # Carrega a imagem com suporte a transparência


# Funções criar_bolas e iniciar_bola_branca fora da classe Ball
def criar_bolas(table):
    '''
    Inicializa as bolas de sinuca e as posiciona em formato triangular no canto superior direito da mesa.
    Cada bola recebe uma imagem correspondente e é adicionada à mesa de jogo.
    
    Args:
        table (Table): A mesa de sinuca onde as bolas serão posicionadas.
    '''
    raio_bola = 10  # Aumente o raio da bola
    massa_bola = 1
    espaco_entre_bolas = 5  # Aumentar o espaçamento entre as bolas para evitar sobreposição

    # Coordenadas ajustadas para centralizar no eixo y e deslocar um pouco mais à direita no eixo x
    x_inicial = table.x_start + table.largura * 0.7
    y_inicial = table.y_start + table.altura / 2 - (3 * raio_bola)

    contador_bola = 0
    for linha in range(5):
        for i in range(linha + 1):
            x_pos = x_inicial + (linha * (raio_bola * 2 + espaco_entre_bolas))
            y_pos = y_inicial + (i * (raio_bola * 2 + espaco_entre_bolas)) + (linha * raio_bola)
            
            # Carrega a imagem correspondente ao número da bola
            if contador_bola == 0:
                imagem_bola = 1
            elif contador_bola % 2 != 0:
                imagem_bola = 3
            else:
                imagem_bola =  2
                
            imagem_bola = carregar_imagem_bola(imagem_bola)
            
            # Cria a bola com a imagem redimensionada para o novo raio
            bola = Ball(numero=contador_bola + 1, raio=raio_bola, massa=massa_bola, posicao=(x_pos, y_pos), imagem=imagem_bola)
            bola.velocidade = (0, 0)
            table.bolas.append(bola)
            contador_bola += 1

def iniciar_bola_branca(table):
    '''
    Inicializa a bola branca em uma posição específica na mesa e define sua velocidade inicial.
    
    Args:
        table (Table): A mesa onde a bola branca será posicionada.
    '''
    # Carrega a imagem da bola branca
    imagem_bola_branca = carregar_imagem_bola(0)  # Supondo que a bola branca é "ball0.png"
    
    bola_branca = Ball(numero=0, raio=cfg.bola_branca_raio, 
                                 massa=cfg.bola_branca_massa, 
                                 posicao=cfg.bola_branca_posicao_inicial, 
                                 imagem=imagem_bola_branca)
    bola_branca.velocidade = (0, 0)
    table.bolas.append(bola_branca)
    table.bola_branca = bola_branca
