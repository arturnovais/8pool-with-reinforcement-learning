import pygame
import sys
import utils.config as cfg


class InitialScreen:
    def __init__(self):
        """
        Inicializa a tela inicial com campos para nome dos jogadores e botão.
        """
        pygame.init()
        self.WIDTH = cfg.display_width
        self.HEIGHT = cfg.display_height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tela Inicial")
        
        # Fonte
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 40)

        # Botão Jogar
        self.button_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 120, 200, 80)  # Ajustado para ficar mais acima

        # Botões de Cenário
        self.inf_button_rect = pygame.Rect(self.WIDTH // 2 - 400, self.HEIGHT - 160, 200, 100)
        self.night_button_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 160, 200, 100)
        self.mamaco_button_rect = pygame.Rect(self.WIDTH // 2 + 200, self.HEIGHT - 160, 200, 100)

        # Background das opções de cenário
        self.inf_background = pygame.image.load('imgs/Background/inf1.jpg').convert()
        self.inf_background = pygame.transform.scale(self.inf_background, (200, 100))

        self.night_background = pygame.image.load('imgs/Background/bar1.jpg').convert()
        self.night_background = pygame.transform.scale(self.night_background, (200, 100))

        self.mamaco_background = pygame.image.load('imgs/Background/apes_planet.png').convert()
        self.mamaco_background = pygame.transform.scale(self.mamaco_background, (200, 100))

        # Background inicial
        self.selected_background = cfg.background_image  # Background padrão
        self.current_background = pygame.image.load(cfg.initial_screen_background).convert()
        self.current_background = pygame.transform.scale(self.current_background, (self.WIDTH, self.HEIGHT))

        # Campos de texto para os nomes dos jogadores
        self.input_boxes = [
            pygame.Rect(self.WIDTH // 2 - 200, self.HEIGHT // 2 - 150, 400, 50),  # Player 1 (mover mais para cima)
            pygame.Rect(self.WIDTH // 2 - 200, self.HEIGHT // 2 - 70, 400, 50)  # Player 2 (mover mais para cima)
        ]
        self.active_box = None
        self.player_names = ["Player 1", "Player 2"]
        self.input_texts = ["Player 1", "Player 2"]
        self.default_texts = ["Player 1", "Player 2"]  # Valores padrão
        
        self.title_font = pygame.font.Font(cfg.tittle_font, 80)

    def draw_button_with_background(self, rect, background, label):
        """
        Desenha um botão com um fundo de imagem.
        
        Args:
            rect (pygame.Rect): Retângulo que representa o botão.
            background (pygame.Surface): Imagem de fundo do botão.
            label (str): Texto a ser exibido no botão.
        """
        self.screen.blit(background, rect.topleft)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)  # Borda
        text_surface = self.small_font.render(label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_input_boxes(self):
        """
        Desenha os campos de entrada de texto para os nomes dos jogadores.
        """
        for i, box in enumerate(self.input_boxes):
            color = (0, 0, 0)  # Texto preto nos campos
            pygame.draw.rect(self.screen, (255, 255, 255), box)  # Fundo branco
            pygame.draw.rect(self.screen, (0, 0, 0), box, 2)  # Borda preta
            text_surface = self.small_font.render(self.input_texts[i], True, color)
            text_rect = text_surface.get_rect(center=box.center)
            self.screen.blit(text_surface, text_rect)
            
    def draw_title(self, text):
        """
        Desenha o título na parte superior da tela.
        
        Args:
            text (str): O texto a ser exibido como título.
        """
        title_surface = self.title_font.render(text, True, (255, 255, 255))  # Texto branco
        title_rect = title_surface.get_rect(center=(self.WIDTH // 2, 50))  # Centralizado no topo
        self.screen.blit(title_surface, title_rect)


    def run(self):
        """
        Executa a lógica da tela inicial.
        
        Returns:
            tuple: Retorna os nomes dos jogadores e o background selecionado.
        """
        running = True
        while running:
            # Desenhar o background
            self.screen.blit(self.current_background, (0, 0))
            
            # Capturar eventos
            mouse_pos = pygame.mouse.get_pos()
            is_hovered_play = self.button_rect.collidepoint(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        if is_hovered_play:  # Botão "Jogar" clicado
                            return self.input_texts, self.selected_background

                        # Detectar clique nos botões de cenário
                        if self.inf_button_rect.collidepoint(event.pos):
                            self.selected_background = 'imgs/Background/inf1.jpg'
                            self.current_background = self.inf_background
                        elif self.night_button_rect.collidepoint(event.pos):
                            self.selected_background = 'imgs/Background/bar1.jpg'
                            self.current_background = self.night_background
                        elif self.mamaco_button_rect.collidepoint(event.pos):
                            self.selected_background = 'imgs/Background/apes_planet.png'
                            self.current_background = self.mamaco_background

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
            
            # Desenhar campos de entrada, botão "Jogar" e botões de cenário
            self.draw_title("SINUCA DOS APES")
            self.draw_input_boxes()
            self.draw_button_with_background(self.inf_button_rect, self.inf_background, "INF")
            self.draw_button_with_background(self.night_button_rect, self.night_background, "Night")
            self.draw_button_with_background(self.mamaco_button_rect, self.mamaco_background, "Mamaco")
            pygame.draw.rect(self.screen, (50, 150, 50), self.button_rect)  # Botão verde
            text_surface = self.font.render("Jogar", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.button_rect.center)
            self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
