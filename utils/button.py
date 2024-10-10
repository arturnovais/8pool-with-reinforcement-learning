import pygame

class button:
    '''
    Classe responsável por criar e gerenciar botões na interface gráfica do jogo.
    
    Args:
        x (int): A coordenada X da posição do botão.
        y (int): A coordenada Y da posição do botão.
        width (int): A largura do botão.
        height (int): A altura do botão.
        color (tuple): A cor do botão no formato RGB.
        text (str): O texto a ser exibido dentro do botão. Padrão é uma string vazia.
    '''
    
    def __init__(self, x, y, width, height, color, text=''):
        '''
        Inicializa o botão com as dimensões, cor e texto especificados.
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        
    def draw(self, screen: pygame.Surface):
        '''
        Desenha o botão na tela, incluindo o retângulo colorido e o texto centralizado.
        
        Args:
            screen (pygame.Surface): A superfície de jogo onde o botão será desenhado.
        '''
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))
    
    def is_clicked(self, x, y):
        '''
        Verifica se o botão foi clicado com base nas coordenadas do clique (x, y).
        
        Args:
            x (int): A coordenada X do clique do mouse.
            y (int): A coordenada Y do clique do mouse.
        
        Returns:
            bool: Retorna True se o botão foi clicado, False caso contrário.
        '''
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height
