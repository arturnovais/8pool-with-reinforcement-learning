class Player:
    '''
    Classe que representa um jogador de sinuca, contendo o nome e a pontuação do jogador.
    
    Args:
        nome (str): O nome do jogador.
    '''
    
    def __init__(self, nome: str):
        '''
        Inicializa um jogador de sinuca com um nome e pontuação inicial de zero.
        '''
        self.nome = nome
        self.pontuacao = 0

    def escolher_tacada(self) -> tuple:
        '''
        Permite que o jogador escolha a intensidade e o ângulo da tacada via entrada de usuário.
        
        Returns:
            tuple: Um par (intensidade, angulo) que representa a tacada escolhida.
        '''
        try:
            intensidade = float(input(f"{self.nome}, escolha a intensidade da tacada (0 a 1): "))
            angulo = float(input(f"{self.nome}, escolha o ângulo da tacada (em radianos): "))
            return intensidade, angulo
        except ValueError:
            print("Entrada inválida. Tente novamente.")
            return self.escolher_tacada()

    def adicionar_pontos(self, pontos: int):
        '''
        Adiciona pontos à pontuação atual do jogador.
        
        Args:
            pontos (int): O número de pontos a ser adicionado à pontuação do jogador.
        '''
        self.pontuacao += pontos

    def exibir_pontuacao(self):
        '''
        Exibe a pontuação atual do jogador no console.
        '''
        print(f"{self.nome} tem {self.pontuacao} pontos.")
