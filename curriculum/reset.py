import utils.config as cfg
import torch

def reset_random_one_ball(env,raio_buraco = 13):
    ## iniciar o ambiente com a configuração do jogo com apenas uma bola na mesa. 
    # - A bola branca em uma posição aleatória
    # - se não bater na bola, acabou a jogada

    cfg.raio_buraco = raio_buraco
    
    epson = raio_buraco*2

    env.reset()
    env.table.bolas = env.table.bolas[1:2] + [env.table.bola_branca]
    numero_bola = env.table.bolas[0].numero
    
    
    for _ ,  bola in enumerate(env.table.bolas):
        bola.posicao[1] = torch.rand(1).item() * (env.table.altura - epson*2  )  + env.table.y_start + epson
        bola.posicao[0] = torch.rand(1).item() * (env.table.largura - epson*2  ) + env.table.x_start + epson
        
    env.numero_bolas = [[ numero_bola ], [ numero_bola ]]
    
    return env.get_observations()
