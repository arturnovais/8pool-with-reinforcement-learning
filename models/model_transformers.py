import torch
import torch.nn as nn
from dataclasses import dataclass


@dataclass
class Model_args:
    embed_dim : int = 128
    num_heads : int = 8         
    ff_dim : int = embed_dim * 2
    num_layers : int =  2       
    dropout : float = 0.1         
    mlp_dim : int = 128

class transformers_input(nn.Module):
    
    def __init__(self, model_args : Model_args):
        super(transformers_input, self).__init__()
        
        # Layer de embedding (entra uma bola com (x,y,z, w) e sai um vetor de 128 dimensões que representa a bola)
        self.embedding       = nn.Linear(4, model_args.embed_dim)
        self.embedding_white = nn.Linear(2, model_args.embed_dim)
        # TODO: self.embedding_white = nn.Linear(2, model_args.embed_dim)
        
        # Encoder layers
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer( d_model=model_args.embed_dim, 
                                       nhead=model_args.num_heads, 
                                       dim_feedforward=model_args.ff_dim, 
                                       dropout=model_args.dropout) for _ in range(model_args.num_layers)
        ])
        
        self.layer_norm = nn.LayerNorm(model_args.embed_dim)
        
        
        self.apply(self._init_weights)
        
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.constant_(module.bias, 0)
        
    def forward(self, x, bola_branca): 

        b = bola_branca.shape[0]

        bola_branca = self.embedding_white(bola_branca)
        x = self.embedding(x)
        
        bola_branca = bola_branca.unsqueeze(1)
        x = torch.cat((bola_branca, x), dim=1)
        
        x = self.layer_norm(x)  # Normalização antes do Transformer
        for layer in self.encoder_layers:
            x = layer(x)
            
        x = self.layer_norm(x)  # Normalização final
        
        # bola branca é nosso Value, que ira representar o estado do jogo
        return  x.mean(dim=1)




class mlp_input(nn.Module):
    
    def __init__(self, model_args : Model_args):
        super(mlp_input, self).__init__()
        
        # Layer de embedding (entra uma bola com (x,y,z, w) e sai um vetor de 128 dimensões que representa a bola)
        
        self.mlp = nn.Sequential( 
                nn.Linear(4*16, model_args.embed_dim),
                nn.ReLU(),
                nn.Linear(model_args.embed_dim, model_args.mlp_dim),
                nn.ReLU(),
                nn.Linear(model_args.mlp_dim, model_args.embed_dim) # Vamos sair com (sen, cos, intensidade)
        )
        
    def forward(self, x, bola_branca): 

        b = bola_branca.shape[0]
        
        t_concat = torch.zeros(b,2, device=bola_branca.device)
        t_concat[:,0] = 1
        t_concat[:,1] = -1
        
        bola_branca = torch.concat( (bola_branca , t_concat), dim=-1).unsqueeze(1)
        x = torch.concat((bola_branca,x),dim=1)
        
        # [b, 16, 4]
        x = x.view(b,-1)
        
        x = self.mlp(x)
        
        return  x

class TransformersAtor(nn.Module):
    def __init__(self, encoder, model_args : Model_args):
        super(TransformersAtor, self).__init__()
        
        self.econder = encoder
        
        self.mlp = nn.Sequential( 
                nn.Linear(model_args.embed_dim, model_args.mlp_dim),
                nn.ReLU(),
                nn.Linear(model_args.mlp_dim, 2) # Vamos sair com (sen, cos, intensidade)
        )
        
        self.head_intensity = nn.Sigmoid() # Sigmoid para garantir que a intensidade fique entre 0 e 1
        
        #self.linear = nn.Linear(model_args.embed_dim, 1)
        
        
    def forward(self, x, bola_branca): 
        
        x = self.econder(x,bola_branca)
        
        x = self.mlp(x)
        
        
        position = x[:,:1]
        
        intensity = self.head_intensity(x[:,1:])

        position = torch.tanh(position) * torch.pi
        #position = self.linear(position)
        #position = torch.clamp(position, -torch.pi, torch.pi)

        #position = 1.2*torch.pi*torch.cos( position * torch.pi)
        
        return torch.concat((position,intensity),dim=-1)


class TransformerValueModel(nn.Module):
    def __init__(self,encoder, model_args : Model_args):
        super(TransformerValueModel, self).__init__()
        
        self.encoder = encoder
        
        self.value_head = nn.Sequential(
            nn.Linear(model_args.embed_dim, model_args.ff_dim),  # Projeta para dimensão intermediária
            nn.ReLU(),                    # Ativação não-linear
            nn.Linear(model_args.ff_dim, 1)          # Saída escalar (valor do estado)
        )

    def forward(self, x, bola_branca):
        
        x = self.encoder(x,bola_branca)
        value = self.value_head(x)
        
        return value 