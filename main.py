import pygame
import sys
from utils.Table import Table
from utils.Ball import Ball, criar_bolas, iniciar_bola_branca
from utils.PhysicsEnvironment import PhysicsEnvironment
from time import sleep
from utils.button import button
from utils.Cue import Cue

display_width = 1200
display_height = 600



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
    table = Table(800, 400, ambiente_fisico,display_width, display_height)
    taco = Cue(table)
    
    buttons = [ button(10, 10, 100, 50, (0, 0, 255), 'Taco'),
               
                ]
    
    criar_bolas(table)
    iniciar_bola_branca(table)
    
    # adiciona um botao
    
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
        
        taco.draw(screen)
        for btt in buttons:
            btt.draw(screen)
        
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            for btt in buttons:
                if btt.is_clicked(x, y):
                    taco.play()
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
