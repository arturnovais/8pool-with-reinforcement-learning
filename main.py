import pygame
import sys
from utils.Table import Table
from utils.Ball import Ball, criar_bolas, iniciar_bola_branca
from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.button import button
from utils.Cue import Cue

display_width = 1200
display_height = 600


def desenhar_borda(screen, x_start, y_start, largura, altura):
    '''
    Desenha a borda da mesa de sinuca.

    A função recebe as coordenadas da mesa e desenha uma borda ao redor
    da área de jogo. A cor da borda é marrom, simbolizando madeira.

    Args:
        screen (Surface): A superfície onde a borda será desenhada (tela principal do jogo).
        x_start (int): Coordenada X inicial da área da mesa.
        y_start (int): Coordenada Y inicial da área da mesa.
        largura (int): A largura da mesa.
        altura (int): A altura da mesa.
    '''
    cor_borda = (139, 69, 19)
    espessura_borda = 20
    pygame.draw.rect(screen, cor_borda, (x_start - espessura_borda, y_start - espessura_borda,
                                         largura + 2 * espessura_borda, altura + 2 * espessura_borda))


def main():
    '''
    Função principal do jogo de sinuca.

    Essa função inicializa o Pygame e configura a tela de jogo. Ela também cria os objetos
    necessários, como a mesa, as bolas e o taco. O loop principal captura eventos de entrada,
    atualiza a tela e verifica interações como cliques e movimentos do mouse para ajustar a
    intensidade da tacada.
    
    O jogo usa um sistema de física para movimentação e colisão das bolas, e uma interface
    simples com botões para futuras funcionalidades.
    '''
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Sinuca")
    clock = pygame.time.Clock()
    
    '''
    Configuração da física e criação dos objetos:
    Cria o ambiente físico para a simulação das colisões e movimentações das bolas na mesa.
    '''
    ambiente_fisico = PhysicsEnvironment()
    table = Table(800, 400, ambiente_fisico, display_width, display_height)
    taco = Cue(table)
    
    '''
    Criação dos botões:
    Inicializa um botão que poderá ser usado para controle de funcionalidade futura.
    '''
    buttons = [button(10, 10, 100, 50, (0, 0, 255), 'Taco')]
    
    '''
    Criação e inicialização das bolas na mesa.
    As bolas são criadas e posicionadas de forma adequada na mesa de sinuca.
    '''
    criar_bolas(table)
    iniciar_bola_branca(table)
    
    
    '''
    Loop principal do jogo:
    Captura e processa eventos do jogo, como fechar a janela ou clicar para aplicar a tacada.
    Atualiza a tela do jogo desenhando a mesa, taco, borda e outros elementos. O loop é responsável
    por manter o jogo funcionando a 60 frames por segundo (FPS).
    '''
    while True:
        '''
        Captura eventos de entrada do Pygame, como o fechamento da janela ou cliques do mouse.
        Se um clique for detectado, a função taco.clicked() será chamada para aplicar a tacada
        ou travar a direção.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                taco.clicked()

        '''
        Se a direção da tacada estiver travada, permite ajustar a intensidade
        com base na posição vertical do mouse.
        '''
        if taco.lance_travado:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            taco.ajustar_intensidade_com_mouse(mouse_y, display_height)

        '''
        Preenche a tela com uma cor de fundo preta, desenha a borda da mesa e renderiza
        os objetos da mesa, incluindo o taco e as bolas.
        '''
        screen.fill((0, 0, 0))
        desenhar_borda(screen, table.x_start, table.y_start, table.largura, table.altura)
        table.draw(screen)
        taco.draw(screen)
        
        '''
        Desenha os botões na tela.
        No momento, apenas um botão está presente, mas mais botões podem ser adicionados
        para expandir as funcionalidades do jogo.
        '''
        for btt in buttons:
            btt.draw(screen)

        '''
        Atualiza a tela exibindo todas as alterações visuais feitas no frame atual.
        O loop é ajustado para rodar a uma taxa de 60 frames por segundo (FPS).
        '''
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    '''
    Ponto de entrada do programa.
    
    Se o script for executado diretamente, a função main() será chamada,
    iniciando o jogo de sinuca.
    '''
    main()
