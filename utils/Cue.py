import math
import pygame

class Cue:
    '''
    Classe responsável por representar o taco de sinuca, controlando a direção e a intensidade da tacada,
    além de desenhar o taco e a barra de intensidade na interface do jogo.
    
    Args:
        table (Table): A mesa onde o taco será utilizado, que contém a bola branca.
        força_maxima (float): Define a força máxima que o taco pode aplicar (em Newtons). Valor padrão: 200.0.
    '''
    
    def __init__(self, table, força_maxima: float = 200.0):
        '''
        Inicializa o taco com a mesa associada e configura a força máxima da tacada, além da
        intensidade inicial da tacada e o controle de travamento de direção.
        '''
        self.table = table
        self.força_maxima = força_maxima
        self.intensidade = 0
        self.intensidade_incremento = 0.01
        self.lance_travado = False
        self.angulo_travado = None

    def calcular_forca(self, intensidade: float, angulo: float) -> tuple:
        '''
        Calcula a força a ser aplicada na bola com base na intensidade da tacada e no ângulo.

        Args:
            intensidade (float): A intensidade da tacada, variando de 0 a 1.
            angulo (float): O ângulo da tacada em radianos.

        Returns:
            tuple: Um par de valores (fx, fy) representando a força aplicada nas direções x e y.
        '''
        intensidade = min(max(intensidade, 0), 1)
        forca_total = intensidade * self.força_maxima
        fx = forca_total * math.cos(angulo)
        fy = forca_total * math.sin(angulo)
        return fx, fy

    def aplicar_tacada(self, bola, intensidade: float, angulo: float):
        '''
        Aplica a tacada na bola branca, calculando a força a ser aplicada com base
        na intensidade e no ângulo travado.

        Args:
            bola (Ball): A bola que será atingida (normalmente a bola branca).
            intensidade (float): A intensidade da tacada (0 a 1).
            angulo (float): O ângulo da tacada em radianos.
        '''
        forca = self.calcular_forca(intensidade, angulo)
        bola.aplicar_forca(forca, dt=0.1)

    def is_enable(self) -> bool:
        '''
        Verifica se o taco está pronto para ser usado, ou seja, se a bola branca está parada.

        Returns:
            bool: True se a bola branca estiver parada, indicando que o taco pode ser usado.
        '''
        return self.table.bola_branca.velocidade == (0, 0)

    def draw(self, screen: pygame.Surface):
        '''
        Desenha o taco e a barra lateral de intensidade na tela do jogo.
        Se a direção da tacada não estiver travada, o taco segue a posição do mouse.

        Args:
            screen (pygame.Surface): A superfície de jogo onde os elementos serão desenhados.
        '''
        if self.is_enable():
            if not self.lance_travado:
                x, y = self.table.bola_branca.posicao
                mx, my = pygame.mouse.get_pos()
                pygame.draw.line(screen, (88, 51, 0), (x, y), (mx, my), 6)

            self.draw_intensidade_bar(screen)

    def draw_intensidade_bar(self, screen: pygame.Surface):
        '''
        Desenha uma barra lateral na tela que exibe a intensidade da tacada.
        A cor da barra varia de verde (baixa intensidade) a vermelho (alta intensidade).

        Args:
            screen (pygame.Surface): A superfície de jogo onde a barra será desenhada.
        '''
        bar_x = 1100
        bar_y = 100
        bar_width = 30
        bar_height = 400

        intensidade_color = (
            int(255 * self.intensidade),
            int(255 * (1 - self.intensidade)),
            0
        )

        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        filled_height = self.intensidade * bar_height
        pygame.draw.rect(screen, intensidade_color, (bar_x, bar_y + bar_height - filled_height, bar_width, filled_height))

    def clicked(self):
        '''
        Método chamado quando o jogador clica na tela.
        Se a direção da tacada não estiver travada, ela será travada com base na posição do mouse.
        Se a direção estiver travada, a tacada será aplicada com a intensidade e o ângulo definidos.
        '''
        if self.is_enable() and not self.lance_travado:
            x, y = self.table.bola_branca.posicao
            mx, my = pygame.mouse.get_pos()

            angulo = math.atan2(my - y, mx - x)

            self.angulo_travado = angulo
            self.lance_travado = True
        elif self.lance_travado:
            self.aplicar_tacada(self.table.bola_branca, self.intensidade, self.angulo_travado)
            self.intensidade = 0
            self.lance_travado = False

    def ajustar_intensidade_com_mouse(self, mouse_y, screen_height):
        '''
        Ajusta a intensidade da tacada com base na posição vertical do mouse.
        Quanto mais alto o mouse estiver na barra lateral, maior a intensidade.

        Args:
            mouse_y (int): A coordenada Y do mouse.
            screen_height (int): A altura total da tela do jogo.
        '''
        bar_y = 100
        bar_height = 400

        pos_relativa = (mouse_y - bar_y) / bar_height
        self.intensidade = min(max(1 - pos_relativa, 0), 1)
