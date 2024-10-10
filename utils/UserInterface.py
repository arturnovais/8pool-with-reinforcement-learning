from utils.Game import Game

class UserInterface:
    '''
    Classe que gerencia a interação com o usuário no jogo de sinuca, exibindo informações e capturando entradas.
    
    Args:
        jogo (Game): A instância do jogo que a interface controlará.
    '''
    
    def __init__(self, jogo: Game):
        '''
        Inicializa a interface do usuário para o jogo de sinuca.
        '''
        self.jogo = jogo

    def exibir_placar(self):
        '''
        Exibe o placar atual chamando o método do placar dentro do jogo.
        '''
        self.jogo.scoreboard.exibir_placar()

    def exibir_jogador_atual(self):
        '''
        Exibe o jogador atual que está na vez de jogar.
        '''
        jogador_atual = self.jogo.scoreboard.obter_jogador_atual()
        print(f"Jogador atual: {jogador_atual.nome}")

    def capturar_tacada(self) -> tuple:
        '''
        Captura a intensidade e o ângulo da tacada do jogador atual, solicitando entradas do usuário.
        
        Returns:
            tuple: Um par (intensidade, angulo) que representa a tacada.
        '''
        jogador_atual = self.jogo.scoreboard.obter_jogador_atual()

        try:
            intensidade = float(input(f"{jogador_atual.nome}, escolha a intensidade da tacada (0 a 1): "))
            angulo = float(input(f"{jogador_atual.nome}, escolha o ângulo da tacada (em radianos): "))
            return intensidade, angulo
        except ValueError:
            print("Entrada inválida. Tente novamente.")
            return self.capturar_tacada()

    def exibir_estado_jogo(self):
        '''
        Exibe o estado atual do jogo, incluindo o jogador da vez e o placar.
        '''
        self.exibir_jogador_atual()
        self.exibir_placar()

    def exibir_fim_de_jogo(self):
        '''
        Exibe o placar final e declara o vencedor ao fim do jogo.
        '''
        print("Fim de jogo!")
        self.exibir_placar()

        vencedor = max(self.jogo.scoreboard.jogadores, key=lambda jogador: jogador.pontuacao)
        print(f"O vencedor é {vencedor.nome}!")

    def iniciar_jogo(self):
        '''
        Inicia o loop do jogo e interage com o usuário até que o jogo termine.
        '''
        while self.jogo.rodando:
            self.exibir_estado_jogo()
            intensidade, angulo = self.capturar_tacada()
            self.jogo.jogar_rodada(intensidade, angulo)

        self.exibir_fim_de_jogo()
