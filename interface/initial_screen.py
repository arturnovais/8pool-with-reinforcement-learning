import pygame
import sys
import utils.config as cfg  # Certifique-se de que cfg é acessível e configurado


class InitialScreen:
    def __init__(self, width=1400, height=800):
        """
        Inicializa a tela inicial com campos para nome dos jogadores e botão.
        
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
        self.BOX_COLOR = (200, 200, 200)
        self.BOX_ACTIVE_COLOR = (150, 150, 150)
        self.FONT_COLOR = (0, 0, 0)
        
        # Fonte
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 40)

        # Botão
        self.button_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 150, 200, 100)

        # Background
        self.background = pygame.image.load(cfg.initial_screen_background).convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Campos de texto para os nomes dos jogadores
        self.input_boxes = [
            pygame.Rect(self.WIDTH // 2 - 200, self.HEIGHT // 2 - 100, 400, 50),  # Player 1
            pygame.Rect(self.WIDTH // 2 - 200, self.HEIGHT // 2, 400, 50)  # Player 2
        ]
        self.active_box = None
        self.player_names = ["Player 1", "Player 2"]
        self.input_texts = ["Player 1", "Player 2"]
        self.default_texts = ["Player 1", "Player 2"]  # Valores padrão

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

    def draw_input_boxes(self):
        """
        Desenha os campos de entrada de texto para os nomes dos jogadores.
        """
        for i, box in enumerate(self.input_boxes):
            color = self.BOX_ACTIVE_COLOR if self.active_box == i else self.BOX_COLOR
            pygame.draw.rect(self.screen, color, box)
            
            # Verificar se o texto é o valor padrão e o campo não está ativo
            if self.input_texts[i] == self.default_texts[i] and self.active_box != i:
                text_color = (150, 150, 150)  # Cor cinza para texto de placeholder
            else:
                text_color = self.FONT_COLOR
            
            text_surface = self.small_font.render(self.input_texts[i], True, text_color)
            text_rect = text_surface.get_rect(center=box.center)
            self.screen.blit(text_surface, text_rect)

    def run(self):
        """
        Executa a lógica da tela inicial.
        
        Returns:
            list: Retorna os nomes dos jogadores após o botão "Jogar" ser clicado.
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        if is_hovered:  # Botão "Jogar" clicado
                            # Substituir texto padrão se não tiver sido alterado
                            for i, text in enumerate(self.input_texts):
                                if text == self.default_texts[i]:
                                    self.input_texts[i] = self.default_texts[i]
                            return self.input_texts  # Retorna os nomes dos jogadores

                        # Verificar se clicou em um campo de texto
                        for i, box in enumerate(self.input_boxes):
                            if box.collidepoint(event.pos):
                                self.active_box = i
                                if self.input_texts[i] == self.default_texts[i]:
                                    self.input_texts[i] = ""  # Limpar o texto padrão ao clicar
                                break
                        else:
                            self.active_box = None
                if event.type == pygame.KEYDOWN:
                    if self.active_box is not None:  # Se um campo de texto estiver ativo
                        if event.key == pygame.K_BACKSPACE:
                            self.input_texts[self.active_box] = self.input_texts[self.active_box][:-1]
                        elif len(self.input_texts[self.active_box]) < 20:  # Limite de caracteres
                            self.input_texts[self.active_box] += event.unicode
            
            # Desenhar campos de entrada e botão
            self.draw_input_boxes()
            self.draw_button("Jogar", is_hovered)
            
            pygame.display.flip()
