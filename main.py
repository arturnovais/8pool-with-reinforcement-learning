
from utils.Table import Table

from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.button import button
import utils.config as cfg





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

    
    '''
    Configuração da física e criação dos objetos:
    Cria o ambiente físico para a simulação das colisões e movimentações das bolas na mesa.
    '''
    table = Table(cfg.display_table_width, cfg.display_table_height, 
                  ambiente_fisico= PhysicsEnvironment(),
                  display_width = cfg.display_width, 
                  display_height = cfg.display_height,
                  draw_game=True
                  )
    
    '''
    Criação dos botões:
    Inicializa um botão que poderá ser usado para controle de funcionalidade futura.
    '''
    
    buttons = [button(10, 10, 100, 50, (0, 0, 255), 'Taco')]
    
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
      

        '''
        Preenche a tela com uma cor de fundo preta, desenha a borda da mesa e renderiza
        os objetos da mesa, incluindo o taco e as bolas.
        '''
        
        table.exec_physics() # executa 1 unidade de tempo de física
        table.draw()
        
        '''
        Desenha os botões na tela.
        No momento, apenas um botão está presente, mas mais botões podem ser adicionados
        para expandir as funcionalidades do jogo.
        '''
        for btt in buttons:
            btt.draw(table.screen)


if __name__ == "__main__":
    '''
    Ponto de entrada do programa.
    
    Se o script for executado diretamente, a função main() será chamada,
    iniciando o jogo de sinuca.
    '''
    main()
