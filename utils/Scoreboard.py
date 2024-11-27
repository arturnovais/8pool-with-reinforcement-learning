import pygame
import utils.config as cfg


class Scoreboard:
    '''
    Classe que gerencia o placar do jogo de sinuca, registrando bolas encaçapadas e alternando entre os jogadores.
    
    Args:
        jogadores (list): Uma lista de instâncias da classe Player representando os jogadores.
    '''
    
    def __init__(self, jogadores: list, game):
        '''
        Inicializa o placar do jogo de sinuca.
        '''
        self.jogadores = jogadores
        self.game = game

    def draw(self, screen):
        """
        Desenha o placar na tela do jogo.
        """
        pygame.font.init()
        font = pygame.font.Font(None, 30)  # Fonte menor
        header_font = pygame.font.Font(None, 40)  # Fonte menor para o título

        # Tamanho da tela e mesa com base em config
        screen_width = cfg.display_width
        screen_height = cfg.display_height
        table_width = cfg.display_table_width
        table_height = cfg.display_table_height

        # Define cores e estilos
        background_color = (30, 30, 30)  # Fundo do placar
        header_color = (200, 200, 200)  # Cor do título
        active_player_color = (255, 100, 100)  # Destaque para o jogador atual
        text_color = (255, 255, 255)  # Cor do texto normal

        # Dimensões ajustadas do placar (reduzido)
        placar_width = int(screen_width * 0.15)  # 15% da largura da tela
        placar_height = 80 + len(self.jogadores) * 40  # Caixas menores
        placar_x = 10  # Margem esquerda fixa
        placar_y = 10  # Margem superior fixa

        # Ajuste para evitar interferência na mesa
        if placar_height > table_height:
            placar_height = table_height - 20  # Limite para não ultrapassar a mesa

        # Desenhar fundo do placar
        placar_rect = pygame.Rect(placar_x, placar_y, placar_width, placar_height)
        pygame.draw.rect(screen, background_color, placar_rect)
        pygame.draw.rect(screen, (255, 255, 255), placar_rect, 2)  # Borda do placar

        # Escrever título
        header_text = header_font.render("Placar", True, header_color)
        screen.blit(header_text, (placar_rect.centerx - header_text.get_width() // 2, placar_y + 5))

        # Listar os jogadores
        for i, jogador in enumerate(self.jogadores):
            # Verificar se é o jogador atual
            if self.game.jogador_atual == i:
                bg_color = active_player_color
            else:
                bg_color = background_color

            # Caixa de cada jogador
            player_rect = pygame.Rect(placar_x + 5, placar_y + 40 + i * 40, placar_width - 10, 30)
            pygame.draw.rect(screen, bg_color, player_rect)
            pygame.draw.rect(screen, (255, 255, 255), player_rect, 1)  # Borda

            # Quantidade de bolas restantes
            bolas_jogador = [b for b in self.game.numero_bolas[i]]
            bolas_jogador_mesa = [b.numero for b in self.game.table.bolas if b.numero in bolas_jogador]

            # Texto do jogador
            player_text = font.render(
                f"{self.jogadores[i]}: {len(bolas_jogador_mesa)}/{len(bolas_jogador)}",
                True,
                text_color
            )
            screen.blit(player_text, (player_rect.x + 5, player_rect.y + 5))
