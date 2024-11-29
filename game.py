
from utils.Table import Table
from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.button import button
import utils.config as cfg
from utils.Scoreboard import Scoreboard

from interface.initial_screen import InitialScreen
from interface.end_screen import EndScreen 
import torch

class GAME:
    
    
    def __init__(self, players_names=['Player 1', 'Player 2'], background='imgs/Background/inf1.jpg', draw=True):
        
        self.Scoreboard = Scoreboard(players_names,game=self)
        self.table = Table(cfg.display_table_width, cfg.display_table_height, 
                  ambiente_fisico= PhysicsEnvironment(),
                  display_width = cfg.display_width, 
                  display_height = cfg.display_height,
                  draw_game=draw,
                  scoreboard=self.Scoreboard,
                  background=background,
                  game = self)

        # comando para controlar o jogo.... o TACO INTERFERE NESSAS VARIAVEIS
        self.iniciou_jogada = False
        self.jogador_atual = 0
        self.iniciou_jogada_angulo = 0
        self.inicou_jogada_intensidade = 0
        self.numero_bolas = [[],[]] # numero das bolas que cada jogador deve derrubar
        
    def reset(self):
        self.table.reset()
        self.iniciou_jogada = False
        self.jogador_atual = 0
        self.iniciou_jogada_angulo = 0
        self.inicou_jogada_intensidade = 0
        self.numero_bolas = [[],[]] # numero das bolas que cada jogador deve derrubar     
        
        return self.get_observations()
        
    def rules(self, information, idx_player):
        # Função que verifica as regras do jogo
        
        bolas_caidas_sem_branca = [b for b in information['bolas_caidas'] if b.numero != 0]
        fez_bola_branca = 0 in [b.numero for b in information['bolas_caidas']]
        
        # Inicializando estado do jogo
        information['perdeu'] = False
        information['ganhou'] = False
        information['penalizado'] = False
        information['joga_novamente'] = False

        # Caso inicial: nenhuma bola foi derrubada
        if len(self.table.bolas) == 16:
            # Ninguém fez nenhuma bola ainda
            return information

        # Caso: Primeira bola derrubada
        elif len(self.table.bolas) + len(bolas_caidas_sem_branca) == 16:
            """
            Jogador fez a primeira bola da partida
            """
            first_ball = bolas_caidas_sem_branca[0]  # Identifica a primeira bola derrubada

            bolas_jogador = [2, 4, 6, 8, 10, 12, 14]
            bolas_adversario = [3, 5, 7, 9, 11, 13, 15]

            if first_ball.numero % 2 != 0:  # Caso a primeira bola seja ímpar
                bolas_jogador, bolas_adversario = bolas_adversario, bolas_jogador

            # Define as bolas de cada jogador
            if idx_player == 0:
                self.numero_bolas = [bolas_jogador, bolas_adversario]
            else:
                self.numero_bolas = [bolas_adversario, bolas_jogador]

            # Verifica vitória ou derrota na primeira jogada
            if 1 in [b.numero for b in bolas_caidas_sem_branca]:
                if all(b.numero in bolas_jogador for b in bolas_caidas_sem_branca):
                    information['ganhou'] = True
                    return information
                else:
                    information['perdeu'] = True
                    return information

            # Determina se o jogador joga novamente ou passa a vez
            fez_adversario = any(b.numero in bolas_adversario for b in bolas_caidas_sem_branca)
            if fez_bola_branca:
                information['penalizado'] = True
            elif not fez_adversario:
                information['joga_novamente'] = True

            information['bolas_jogador'] = bolas_jogador
            information['bolas_adversario'] = bolas_adversario
            return information

        # Caso: Jogada normal após a primeira bola ser derrubada
        else:
            bolas_jogador = self.numero_bolas[idx_player]
            bolas_adversario = self.numero_bolas[1 - idx_player]

            information['bolas_jogador'] = bolas_jogador
            information['bolas_adversario'] = bolas_adversario

            # Verifica a primeira colisão
            colisao_ok = False
            if len(information['colisoes']) > 0:
                first_collision = information['colisoes'][0]
                first_collision_numero = (
                    first_collision[0].numero
                    if first_collision[0].numero != 0
                    else first_collision[1].numero
                )

                if first_collision_numero in bolas_jogador:
                    colisao_ok = True

            # Penalidades e regras adicionais
            if not colisao_ok or fez_bola_branca:
                information['penalizado'] = True
            else:
                for bola in bolas_caidas_sem_branca:
                    if bola.numero in bolas_adversario:
                        information['penalizado'] = True
                    if bola.numero in bolas_jogador:
                        information['joga_novamente'] = True

                if information['joga_novamente'] and information['penalizado']:
                    information['joga_novamente'] = False

            return information


        
        
          
     # Importar a nova tela

    
    
    def make_step(self, information):
            information = self.rules(information, self.jogador_atual)
            information['winner'] = None
            
            
            #################################################################
            ########### Executa as regras do jogo ############################
            if information['perdeu']:
                information['winner'] = self.Scoreboard.jogadores[1 - self.jogador_atual]
                return information
            
            elif information['ganhou']:
                information['winner'] = self.Scoreboard.jogadores[self.jogador_atual]
                return information
            
            elif information['penalizado']:
                # Derruba uma bola do adversário
                bolas_mesa_adversario = [b for b in self.table.bolas if b.numero in self.numero_bolas[1 - self.jogador_atual]]
                # Remove a bola da mesa
                if len(bolas_mesa_adversario) > 0:
                    self.table.bolas.remove(bolas_mesa_adversario[0])
                else:
                    print("Nao tem mais bolas do adversario na mesa")
                    print("perdeu")
                    information['perdeu'] = True
                    information['winner'] = self.Scoreboard.jogadores[1 - self.jogador_atual]
                    return information
                
                information['joga_novamente'] = False

            # Verifica se o jogador derrubou todas as bolas e nao tem a bola 1
            bola_1_na_mesa = 1 in [bola.numero for bola in self.table.bolas]
            bola_mesa_jogador = [b for b in self.table.bolas if b.numero in self.numero_bolas[self.jogador_atual]]

            if not bola_1_na_mesa:
                if len(bola_mesa_jogador) == 0:
                    information['ganhou'] = True
                    information['winner'] = self.Scoreboard.jogadores[self.jogador_atual]
                else:
                    information['perdeu'] = True
                    information['winner'] = self.Scoreboard.jogadores[1 - self.jogador_atual]

                return information

            if not information['joga_novamente']:
                self.jogador_atual = not self.jogador_atual

            return information



    def run_game(self):
        while True:
            print("Iniciando jogada", self.jogador_atual)

            while not self.iniciou_jogada:
                self.table.draw()

            information = self.step((self.iniciou_jogada_angulo, self.inicou_jogada_intensidade))[1]
            
            self.iniciou_jogada = False
                
            if information.get('winner',None) is not None:
                print('Fim de jogo - ', information['winner'])
                break
            
        print("Fim de jogo")
        self.iniciou_jogada = True

        # Chamar a tela final
        if cfg.end_screen: 
            end_screen = EndScreen(information['winner'])
            result = end_screen.run()
            if result == "menu":
                return  # Volta ao menu principal


    def get_observations(self):
        #
        
        
        bolas_jogador = [b for b in self.numero_bolas[self.jogador_atual]]
        bolas_jogador_mesa = [b.numero for b in self.table.bolas if b.numero in bolas_jogador]
        
        # {len(bolas_jogador_mesa)}/{len(bolas_jogador)}
                
        
        bolas_jogador_atual = self.numero_bolas[self.jogador_atual]
        bolas_mesa = len([bola for bola in self.table.bolas if bola.numero != 0])
        
        # cria um vetor de 16 posicao
        state = torch.zeros(15,4, device=cfg.device)
        
        bola_branca_position = None
        
        index = 0
        for bola in self.table.bolas:
            position_bola = bola.get_position()
            
            if bola.numero == 0:
                bola_branca_position = torch.tensor([position_bola[0], position_bola[1]], device=cfg.device)
            elif bola.numero == 1:
                bola_do_jogador=False
                if (len(bolas_jogador) != 0) and (len(bolas_jogador_mesa) == 0 ): # quando o jogador ja tiver as bolas associadas e quando fizer todas
                    bola_do_jogador = True 
                    
                state[index] = torch.tensor([position_bola[0], 
                                             position_bola[1], 
                                             1, # bola existe
                                             bola_do_jogador],
                                             device=cfg.device)
            else:
                bola_jogador = bola.numero in bolas_jogador_atual
                state[index] = torch.tensor([position_bola[0], 
                                             position_bola[1], 
                                             1, # bola existe
                                             bola_jogador
                                            ])
            index += 1                                 
        return state, bola_branca_position
        
    def single_observation_space():
        return 15*4 + 2
    # cada bola, possui x,y, se existe, se é do jogador
    
    def step(self, actions, rewards_function=None):
        angulo, forca = actions
        informations  = self.table.step(angulo, forca)
        informations = self.make_step(informations)
        
        terminations = informations.get('perdeu', False) or informations.get('ganhou', False) or informations.get('winner', None) is not None
        
        rewards = None
        if rewards_function is not None:
            rewards = rewards_function(informations)
            
        
        return self.get_observations(), informations , terminations, rewards
        
        



def main():
    while True:
        if cfg.initial_screen:
            initial_screen = InitialScreen()
            player_names, background = initial_screen.run()[0], initial_screen.run()[1]
            print('PLAYERS:', player_names)
            game = GAME(players_names=player_names, background=background)
            game.run_game()
        else:
            game = GAME()
            game.run_game()

    
    
    
if __name__ == "__main__":
    '''
    Ponto de entrada do programa.
    
    Se o script for executado diretamente, a função main() será chamada,
    iniciando o jogo de sinuca.
    '''
    main()
