import pygame
import utils.config as cfg


class Scoreboard:
    def __init__(self, jogadores: list, game):
        """
        Inicializa o placar do jogo de sinuca.
        """
        self.jogadores = jogadores
        self.game = game
        self.bolas_imagens = [None, None]  # Armazena a imagem da bola associada a cada jogador

    def draw(self, screen):
        """
        Desenha o placar na tela do jogo.
        """
        pygame.font.init()
        font = pygame.font.Font(None, 30)
        header_font = pygame.font.Font(None, 40)

        # Dimensões e cores
        screen_width = cfg.display_width
        background_color = (30, 30, 30)
        active_player_color = (255, 100, 100)
        text_color = (255, 255, 255)

        placar_width = int(screen_width * 0.15)
        placar_height = 80 + len(self.jogadores) * 40
        placar_x, placar_y = 10, 10

        # Desenhar fundo do placar
        placar_rect = pygame.Rect(placar_x, placar_y, placar_width, placar_height)
        pygame.draw.rect(screen, background_color, placar_rect)
        pygame.draw.rect(screen, (255, 255, 255), placar_rect, 2)

        # Escrever título
        header_text = header_font.render("Placar", True, text_color)
        screen.blit(header_text, (placar_rect.centerx - header_text.get_width() // 2, placar_y + 5))

        # Listar os jogadores
        for i, jogador in enumerate(self.jogadores):
            bg_color = active_player_color if self.game.jogador_atual == i else background_color

            # Caixa de cada jogador
            player_rect = pygame.Rect(placar_x + 5, placar_y + 40 + i * 40, placar_width - 10, 30)
            pygame.draw.rect(screen, bg_color, player_rect)
            pygame.draw.rect(screen, (255, 255, 255), player_rect, 1)

            # Imagem da bola associada
            if self.bolas_imagens[i] is not None:
                # Exibir a imagem associada ao jogador
                img_x = player_rect.x + 5
                img_y = player_rect.y + 5
                screen.blit(self.bolas_imagens[i], (img_x, img_y))

            # Texto do jogador
            bolas_jogador = [b for b in self.game.numero_bolas[i]]
            bolas_jogador_mesa = [b.numero for b in self.game.table.bolas if b.numero in bolas_jogador]
            player_text = font.render(
                f"{self.jogadores[i]}: {len(bolas_jogador_mesa)}/{len(bolas_jogador)}",
                True,
                text_color
            )
            screen.blit(player_text, (player_rect.x + 40, player_rect.y + 5))  # Ajuste para dar espaço à imagem
