from utils.Scoreboard import Scoreboard
from utils.Table import Table
from utils.Cue import Cue
from utils.CollisionDetector import CollisionDetector
from utils.Player import Player

class Game:
    def __init__(self, jogadores: list, mesa: Table, bolas: list, taco: Cue):
        """
        Inicializa o jogo de sinuca.

        Args:
            jogadores (list): Uma lista de instâncias da classe Player.
            mesa (Table): A instância da mesa de sinuca.
            bolas (list): Uma lista de instâncias da classe Ball representando as bolas no jogo.
            taco (Cue): A instância do taco de sinuca (Cue).
        """
        self.mesa = mesa  # Mesa onde o jogo acontece
        self.bolas = bolas  # Lista de bolas em jogo
        self.taco = taco  # Taco usado pelos jogadores
        self.scoreboard = Scoreboard(jogadores)  # Placar do jogo
        self.rodando = True  # Estado do jogo

    def jogar_rodada(self, intensidade: float, angulo: float):
        """
        Executa uma rodada do jogo, onde o jogador atual realiza uma tacada.

        Args:
            intensidade (float): A intensidade da tacada, de 0 a 1.
            angulo (float): O ângulo da tacada em radianos.
        """
        jogador_atual = self.scoreboard.obter_jogador_atual()

        # Pegamos a bola branca (geralmente a bola 0)
        bola_branca = self.bolas[0]

        # O jogador atual realiza uma tacada na bola branca
        self.taco.aplicar_tacada(bola_branca, intensidade, angulo)

        # Atualiza o estado do jogo (movimento das bolas, colisões etc.)
        self.atualizar_estado_jogo(jogador_atual)

    def atualizar_estado_jogo(self, jogador_atual: Player):
        """
        Atualiza o estado do jogo, verificando colisões, bolas encaçapadas e alternância de turnos.

        Args:
            jogador_atual (Player): O jogador atual que realizou a jogada.
        """
        collision_detector = CollisionDetector()

        # Atualiza as posições das bolas e verifica colisões
        for bola in self.bolas:
            if not self.mesa.detectar_buraco(bola):  # Verifica se a bola não foi encaçapada
                self.mesa.atualizar_estado_bola(bola, dt=0.1)

                # Verifica colisão com outras bolas
                for outra_bola in self.bolas:
                    if bola != outra_bola and collision_detector.detectar_colisao_bolas(bola, outra_bola):
                        collision_detector.resolver_colisao_bolas(bola, outra_bola)

                # Verifica colisão com as bordas da mesa
                collision_detector.detectar_colisao_borda(bola, self.mesa)
            else:
                self.scoreboard.registrar_bola_encaçapada(bola)
                self.scoreboard.adicionar_pontos(jogador_atual, 10)  # Exemplo de pontuação

        # Verifica se o jogo terminou (todas as bolas encaçapadas)
        if self.scoreboard.verificar_fim_de_jogo():
            self.rodando = False
        else:
            # Alterna o turno para o próximo jogador
            self.scoreboard.mudar_jogador()
