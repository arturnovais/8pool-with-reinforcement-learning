from utils.Ball import Ball
from utils.Player import Player

class Scoreboard:
    def __init__(self, jogadores: list):
        """
        Inicializa o placar do jogo de sinuca.

        Args:
            jogadores (list): Uma lista de instâncias da classe Player.
        """
        self.jogadores = jogadores  # Lista de jogadores (instâncias de Player)
        self.bolas_encaçapadas = []  # Lista de bolas encaçapadas
        self.jogador_atual = 0  # Índice do jogador atual

    def adicionar_pontos(self, jogador: Player, pontos: int):
        """
        Adiciona pontos ao jogador.

        Args:
            jogador (Player): O jogador que recebe os pontos.
            pontos (int): O número de pontos a ser adicionado.
        """
        jogador.adicionar_pontos(pontos)

    def registrar_bola_encaçapada(self, bola: Ball):
        """
        Registra uma bola que foi encaçapada.

        Args:
            bola (Ball): A bola que foi encaçapada.
        """
        self.bolas_encaçapadas.append(bola.numero)

    def mudar_jogador(self):
        """
        Alterna para o próximo jogador.
        """
        self.jogador_atual = (self.jogador_atual + 1) % len(self.jogadores)

    def obter_jogador_atual(self) -> Player:
        """
        Retorna o jogador atual.

        Returns:
            Player: A instância do jogador atual.
        """
        return self.jogadores[self.jogador_atual]

    def exibir_placar(self):
        """
        Exibe o placar atual com os nomes dos jogadores e suas pontuações.
        """
        print("Placar Atual:")
        for jogador in self.jogadores:
            jogador.exibir_pontuacao()

    def verificar_fim_de_jogo(self) -> bool:
        """
        Verifica se todas as bolas foram encaçapadas e o jogo acabou.

        Returns:
            bool: True se o jogo terminou, False caso contrário.
        """
        # Supondo que temos 15 bolas de sinuca (excluindo a bola branca)
        return len(self.bolas_encaçapadas) == 15
