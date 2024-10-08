class Player:
    def __init__(self, nome: str):
        """
        Inicializa um jogador de sinuca.

        Args:
            nome (str): O nome do jogador.
        """
        self.nome = nome  # Nome do jogador
        self.pontuacao = 0  # Pontuação inicial do jogador

    def escolher_tacada(self) -> tuple:
        """
        Permite que o jogador escolha a intensidade e o ângulo da tacada.

        Returns:
            tuple: Um par (intensidade, angulo) que representa a tacada.
        """
        try:
            intensidade = float(input(f"{self.nome}, escolha a intensidade da tacada (0 a 1): "))
            angulo = float(input(f"{self.nome}, escolha o ângulo da tacada (em radianos): "))
            return intensidade, angulo
        except ValueError:
            print("Entrada inválida. Tente novamente.")
            return self.escolher_tacada()

    def adicionar_pontos(self, pontos: int):
        """
        Adiciona pontos à pontuação do jogador.

        Args:
            pontos (int): Número de pontos a serem adicionados.
        """
        self.pontuacao += pontos

    def exibir_pontuacao(self):
        """
        Exibe a pontuação atual do jogador.
        """
        print(f"{self.nome} tem {self.pontuacao} pontos.")
