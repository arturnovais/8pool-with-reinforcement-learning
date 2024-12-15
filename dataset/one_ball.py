from game import GAME
import torch
import numpy as np

import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import torch
import torch.nn as nn
import torch.nn.functional as F

from dataclasses import dataclass

from torch.distributions import Normal
from utils import config as cfg
from curriculum.reset import reset_random_one_ball
import matplotlib.pyplot as plt
import pickle

from tqdm import tqdm

def one_ball(amostras = 15_000):
    env = GAME(draw=False)  
    
    states, states_white, label = [],[],[]
    
    for _ in tqdm(range(amostras)):
        
        state, state_bola_branca = reset_random_one_ball(env=env)
        #x, y = state_bola_branca
        #x1, y1 = state[0][:2]

        distance = (state_bola_branca -state[0][:2]).pow(2).sum().item() **0.5
        
        #x *= cfg.display_table_width
        #x1 *= cfg.display_table_width
        #y *= cfg.display_table_height
        #y1 *= cfg.display_table_height
        
        x,y = (state[0][:2] - state_bola_branca)*torch.tensor([cfg.display_table_width, cfg.display_table_height])
        angulo = torch.atan2(y,x)
        
        intensidade  = torch.tensor(distance * 0.42)
        
        angulo = angulo.unsqueeze(0)
        intensidade = intensidade.unsqueeze(0)
        
        angulo = torch.concat([angulo, intensidade])
        
        
        
        
        states += [state]
        states_white += [state_bola_branca]
        label += [angulo]
        env.iniciou_jogada = False

    objeto_to_save = {
        'states': states,
        'states_white': states_white,
        'label': label
    }
    
    with open('dataset/one_ball.pkl', 'wb') as f:
        pickle.dump(objeto_to_save, f)
        print('Amostras salvas em dataset/one_ball.pkl')
        
        
