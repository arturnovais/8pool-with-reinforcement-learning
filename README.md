# Projeto Sinuca com Aprendizado por Reforço

Este projeto desenvolve um jogo de sinuca com simulação física realista, onde agentes treinados por aprendizado por reforço podem jogar de forma autônoma. O objetivo final é realizar um campeonato entre agentes representando diferentes algoritmos.

## Sobre o Projeto

O projeto combina simulação física e aprendizado por reforço para criar um ambiente de sinuca interativo. Ele busca replicar o comportamento real das bolas e da mesa, fornecendo um ambiente para treinar e avaliar agentes autônomos.

### Estrutura do Projeto

- **`game/`**  
  Contém o arquivo principal para executar o jogo e interagir com o ambiente.

- **`utils/`**  
  Inclui classes e funções auxiliares, como:
  - `Ball.py`: Define as propriedades das bolas.
  - `CollisionDetector`: Cuida das colisões entre objetos (bolas, bola e quina...)
  - `Table.py`: Representa a mesa de sinuca.
  - `Cue.py`: Representa o taco.
  - `PhysicsEnvironment.py`: Implementa a simulação física, como atrito, resistência do ar, decomposição de vetores para direção em caso de colisão...
  - `Pocket.py`: Representa os buracos da mesa.
  - `Scoreboard.py`: Representa o placar do jogo.
  - `config.py`: Permite configurações personalizadas do jogo.

- **`imgs/`**  
  Contém os arquivos gráficos do jogo, como imagens da mesa e bolas, cada classe com sua subpasta.

- **`interface/`**  
  Inclui arquivos para a tela inicial e a tela de resultados finais.


## Como usar

Este projeto oferece duas formas principais de utilização: jogar o jogo manualmente e usar o ambiente para treinar modelos com aprendizado por reforço.

### Jogar o Jogo Manualmente

Para jogar o jogo diretamente, execute o arquivo principal `game.py`:

```bash
python game.py
```

Isso abrirá o jogo, permitindo interações diretas com o ambiente da mesa de sinuca.


### Treinar Modelos de Aprendizado por Reforço

O ambiente do jogo foi padronizado de forma semelhante ao `gymnasium` para facilitar a integração com algoritmos de aprendizado por reforço. As funções principais disponíveis são:

- **`step(action)`**:  
  Executa uma ação (tacada na bola usando ângulo e força) e retorna:  
  - O estado atual.  
  - A recompensa recebida.  
  - Um indicador se o episódio terminou.  
  - Informações adicionais.

- **`reset()`**:  
  Restaura o ambiente ao estado inicial para iniciar um novo episódio.

- **`get_observations()`**:  
  Retorna as observações do estado atual, como:  
  - Posições das bolas.  
  - Direção e velocidade.
 
  Os retornos serão melhores detalhados no código de exemplo.


## Exemplo de Uso

O código abaixo demonstra como utilizar o ambiente de sinuca com aprendizado por reforço. Ele inclui a configuração inicial, execução de ações e personalização da função de recompensas.

### Clonando o Repositório e Configurando o Ambiente

O primeiro passo é clonar o repositório, mover os arquivos para o diretório atual e instalar as dependências:

```bash
!git clone https://github.com/arturnovais/8pool-with-reinforcement-learning.git ./game
!mv ./game/* ./
!rm -rf ./game

# Execute a primeira parte caso não tenha o projeto

!pip install -r ./requirements.txt
!pip install tqdm
!pip install ipykernel
```

### Inicializando o Ambiente

Para inicializar o ambiente, utilize a classe `GAME`. O parâmetro `draw` define se o jogo será visualizado graficamente:

```python
from game import GAME

env = GAME(draw=False)  # draw=True permite visualizar graficamente, mas não funciona no Colab
observations = env.reset()
```

O método reset() retorna as observações iniciais do ambiente.

Para desenhar a mesa (se draw=True estiver ativado), utilize:

```python
env.table.draw()
```

### Criando uma Função de Recompensas
A função de recompensas é personalizável e define como as ações realizadas pelo agente serão avaliadas. Aqui está um exemplo de função de recompensas:

```python
def rewards_function(information):
    colisoes = information['colisoes']
    bolas_caidas = information['bolas_caidas']
    perdeu = information['perdeu']
    ganhou = information['ganhou']
    joga_novamente = information['joga_novamente']
    bolas_jogador = information.get('bolas_jogador', [])
    bolas_adversario = information.get('bolas_adversario', [])
    winner = information.get('winner', None)
    penalizado = information.get('penalizado', False)

    rewards = 0

    if joga_novamente:
        rewards += 1

    if perdeu:
        rewards -= 1.5

    if ganhou:
        rewards += 1.5

    if penalizado:
        rewards -= 1

    return rewards
```
Essa função utiliza informações do ambiente para calcular as recompensas, como colisões, bolas caídas, se o jogador ganhou ou perdeu, e penalizações (Uma penalização indica que o jogador executou uma ação indevida, como derrubar bola branca, não acertar nenhuma bola em sua jogada...).


### Executando uma Ação
Para realizar uma ação no ambiente, utilize o método step(). Este método aceita dois argumentos principais:

Ação (action): Um tupla contendo o ângulo e a intensidade do taco.
Função de Recompensas (rewards_function): A função que será utilizada para calcular a recompensa.

Exemplo:

```python
angulo = 10
intensidade = 0.9

obs, information, terminations, rewards = env.step((angulo, intensidade),
                                                   rewards_function=rewards_function)
print('state', obs)
print('termination', terminations)
print('rewards', rewards)
```

#### Retornos do step()

**obs**:
Representa o estado atual do ambiente. É uma tupla composta por:

Tensor com (x, y, m, j), sendo:
  - x, y as coordenadas das bolas
  - m se a bola está na mesa ou já foi derrubada
  - j se a bola pertence ou não aquele jogador.


**information**:
Contém informações detalhadas sobre o estado atual, como:

Colisões.
Bolas que caíram.
Se o jogador ganhou ou perdeu.

**terminations**:
Um valor booleano que indica se o jogo terminou.

**rewards**:
A recompensa calculada pela função de recompensas.


### Exemplo de Jogada
O exemplo abaixo mostra como realizar uma jogada completa e atualizar o estado do jogo:

```python
print("Iniciando jogada", env.jogador_atual)

while not env.iniciou_jogada:
    env.table.draw()

obs, information, terminations, rewards = env.step(
    (env.iniciou_jogada_angulo, env.inicou_jogada_intensidade), 
    rewards_function=rewards_function
)
env.iniciou_jogada = False

print("Recompensa da jogada:", rewards)
```

Esse exemplo aguarda o início de uma jogada, executa a ação e imprime a recompensa obtida.





