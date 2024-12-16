import torch
from torch import nn
from models.model_transformers import Model_args, TransformerValueModel, TransformersAtor , transformers_input, mlp_input
from torch.distributions import Normal, Categorical
import utils.config as cfg
import math


class Agent(nn.Module):
    def __init__(self, action_dim, model_args):
        super().__init__()
        
        if action_dim is None:
            action_dim = 2
            
        #self.encoder = transformers_input(model_args)
        self.encoder = transformers_input(model_args)
        
        self.critic = TransformerValueModel(self.encoder,model_args)  # Modelo para estimar o valor
        self.actor_mean = TransformersAtor(self.encoder,model_args)  # Modelo para estimar a média das ações
        self.actor_log_std = nn.Parameter(torch.zeros(action_dim))  # Desvio padrão fixo

    def get_value(self, state, bola_branca):
        """Obtém o valor estimado pelo modelo crítico."""
        return self.critic(state, bola_branca)
    
    
    def get_action_and_value(self, state, bola_branca, action=None):
        action_probs, intensity, noise = self.actor_mean(state, bola_branca)
        angulos_batch, mask_batch = get_actions(state, bola_branca)

        # Máscara e distribuição categórica
        masked_action_probs = action_probs.masked_fill(mask_batch == 0, float('-inf'))
        masked_action_probs = torch.softmax(masked_action_probs, dim=-1)
        dist_categorical = Categorical(masked_action_probs)

        if action is None:
            action_index = dist_categorical.sample()
        else:
            action_index = action[..., 0].long()  # ação discreta extraída da entrada

        log_prob_discrete = dist_categorical.log_prob(action_index)
        entropy_discrete = dist_categorical.entropy()

        selected_angle = angulos_batch.gather(1, action_index.unsqueeze(-1)).squeeze(-1)
        angle_with_noise = selected_angle + noise

        # Distribuição contínua
        mean_continuous = torch.cat((intensity.unsqueeze(-1), noise.unsqueeze(-1)), dim=-1)
        log_std_continuous = self.actor_log_std.expand_as(mean_continuous)
        std_continuous = torch.exp(log_std_continuous)
        dist_continuous = Normal(mean_continuous, std_continuous)

        if action is None:
            action_continuous = dist_continuous.sample()
            # Ação final mantendo a estrutura: primeiro índice discreto, depois contínuos
            action = torch.cat((
                action_index.unsqueeze(-1).float(),
                angle_with_noise.unsqueeze(-1),
                intensity.unsqueeze(-1)
            ), dim=-1)
        else:
            action_continuous = action[..., 1:]

        log_prob_continuous = dist_continuous.log_prob(action_continuous).sum(axis=-1)
        entropy_continuous = dist_continuous.entropy().sum(axis=-1)

        log_prob = log_prob_discrete + log_prob_continuous
        entropy = entropy_discrete + entropy_continuous

        value = self.critic(state, bola_branca)

        # Não sobrescrever o action aqui, apenas retornar
        return action, log_prob, entropy, value










def get_actions(state, state_bola_branca):
    """
    Processa um batch de estados e bolas brancas para calcular os ângulos,
    preenchendo com valores sentinela para garantir tamanho fixo de 63.

    Args:
        state: Tensor de estados, onde cada estado contém informações de uma bola.
        state_bola_branca: Tensor com as posições da bola branca para cada estado.

    Returns:
        angulos_batch: Tensor com ângulos calculados para cada estado, tamanho [batch_size, 63].
        mask_batch: Máscara indicando ângulos válidos (1) ou preenchidos (0), tamanho [batch_size, 63].
    """
    batch_size = state.size(0)  # Tamanho do batch
    max_angles = 7 * 9  # Máximo de ângulos permitidos
    angulos_batch = []
    mask_batch = []

    for i in range(batch_size):
        indices = (state[i, :, -1] == 1).nonzero(as_tuple=True)[0]  # Índices de bolas válidas no estado
        if indices.shape[0] == 0: 
            indices = torch.tensor([1, 2, 3, 4, 5, 6, 7], device=state.device)

        angulos = []
        for indice in indices:
            for p in range(9):
                angulos.append(
                    list(
                        draw_mirrored_pool_tables(
                            state_bola_branca[i].cpu().numpy().tolist(), 
                            state[i, indice, :2].cpu().numpy().tolist()
                        )
                    )[p]
                )

        # Garantir que temos exatamente 63 ângulos
        valid_len = len(angulos)
        if valid_len < max_angles:
            angulos += [float('nan')] * (max_angles - valid_len)  # Preencher com nan

        angulos_batch.append(angulos[:max_angles])  # Cortar caso exceda 63
        mask_batch.append([1] * valid_len + [0] * (max_angles - valid_len))  # Máscara de ângulos válidos

    angulos_batch = torch.tensor(angulos_batch, device=state.device)
    mask_batch = torch.tensor(mask_batch, device=state.device)

    return angulos_batch, mask_batch




def calcula_angulo(bola_branca, bola_numero):

        x, y = bola_branca
        x1, y1 = bola_numero 

        x *= cfg.display_table_width
        x1 *= cfg.display_table_width
        y *= cfg.display_table_height
        y1 *= cfg.display_table_height   


        return math.atan2(y1 - y, x1 - x)


def draw_mirrored_pool_tables(bola_branca, bola_numero):
    """
    Draws 9 mirrored pool tables based on the given dimensions and ball positions.

    Args:
        l: Width of the table.
        A: Height of the table.
        balls: List of ball positions as tuples (x, y).
    """
    l=cfg.display_table_width 
    A=cfg.display_table_height
    posicoes = [ 
                    (bola_numero[0], bola_numero[1]),
                    (-bola_numero[0], bola_numero[1]),
                    ( l+(l-bola_numero[0]), bola_numero[1]),#
                    (bola_numero[0], -bola_numero[1]),
                    (bola_numero[0], A+(A-bola_numero[1])),#
                    (-bola_numero[0], A+(A-bola_numero[1])),#
                    (-bola_numero[0], -bola_numero[1]),
                    ( l+(l-bola_numero[0]), A+(A-bola_numero[1])),
                    ( l+(l-bola_numero[0]), -bola_numero[1]),#
                ]
    
    l,A = 1 , 1
    posicoes = [ 
                    (bola_numero[0], bola_numero[1]),
                    (-bola_numero[0], bola_numero[1]),
                    ( l+(l-bola_numero[0]), bola_numero[1]),#
                    (bola_numero[0], -bola_numero[1]),
                    (bola_numero[0], A+(A-bola_numero[1])),#
                    (-bola_numero[0], A+(A-bola_numero[1])),#
                    (-bola_numero[0], -bola_numero[1]),
                    ( l+(l-bola_numero[0]), A+(A-bola_numero[1])),
                    ( l+(l-bola_numero[0]), -bola_numero[1]),#
                ]

    for p in posicoes:
        yield calcula_angulo(bola_branca, p)






        """def get_action_and_value(self, state, bola_branca, action=None):
            "
            Obtém a ação, log_prob, entropia e valor.
            
            Args:
                x: Entrada para o modelo.
                bola_branca: Dados da bola branca.
                action: Ação opcional para avaliar log_prob e entropia.
            
            Returns:
                action: Ação amostrada ou fornecida.
                log_prob: Logaritmo da probabilidade da ação.
                entropy: Entropia da distribuição.
                value: Valor estimado pelo crítico.
            ""
            # O ator retorna ângulo e intensidade
            mean = self.actor_mean(state, bola_branca)  # Predição da média das ações
            
            
            log_std = self.actor_log_std.expand_as(mean)  # Ajusta o desvio padrão ao formato correto
            std = torch.exp(log_std)  # Calcula o desvio padrão

            # Distribuição Normal para ações contínuas
            
            dist = Normal(mean, std)

            if action is None:
                action = dist.sample()  # Amostra uma ação da distribuição
                
            action[..., 0] = torch.clamp(action[..., 0], 0, 360)
            action[..., 1] = torch.clamp(action[..., 1], 0, 1)
        
            log_prob = dist.log_prob(action).sum(axis=-1)  # Log probabilidade
            entropy = dist.entropy().sum(axis=-1)  # Entropia

            value = self.critic(state, bola_branca)  # Valor estimado pelo crítico

            return action, log_prob, entropy, value"""