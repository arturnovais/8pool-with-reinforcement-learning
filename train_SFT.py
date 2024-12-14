import sys

from models.agent import Agent
from models.model_transformers import Model_args
import pickle
import torch

def train():
    dataset = 'dataset\one_ball.pkl'
    
    with open(dataset, 'rb') as f:
        dataset = pickle.load(f)
        
    states, states_white, labels = dataset['states'], dataset['states_white'], dataset['label']
    
    states_white = [ s.unsqueeze(0) for s in states_white]
    states = [ s.unsqueeze(0) for s in states]
    labels = [ s.unsqueeze(0) for s in labels]
    
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    batch_size = 128
    
    states = torch.concatenate(states).to(device)
    states_white = torch.concatenate(states_white).to(device)
    labels = torch.concatenate(labels).to(device)

    
    agent = Agent(action_dim=2, model_args=Model_args()).to(device)
    
    
    
    print("WARNING - APLICANDO NORMALIZAÇÃO NO DATASET")
    states[:,:,0] = states[:,:,0] / 800
    states[:,:,1] = states[:,:,1] / 400
    states_white[:,0] = states_white[:,0] / 800
    states_white[:,1] = states_white[:,1] / 400
    # -------------------------

    epochs = 10
    loss = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(agent.parameters(), lr=0.001)
    
    
    split_idx = 6000
    test_states = states[split_idx:]
    test_states_white = states_white[split_idx:]
    test_labels = labels[split_idx:]

    train_states = states[:split_idx]
    train_states_white = states_white[:split_idx]
    train_labels = labels[:split_idx]
    
    
    
    losses = []
    
    for epc in range(epochs):
        for i in range(0, len(states), batch_size):
            batch_states = states[i:i+batch_size]
            batch_states_white = states_white[i:i+batch_size]
            batch_label = labels[i:i+batch_size]
            
            output = agent.actor_mean(batch_states, batch_states_white)

            loss_value = loss(output, batch_label)
            
            
            optimizer.zero_grad()
            loss_value.backward()
            optimizer.step()
            
            
        print(f"Epoch {epc}: Loss = {loss_value.item():.4f}")
        evaluate(agent, (test_states, test_states_white, test_labels))
        agent.train()    
                
            #if i % (batch_size * 50) == 0:
                #print(f"Batch {i // batch_size}: Loss = {loss_value.item():.4f}")
                #evaluate(agent, (test_states, test_states_white, test_labels))
                #agent.train()
         

         
         
         
def evaluate(agent, data):
    test_states, test_states_white, test_labels = data
    
    agent.eval()  # Coloca o modelo em modo de avaliação

    with torch.no_grad():
        output = agent.actor_mean(test_states, test_states_white)
        mse = torch.nn.functional.mse_loss(output, test_labels)

    print(f"Mean Squared Error (MSE) on test data: {mse.item():.4f}")         
         
         
         
         
         

if __name__ == '__main__':
    train()
    
        