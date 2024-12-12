import torch
import torch.nn as nn
from dataclasses import dataclass


@dataclass
class Args:
    embed_dim : int = 128
    num_heads : int = 8         
    ff_dim : int = embed_dim * 2
    num_layers : int =  2       
    dropout : float = 0.1         
    

class TransformersAtor(nn.Module):
    def __init__(self, args : Args):
        super(TransformersAtor, self).__init__()
        
        # Layer de embedding (entra uma bola com (x,y,z, w) e sai um vetor de 128 dimensões que representa a bola)
        self.embedding = nn.Linear(4, args.embed_dim)
        
        # Encoder layers
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer( d_model=args.embed_dim, 
                                       nhead=args.num_heads, 
                                       dim_feedforward=args.ff_dim, 
                                       dropout=args.dropout) for _ in range(args.num_layers)
        ])
        
        # Layer normalization
        self.layer_norm = nn.LayerNorm(args.embed_dim)
        
        #MlP para gerar regressão de angulo e intensidade
        self.mlp = nn.Sequential( 
                nn.Linear(args.embed_dim, args.ff_dim),
                nn.Tanh(),
                nn.Linear(args.ff_dim, 3) # Vamos sair com (sen, cos, intensidade)
        )
        
        self.head_position = nn.Tanh() # Tanh para garantir que o angulo fique entre -1 e 1
        self.head_intensity = nn.Sigmoid() # Sigmoid para garantir que a intensidade fique entre 0 e 1

    def forward(self, x, bola_branca): 
        # adiciona a dimensão da bolinha branca -> batch, (x,y,1,-1)
        b = bola_branca.shape[0]
        t_concat = torch.zeros(b,2, device=bola_branca.device)
        t_concat[:,0] = 1
        t_concat[:,1] = -1
        bola_branca = torch.concat( (bola_branca , t_concat), dim=-1).unsqueeze(1)
        x = torch.concat((bola_branca,x),dim=1)
        
        x = self.embedding(x)        
        
        for layer in self.encoder_layers:
            x = layer(x)
    
        x = self.layer_norm(x)
        
        # bola branca é nosso Value, que ira representar o estado do jogo
        x = x[:,0,:]        
        x = self.mlp(x)
        
        # transforma o x em angulo e intensidade
        position = self.head_position(x[:,:2])
        intensity = self.head_intensity(x[:,2:])
        
        x_sin = position[:,0:1] # seno
        x_cos = position[:,1:2] # cosseno
        
        angles_deg = torch.rad2deg(torch.atan2(x_sin, x_cos)) # converte para graus
        angles_deg = torch.where(angles_deg < 0, angles_deg + 360, angles_deg)
        
        # concatena o resultado
        return torch.concat((angles_deg,intensity),dim=-1) # Retorna o angulo e a intensidade


class TransformerValueModel(nn.Module):
    def __init__(self, args : Args):
        super(TransformerValueModel, self).__init__()
        
        self.embedding = nn.Linear(4, args.embed_dim)
        
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=args.embed_dim,
                nhead=args.num_heads,
                dim_feedforward=args.ff_dim,
                dropout=args.dropout
            ) for _ in range(args.num_layers)
        ])
        
        self.layer_norm = nn.LayerNorm(args.embed_dim)
        
        self.value_head = nn.Sequential(
            nn.Linear(args.embed_dim, args.ff_dim),  # Projeta para dimensão intermediária
            nn.ReLU(),                    # Ativação não-linear
            nn.Linear(args.ff_dim, 1)          # Saída escalar (valor do estado)
        )

    def forward(self, x, bola_branca):
        # Adiciona a dimensão da bolinha branca -> batch, (x,y,1,-1)
        b = bola_branca.shape[0]
        t_concat = torch.zeros(b, 2, device=bola_branca.device)
        t_concat[:, 0] = 1
        t_concat[:, 1] = -1
        bola_branca = torch.concat((bola_branca, t_concat), dim=-1).unsqueeze(1)
        x = torch.concat((bola_branca, x), dim=1)
        
        # Passa pela camada de embedding
        x = self.embedding(x)
        
        # Passa pelas camadas de encoder
        for layer in self.encoder_layers:
            x = layer(x)
        
        # Normalização final
        x = self.layer_norm(x)
        
        # Seleciona a representação do estado do jogo (primeiro token)
        x = x[:, 0, :]
        
        # Passa pela cabeça de valor para prever V(s)
        value = self.value_head(x)
        
        # Garante que a saída está no formato (batch_size,)
        return value  # Remove apenas a última dimensão
