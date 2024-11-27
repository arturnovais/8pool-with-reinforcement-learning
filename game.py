
from utils.Table import Table
from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.button import button
import utils.config as cfg
from utils.Scoreboard import Scoreboard

from interface.initial_screen import InitialScreen


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

        # comando para controlar o jogo.... o TACO INTERFERE NESSAS VARIAVEIS
        self.iniciou_jogada = False
        self.jogador_atual = 0
        self.iniciou_jogada_angulo = 0
        self.inicou_jogada_intensidade = 0
        
        
        self.numero_bolas = [[],[]] # numero das bolas que cada jogador deve derrubar
        
    def reset(self):
        self.__init__()
        
        
    def rules(self, information, idx_player):
        # funcao que verifica as regras do jogo
        
        table = self if type(self) == Table else self.table
        
        bolas_caidas_sem_branca = [b for b in information['bolas_caidas'] if b.numero!= 0]
        fez_bola_branca = 0 in [b.numero for b in information['bolas_caidas']]
        
        # algum jogador já fez suas bolas?
        
        information['perdeu'] = False
        information['ganhou'] = False
        information['penalizado'] = False
        information['joga_novamente'] = False
        
        if len(self.table.bolas) == 16:
            #Ninguem fez nenhuma bola ainda
            return information
        
        elif (len(self.table.bolas) + len(bolas_caidas_sem_branca) == 16):
            """
                Jogador fez a primeira bola da partida                
            """
            
            first_ball = bolas_caidas_sem_branca[0].numero
            
            bolas_jogador    = [2,4,6,8,10,12,14]
            bolas_adversario = [3,5,7,9,11,13,15]
            if first_ball % 2 != 0:
                bolas_jogador    = [3,5,7,9,11,13,15]
                bolas_adversario = [2,4,6,8,10,12,14]
            
            if idx_player == 0:
                self.numero_bolas = [bolas_jogador, bolas_adversario]
            else:
                self.numero_bolas = [bolas_adversario, bolas_jogador]
            
            if 1 in [b.numero for b in bolas_caidas_sem_branca]:
                # se todas as bolas do jogadore cairem
                if all([b.numero in bolas_jogador for b in bolas_caidas_sem_branca]):
                    information['ganhou'] = True
                    return information
                else:
                    information['perdeu'] = True
                    return information
                
            ###############################################################################
            #######  verifica se ele deve jogar novament e / ou pagar uma bola       ######

            # se ele fez uma bola do adversario ele passa a vez
            fez_adversario = False
            for b in bolas_caidas_sem_branca:
                if b.numero in bolas_adversario:
                    fez_adversario = True
            
            
            if fez_bola_branca:
                information['penalizado'] = True
            elif not fez_adversario:
                information['joga_novamente'] = True

            
            information['bolas_jogador'] = bolas_jogador
            information['bolas_adversario'] = bolas_adversario
            return information
        else: 
            bolas_jogador = self.numero_bolas[idx_player]
            bolas_adversario = self.numero_bolas[1-idx_player]
            
            information['bolas_jogador'] = bolas_jogador
            information['bolas_adversario'] = bolas_adversario
            
            
            # verifica a primeira colisao
            colisao_ok = False
            if len(information['colisoes']) > 0:
                
                # TODO: verificar se bateu na bola 1
                
                first_colision = information['colisoes'][0]
                fisrt_colision_numero = first_colision[0].numero if first_colision[0].numero != 0 else first_colision[1].numero

                bolas_jogador_mesa  = [b for b in self.table.bolas if b.numero in bolas_jogador]
                if fisrt_colision_numero in bolas_jogador:
                    colisao_ok = True
                    
                if len(bolas_jogador_mesa) ==0:
                    if fisrt_colision_numero != 1:
                        information['penalizado'] = True
    
            
            if (not colisao_ok) or (fez_bola_branca):
                information['penalizado'] = True
            else:

                for bola in bolas_caidas_sem_branca:
                    if bola.numero in bolas_adversario:
                        information['penalizado'] = True
                    if bola.numero in bolas_jogador:
                        information['joga_novamente'] = True
                        
    
                if information['joga_novamente'] and information['penalizado']:
                    information['joga_novamente'] = False
                else:
                    # TODO: verifica se precisa adicionar a bola 1 na lista do jogador
                    pass
                
                
                
                
                
                
                
                
                
                
                
                
                
            # Algum jogador já fez pelo menos uma bola
            print("AS BOLAS ESTAO DEFINIDAS PARA CADA JOGADOR")
        
        
            # se a primeira colisao foi na bola dele
                # repete a jogada
            
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
            
            
            return information
    
        return information

        
        
          
    def run_game(self):
        
        while True:
            print("Iniciando jogada", self.jogador_atual)
            
            while not self.iniciou_jogada:
                    self.table.draw() 
                    
            information = self.table.step(angulo=self.iniciou_jogada_angulo,
                                    intensidade=self.inicou_jogada_intensidade)
            information['final'] = False
            information = self.rules(information, self.jogador_atual)
            
            
            print(information)
            
            
            #################################################################
            ########### Executa as regras do jogo ############################
            if information['perdeu']:
                break
            elif information['ganhou']:
                break
            elif information['penalizado']:
                # derruba uma bola do adversario
                bolas_mesa_adversario = [b for b in self.table.bolas if b.numero in self.numero_bolas[1-self.jogador_atual]]
                # remove a bola da mesa
                if len(bolas_mesa_adversario) > 0:
                    self.table.bolas.remove(bolas_mesa_adversario[0])
                else:
                    print("Nao tem mais bolas do adversario na mesa")
                    print("perdeu")
                    information['perdeu'] = True
            
                information['joaga_novamente'] = False
            
            
            # verifica se o jogador derrubou todas as bolas e nao tem a bola 1
            bola_1_na_mesa = 1 in [bola.numero for bola in self.table.bolas]
            bola_mesa_jogador = [b for b in self.table.bolas if b.numero in self.numero_bolas[self.jogador_atual]]
            
            if not bola_1_na_mesa:
                if len(bola_mesa_jogador) == 0:
                    information['ganhou'] = True
                else:
                    information['perdeu'] = True
                    
                break
            
            if not information['joga_novamente']:
                self.jogador_atual = not self.jogador_atual

            print("terminou a jogada")
            self.iniciou_jogada = False
            
        
        # episodio_final
        information['final']= True
        print("Fim de jogo")
        self.iniciou_jogada = True
        if information['ganhou']:
            print("Jogador", self.jogador_atual, "Ganhou")
        elif information['perdeu']:
            print("Jogador", self.jogador_atual, "Perdeu")

            




def main():
    initial_screen = InitialScreen()
    start_game = initial_screen.run()

    # Se o botão "Jogar" for clicado, inicia o jogo
    if start_game:
        game = GAME()
        game.run_game()
    
    
    
if __name__ == "__main__":
    '''
    Ponto de entrada do programa.
    
    Se o script for executado diretamente, a função main() será chamada,
    iniciando o jogo de sinuca.
    '''
    main()
