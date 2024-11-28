import pygame
from utils.PhysicsEnvironment import PhysicsEnvironment
import utils.config as  cfg
import random
import torch

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
        self.massa = torch.tensor(massa, device=cfg.device, dtype=torch.float32)
        self.posicao = torch.tensor(posicao, device=cfg.device, dtype=torch.float32)
        self.velocidade = torch.tensor(velocidade, device=cfg.device, dtype=torch.float32)
#        self.aceleracao = torch.tensor((0,0), device=cfg.device, dtype=torch.float32)
        self.rotação = rotação
        self.spin = 0
        self.player = -1

        
        self.dt = torch.tensor(cfg.delta_tempo, device=cfg.device, dtype=torch.float32)
        
        self.visual_raio = raio * 2  # Raio visual para o dobro do tamanho
        if imagem is not None:
            # Redimensiona a imagem para o dobro do tamanho da bola (baseado no raio visual)
            self.imagem = pygame.transform.scale(imagem, (int(self.visual_raio * 2), int(self.visual_raio * 2)))
        else:
            self.imagem = None

    def aplicar_forca(self, forca: tuple):
        '''
        Aplica uma força à bola, ajustando sua aceleração e velocidade de acordo com a segunda lei de Newton.
        
        Args:
            forca (tuple): Força aplicada à bola nas direções (fx, fy), em Newtons.
            dt (float): Intervalo de tempo em segundos durante o qual a força é aplicada.
        '''
        
        forca = torch.tensor(forca, device=cfg.device, dtype=torch.float32) / self.massa
        self.velocidade = self.velocidade + forca * self.dt
        
    
    #def atualizar_estado_bola(self, bola: Ball, dt: float):
    #    '''
    #    Atualiza a posição da bola considerando as forças de atrito e resistência do ar.
    #    
    #    Args:
    #        bola (Ball): A bola cujo estado será atualizado.
    #        dt (float): Intervalo de tempo (em segundos) para atualização.
    #    '''
    #    bola.velocidade = self.ambiente_fisico.aplicar_atrito(bola.velocidade)
    #    bola.velocidade = self.ambiente_fisico.aplicar_resistencia_ar(bola.velocidade)
#
    #    bola.posicao = bola.posicao + bola.velocidade * dt
    #    
        
    def atualizar_posicao(self, ambiente_fisico: PhysicsEnvironment):
        '''
        Atualiza a posição da bola levando em consideração a velocidade atual, o atrito e a resistência do ar.
        
        Args:
            dt (float): Intervalo de tempo para atualização, em segundos.
            ambiente_fisico (PhysicsEnvironment): Ambiente físico que define atrito e resistência.
        '''
        self.velocidade = ambiente_fisico.aplicar_atrito(self.velocidade)
        self.velocidade = ambiente_fisico.aplicar_resistencia_ar(self.velocidade)

        if self.velocidade.abs().sum() < 0.01:
            self.velocidade = torch.tensor([0, 0], device=cfg.device, dtype=torch.float32)

        self.posicao = self.posicao + self.velocidade * self.dt
        
        #self.aplicar_spin()

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
        caminho_imagem = f"imgs/Balls/ball{numero}.png"  # Assumindo que as imagens estão em "imagens/ballX.png"
        return pygame.image.load(caminho_imagem).convert_alpha()  # Carrega a imagem com suporte a transparência


# Funções criar_bolas e iniciar_bola_branca fora da classe Ball
def criar_bolas(table):
    '''
    Inicializa as bolas de sinuca e as posiciona em formato triangular no canto superior direito da mesa.
    Cada bola recebe uma imagem correspondente e é adicionada à mesa de jogo.
    
    Args:
        table (Table): A mesa de sinuca onde as bolas serão posicionadas.
    '''
    raio_bola = cfg.bola_raio  # Aumente o raio da bola
    massa_bola = cfg.bola_massa
    espaco_entre_bolas = 5  # Aumentar o espaçamento entre as bolas para evitar sobreposição

    # Coordenadas ajustadas para centralizar no eixo y e deslocar um pouco mais à direita no eixo x
    x_inicial = table.x_start + table.largura * 0.7
    y_inicial = table.y_start + table.altura / 2 - (3 * raio_bola)

    
    
    positions = []
    for linha in range(5):
        if linha == 0:
            continue
        
        for i in range(linha + 1):
            x_pos = x_inicial + (linha * (raio_bola * 2 + espaco_entre_bolas))
            y_pos = table.y_start + (table.altura / 2) - ((linha) * (raio_bola * 2 + espaco_entre_bolas))/2
            y_pos += i * (raio_bola * 2 + espaco_entre_bolas)
            positions += [(x_pos, y_pos)]
    random.shuffle(positions)
    
    
    positions_ball_1= (table.x_start + cfg.bola_branca_raio+1,cfg.bola_branca_posicao_inicial[1])
    positions =  [positions_ball_1] + positions
            
    for contador_bola, position in enumerate(positions,start=1):
            if contador_bola == 1:
                imagem_bola = 1
            elif contador_bola % 2 != 0:
                imagem_bola = 3
            else:
                imagem_bola =  2
                
            imagem_bola = carregar_imagem_bola(imagem_bola)
            
            # Cria a bola com a imagem redimensionada para o novo raio
            bola = Ball(numero=contador_bola, raio=raio_bola, massa=massa_bola, posicao=position, imagem=imagem_bola, velocidade=(0, 0))
            table.bolas.append(bola)

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
                                 imagem=imagem_bola_branca,
                                 velocidade=(0, 0)
                                 )
    table.bolas.append(bola_branca)
    table.bola_branca = bola_branca
