import pygame
import sys
from classes.Table import Table
from classes.Ball import Ball
from classes.PhysicsEnvironment import PhysicsEnvironment
from time import sleep

display_width = 1200
display_height = 1000

def criar_bolas(table):
    """
    Função para inicializar as bolas com posições e cores adequadas em um formato triangular,
    no canto superior direito da mesa, independentemente da posição da mesa.
    """
    cores = [
        (255, 255, 0),    # Amarelo
        (255, 0, 0),      # Vermelho
        (0, 255, 0),      # Verde
        (0, 0, 255),      # Azul
        (255, 20, 147),   # Rosa
        (0, 0, 0),        # Preto
        (255, 165, 0),    # Laranja
        (139, 69, 19),    # Marrom
        (255, 255, 255),  # Bola Branca
        # Listradas
        (255, 192, 203),  # Listrada rosa
        (0, 128, 128),    # Listrada ciano
        (128, 0, 128),    # Listrada roxa
    ]

    raio_bola = 10
    massa_bola = 1
    espaco_entre_bolas = 2  # Espaço extra entre as bolas para evitar sobreposição

    # Coordenadas iniciais para o triângulo de bolas no canto superior direito da mesa
    x_inicial = table.x_start + table.largura - (5 * raio_bola * 2) - espaco_entre_bolas  # Deixa espaço no lado direito da mesa
    y_inicial = table.y_start + (raio_bola * 2)  # Posiciona logo abaixo do topo da mesa

    contador_bola = 0
    for linha in range(5):
        for i in range(linha + 1):
            # Calcula a posição de cada bola, com espaçamento adequado
            x_pos = x_inicial + (linha * (raio_bola * 2 + espaco_entre_bolas))
            y_pos = y_inicial + (i * (raio_bola * 2 + espaco_entre_bolas)) + (linha * raio_bola)
            bola = Ball(numero=contador_bola + 1, raio=raio_bola, massa=massa_bola, posicao=(x_pos, y_pos))
            bola.velocidade = (0, 0)  # Todas começam paradas
            bola.cor = cores[contador_bola % len(cores)]  # Atribui uma cor para cada bola
            table.bolas.append(bola)
            contador_bola += 1


def iniciar_bola_branca(table):
    """
    Função para inicializar a bola branca na posição correta e com uma velocidade inicial.
    """
    bola_branca = Ball(numero=0, raio=10, massa=1, posicao=(150, 500))  
    bola_branca.velocidade = (100, 100)  
    bola_branca.cor = (255, 255, 255)  
    table.bolas.append(bola_branca)

def desenhar_borda(screen, x_start, y_start, largura, altura):
    """
    Desenha a borda da mesa de sinuca em torno da área verde.
    """
    cor_borda = (139, 69, 19)  # Marrom para a borda
    espessura_borda = 20  # Largura da borda
    pygame.draw.rect(screen, cor_borda, (x_start - espessura_borda, y_start - espessura_borda,
                                         largura + 2 * espessura_borda, altura + 2 * espessura_borda))

def main():
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Sinuca")
    clock = pygame.time.Clock()
    ambiente_fisico = PhysicsEnvironment()
    table = Table(800, 400, ambiente_fisico)

    criar_bolas(table)
    iniciar_bola_branca(table)

    while True:
        #sleep(0.3)
        for event in pygame.event.get():
            #sleep(0.1)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Fundo preto

        # Desenha a borda antes da mesa
        desenhar_borda(screen, table.x_start, table.y_start, table.largura, table.altura)

        # Desenha a mesa e as bolas
        table.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
