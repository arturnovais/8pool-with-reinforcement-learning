from utils.Table import Table
from utils.PhysicsEnvironment import PhysicsEnvironment
from utils.Ball import Ball
from utils.Player import Player
from utils.Cue import Cue
from utils.Game import Game
from utils.UserInterface import UserInterface

def main():
    print("Bem-vindo ao jogo de Sinuca!")

    # Criar a mesa com dimensões padrão e o ambiente físico
    mesa = Table(largura=2.84, altura=1.42, ambiente_fisico=PhysicsEnvironment(friccao=0.98, resistencia_ar=0.995))
    
    # Criar as bolas (16 bolas, sendo a bola 0 a bola branca)
    bolas = [Ball(numero=i, raio=0.057, massa=0.17, posicao=(1 + i * 0.1, 0.5)) for i in range(16)]
    
    # Criar o taco com uma força máxima
    taco = Cue(força_maxima=12.0)

    # Criar jogadores
    jogador1 = Player("Jogador 1")
    jogador2 = Player("Jogador 2")

    # Criar o jogo com os dois jogadores
    jogo = Game(jogadores=[jogador1, jogador2], mesa=mesa, bolas=bolas, taco=taco)

    # Criar a interface do usuário para o jogo
    interface = UserInterface(jogo)

    # Iniciar o jogo
    interface.iniciar_jogo()

# Executar o jogo
if __name__ == "__main__":
    main()
