import pygame
import sys
import utils.config as cfg  # Certifique-se de que cfg é acessível e configurado

class InitialScreen:
    def __init__(self, width=1400, height=800):
        """
        Inicializa a tela inicial com background e configurações.
        
        Args:
            width (int): Largura da tela.
            height (int): Altura da tela.
        """
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tela Inicial")
        
        # Cores
        self.BUTTON_COLOR = (50, 150, 50)
        self.BUTTON_HOVER_COLOR = (70, 200, 70)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Fonte
        self.font = pygame.font.Font(None, 60)

        # Botão
        self.button_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50, 200, 100)  # Botão centralizado

        # Background
        self.background = pygame.image.load(cfg.initial_screen_background).convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
    
    def draw_button(self, text, is_hovered):
        """
        Desenha o botão na tela.
        
        Args:
            text (str): Texto a ser exibido no botão.
            is_hovered (bool): Indica se o botão está sendo "hovered" pelo mouse.
        """
        color = self.BUTTON_HOVER_COLOR if is_hovered else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.button_rect)
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """
        Executa a lógica da tela inicial.
        
        Returns:
            bool: Retorna True quando o botão "Jogar" é clicado.
        """
        running = True
        while running:
            # Desenhar o background
            self.screen.blit(self.background, (0, 0))
            
            # Capturar eventos
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = self.button_rect.collidepoint(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clique esquerdo
                    if is_hovered:
                        return True  # Botão "Jogar" clicado, inicia o jogo
            
            # Desenhar botão
            self.draw_button("Jogar", is_hovered)
            
            pygame.display.flip()
