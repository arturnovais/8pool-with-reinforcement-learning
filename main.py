import pygame
import sys
from classes.Table import Table
from classes.Ball import Ball
from classes.PhysicsEnvironment import PhysicsEnvironment


display_width = 800
display_height = 600


def main():
    
    
    # create a game with pygame
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Sinuca")
    clock = pygame.time.Clock()
    ambiente_fisico = PhysicsEnvironment()
    table = Table(500, 300, ambiente_fisico)
    
    raio_bola = 10
    bola = Ball(numero = 0, raio = raio_bola, massa=1, posicao=(100 + 20, 100 + 150),
                velocidade=(14,10))
    
    table.bolas.append(bola)
    
    bola2 = Ball(numero = 1, raio = raio_bola, massa=0.6, posicao=(100 + 150, 100 + 150),
                velocidade=(0,0))
    
    table.bolas.append(bola2)
    
    
    
    # create a loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((0, 0, 0))
        table.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
        
    