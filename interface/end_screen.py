import pygame
import sys
import utils.config as cfg

class EndScreen:
    def __init__(self, winner_name):
        """
        Inicializa a tela final com o nome do vencedor.
        """
        pygame.init()
        self.WIDTH = cfg.display_width
        self.HEIGHT = cfg.display_height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Parabéns ao Campeão!")
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 40)
        self.winner_name = winner_name

        # Carregar o plano de fundo
        self.background = pygame.image.load(cfg.celebration_walpapper).convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Botão para voltar ao menu principal
        self.menu_button_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 100, 200, 50)

    def run(self):
        """
        Executa a lógica da tela final.
        """
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))  # Desenha o plano de fundo

            # Texto principal
            title_surface = self.font.render("Parabéns ao Campeão!", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 100))
            self.screen.blit(title_surface, title_rect)

            # Nome do vencedor
            winner_surface = self.font.render(self.winner_name, True, (255, 215, 0))  # Texto dourado
            winner_rect = winner_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(winner_surface, winner_rect)

            # Botão para voltar ao menu
            pygame.draw.rect(self.screen, (50, 150, 50), self.menu_button_rect)
            button_text = self.small_font.render("Voltar ao Menu", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=self.menu_button_rect.center)
            self.screen.blit(button_text, button_rect)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button_rect.collidepoint(event.pos):
                        return "menu"  # Voltar ao menu principal

            pygame.display.flip()
