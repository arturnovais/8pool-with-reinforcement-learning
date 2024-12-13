import sys

from models.agent import Agent
from models.model_transformers import Model_args
import pickle
import torch

def train():
    dataset = 'dataset\one_ball.pkl'
    
    with open(dataset, 'rb') as f:
        dataset = pickle.load(f)
        
    states, states_white, label = dataset['states'], dataset['states_white'], dataset['label']
    
    states_white = [ s.unsqueeze(0) for s in states_white]
    states = [ s.unsqueeze(0) for s in states]
    label = [ s.unsqueeze(0) for s in label]
    
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    batch_size = 10
    
    states = torch.concatenate(states).to(device)
    states_white = torch.concatenate(states_white).to(device)
    label = torch.concatenate(label).to(device)


    
    agent = Agent(action_dim=2, model_args=Model_args()).to(device)
    
    
    
    print("WARNING - APLICANDO NORMALIZAÇÃO NO DATASET")
    states[:,:,0] = states[:,:,0] / 800
    states[:,:,1] = states[:,:,1] / 400
    states_white[:,0] = states_white[:,0] / 800
    states_white[:,1] = states_white[:,1] / 400
    # -------------------------


    optimizer = torch.optim.Adam(agent.parameters(), lr=0.0001)
    loss = torch.nn.MSELoss()
    
    
    test_states =  states[6000:]
    test_states_white = states_white[6000:]
    test_label = label[6000:]
    
    states = states[:6000]
    states_white = states_white[:6000]
    label = label[:6000]
    
    
    for i in range(0, len(states), batch_size):
        batch_states = states[i:i+batch_size]
        batch_states_white = states_white[i:i+batch_size]
        batch_label = label[i:i+batch_size]
        
        output = agent.actor_mean(batch_states, batch_states_white)

        loss_value = loss(output, batch_label)
        print(loss_value)
        break

if __name__ == '__main__':
    train()