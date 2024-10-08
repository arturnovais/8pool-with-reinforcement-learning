from Ball import Ball

class Scoreboard:
    def __init__(self, jogadores: list):
        """
        Inicializa o placar do jogo de sinuca.

        Args:
            jogadores (list): Uma lista com os nomes dos jogadores.
        """
        self.jogadores = jogadores  # Lista de jogadores
        self.pontuacao = {jogador: 0 for jogador in jogadores}  # Dicionário com a pontuação de cada jogador
        self.bolas_encaçapadas = []  # Lista de bolas encaçapadas
        self.jogador_atual = 0  # Índice do jogador atual

    def adicionar_pontos(self, jogador: str, pontos: int):
        """
        Adiciona pontos ao jogador.

        Args:
            jogador (str): O nome do jogador que recebe os pontos.
            pontos (int): O número de pontos a ser adicionado.
        """
        if jogador in self.pontuacao:
            self.pontuacao[jogador] += pontos
        else:
            print(f"Jogador {jogador} não encontrado no placar.")

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

    def obter_jogador_atual(self) -> str:
        """
        Retorna o nome do jogador atual.

        Returns:
            str: O nome do jogador atual.
        """
        return self.jogadores[self.jogador_atual]

    def exibir_placar(self):
        """
        Exibe o placar atual com os nomes dos jogadores e suas pontuações.
        """
        print("Placar Atual:")
        for jogador, pontos in self.pontuacao.items():
            print(f"{jogador}: {pontos} pontos")

    def verificar_fim_de_jogo(self) -> bool:
        """
        Verifica se todas as bolas foram encaçapadas e o jogo acabou.

        Returns:
            bool: True se o jogo terminou, False caso contrário.
        """
        # Supondo que temos 15 bolas de sinuca (excluindo a bola branca)
        return len(self.bolas_encaçapadas) == 15
