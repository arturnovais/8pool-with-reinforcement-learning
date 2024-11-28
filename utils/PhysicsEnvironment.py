import torch
import utils.config as cfg

class PhysicsEnvironment:
    '''
    Classe que representa o ambiente físico do jogo, aplicando forças como atrito e resistência do ar às bolas de sinuca.
    
    Args:
        friccao_dinamica (float): O fator de atrito dinâmico da superfície da mesa (0 < friccao_dinamica <= 1).
        friccao_estatica (float): O fator de atrito estático que age quando a bola se move devagar (0 < friccao_estatica <= 1).
        resistencia_ar (float): O fator de resistência do ar (0 < resistencia_ar <= 1).
    '''
    
    def __init__(self, 
                       
                       
                    ):
        '''
        Inicializa o ambiente físico com atrito dinâmico, atrito estático e resistência do ar.
        '''
        self.friccao_dinamica = torch.tensor(cfg.friccao_dinamica, device=cfg.device, dtype=torch.float32)
        self.friccao_estatica = torch.tensor(cfg.friccao_estatica, device=cfg.device, dtype=torch.float32)
        self.resistencia_ar =   torch.tensor(cfg.resistencia_ar, device=cfg.device, dtype=torch.float32)
        self.limiar_atrito = torch.tensor(cfg.limiar_atrito, device=cfg.device, dtype=torch.float32)# Define o limiar entre o atrito dinâmico e estático

    def aplicar_atrito2(self, velocidade: torch.tensor) -> torch.tensor:
        '''
        Aplica o atrito à velocidade da bola. Quando a bola está se movendo rapidamente, o atrito dinâmico é usado. 
        Quando está se movendo devagar, o atrito estático é usado.
        
        Args:
            velocidade (tuple): A velocidade da bola (vx, vy).
        
        Returns:
            tuple: A nova velocidade após aplicar o atrito.
        '''
        magnitude_velocidade = velocidade.pow(2).sum().sqrt()
          

        if magnitude_velocidade > self.limiar_atrito:
            friccao_real = self.friccao_dinamica * (1 - (magnitude_velocidade * 0.0005))
        else:
            friccao_real = self.friccao_estatica

        friccao_real = friccao_real.clamp(0, 1)
        
        return velocidade * friccao_real
            
    def aplicar_atrito(self, velocidade: torch.tensor) -> torch.tensor:
        '''
        Aplica o atrito à velocidade da bola. Quando a bola está se movendo rapidamente, o atrito dinâmico é suavemente reduzido.
        Quando está se movendo devagar, o atrito estático é suavemente aplicado de forma mais intensa.
        
        Args:
            velocidade (torch.tensor): A velocidade da bola (vx, vy).
        
        Returns:
            torch.tensor: A nova velocidade após aplicar o atrito.
        '''
        # Calcula a magnitude da velocidade
        magnitude_velocidade = velocidade.pow(2).sum().sqrt()

        # Define um fator de redução baseado em uma curva logística
        
        if magnitude_velocidade > 0:
            friccao_real = self.friccao_dinamica / (1 + torch.exp(-10 * (magnitude_velocidade)))
        else:
            friccao_real = self.friccao_estatica

        # Limita o atrito para evitar valores inconsistentes
        friccao_real = friccao_real.clamp(0.1, 0.99)
        
        # Aplica o atrito à velocidade
        return velocidade * friccao_real


    def aplicar_resistencia_ar(self, velocidade: torch.tensor) -> torch.tensor:
        '''
        Aplica a resistência do ar à velocidade da bola.
        
        Args:
            velocidade (tuple): A velocidade da bola (vx, vy).
        
        Returns:
            tuple: A nova velocidade após aplicar a resistência do ar.
        '''
        return velocidade * self.resistencia_ar

