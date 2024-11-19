from utils.Scoreboard import Scoreboard
from utils.Table import Table
from utils.Cue import Cue
from utils.CollisionDetector import CollisionDetector
from utils.Player import Player

class Game:
    '''
    Classe que representa o jogo de sinuca, gerenciando a interação entre os jogadores, mesa, bolas e taco.
    
    Args:
        jogadores (list): Lista de instâncias da classe Player que representam os jogadores.
        mesa (Table): Instância da classe Table, representando a mesa de sinuca.
        bolas (list): Lista de instâncias da classe Ball que representam as bolas no jogo.
        taco (Cue): Instância da classe Cue, que representa o taco usado pelos jogadores.
    '''
    
    def __init__(self, jogadores: list, mesa: Table, bolas: list, taco: Cue):
        '''
        Inicializa o jogo de sinuca com os jogadores, mesa, bolas e taco.
        
        A classe também inicializa o placar (scoreboard) e define o estado inicial do jogo como "rodando".
        '''
        self.mesa = mesa
        self.bolas = bolas
        self.taco = taco
        self.scoreboard = Scoreboard(jogadores)
        self.rodando = True

    def jogar_rodada(self, intensidade: float, angulo: float):
        '''
        Executa uma rodada do jogo, onde o jogador atual realiza uma tacada.
        
        Args:
            intensidade (float): A intensidade da tacada, variando de 0 a 1.
            angulo (float): O ângulo da tacada em radianos.
        '''
        jogador_atual = self.scoreboard.obter_jogador_atual()
        bola_branca = self.bolas[0]
        
        self.taco.aplicar_tacada(bola_branca, intensidade, angulo)
        self.atualizar_estado_jogo(jogador_atual)

    def atualizar_estado_jogo(self, jogador_atual: Player):
        '''
        Atualiza o estado do jogo, verificando colisões entre bolas, bolas encaçapadas, e alternância de turnos.
        
        Args:
            jogador_atual (Player): O jogador atual que realizou a jogada.
        '''
        collision_detector = CollisionDetector()

        for bola in self.bolas:
            if not self.mesa.detectar_buraco(bola):
                self.mesa.atualizar_estado_bola(bola, dt=0.1)

                for outra_bola in self.bolas:
                    if bola != outra_bola and collision_detector.detectar_colisao_bolas(bola, outra_bola):
                        collision_detector.resolver_colisao_bolas(bola, outra_bola)

                collision_detector.detectar_colisao_borda(bola, self.mesa.x_start, self.mesa.y_start, self.mesa.largura, self.mesa.altura)
            else:
                self.scoreboard.registrar_bola_encaçapada(bola)
                self.scoreboard.adicionar_pontos(jogador_atual, 10)

        if self.scoreboard.verificar_fim_de_jogo():
            self.rodando = False
        else:
            self.scoreboard.mudar_jogador()
