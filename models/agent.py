import torch
from torch import nn
from models.model_transformers import Model_args, TransformerValueModel, TransformersAtor
from torch.distributions import Normal

class Agent(nn.Module):
    def __init__(self, action_dim, model_args):
        super().__init__()
        self.critic = TransformerValueModel(model_args)  # Modelo para estimar o valor
        self.actor_mean = TransformersAtor(model_args)  # Modelo para estimar a média das ações
        self.actor_log_std = nn.Parameter(torch.zeros(action_dim))  # Desvio padrão fixo

    def get_value(self, state, bola_branca):
        """Obtém o valor estimado pelo modelo crítico."""
        return self.critic(state, bola_branca)

    def get_action_and_value(self, state, bola_branca, action=None):
        """
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
        """
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

        return action, log_prob, entropy, value