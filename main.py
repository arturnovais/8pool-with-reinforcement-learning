
from utils.Table import Table

from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.button import button
import utils.config as cfg





def main():
    
    table = Table(cfg.display_table_width, cfg.display_table_height, 
                  ambiente_fisico= PhysicsEnvironment(),
                  display_width = cfg.display_width, 
                  display_height = cfg.display_height,
                  draw_game=True
                  )
    
    
   # buttons = [button(10, 10, 100, 50, (0, 0, 255), 'Taco')]
    
    table.reset()
    print("STATER GAME")
    information = table.step(10,1)    
    
    
if __name__ == "__main__":
    '''
    Ponto de entrada do programa.
    
    Se o script for executado diretamente, a função main() será chamada,
    iniciando o jogo de sinuca.
    '''
    main()
