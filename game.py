
from utils.Table import Table

from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.button import button
import utils.config as cfg
from utils.Scoreboard import Scoreboard

class GAME:
    
    
    def __init__(self):
        
        self.Scoreboard = Scoreboard(['Player 1', 'Player 2'],game=self)
        self.table = Table(cfg.display_table_width, cfg.display_table_height, 
                  ambiente_fisico= PhysicsEnvironment(),
                  display_width = cfg.display_width, 
                  display_height = cfg.display_height,
                  draw_game=True,
                  scoreboard=self.Scoreboard,
                  game = self)
        self.table.reset()

        self.iniciou_jogada = False
        self.jogador_atual = 0
        self.iniciou_jogada_angulo = 0
        self.inicou_jogada_intensidade = 0
            

    def run_game(self):
        
        while True:
            self.jogador_atual = not self.jogador_atual
            
            print("Iniciando jogada", self.jogador_atual)
            
            while not self.iniciou_jogada:
                    self.table.draw() 
            information = self.table.step(angulo=self.iniciou_jogada_angulo,
                                    intensidade=self.inicou_jogada_intensidade)
            
            
            if len(information['colisoes']) > 0:
                
                assert 0 in [information['colisoes'][0][0].numero,
                             information['colisoes'][0][1].numero,
                             ]
                    
            print(information)
            
            # -> 
            # se a primeira colisao foi na bola dele
            
                    
            # se o jogador derrubou uma bola dele
                # repete a jogada
                
            # se o jogador derrubou uma bola do adversario
                # penalizado
            
            # se ele nao tocou nenhuma bola
                # penalizado
            
            # se ele derrubou a bola branca
                # penalizado
            
            # se ele derrubar a ultima bola 
                # depende 
            
            
            print("terminou a jogada")
            self.iniciou_jogada = False
        
            




def main():
    game = GAME()
    
    game.run_game()
    
    
if __name__ == "__main__":
    '''
    Ponto de entrada do programa.
    
    Se o script for executado diretamente, a função main() será chamada,
    iniciando o jogo de sinuca.
    '''
    main()
