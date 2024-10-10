from utils.Ball import Ball

class Pocket:
    '''
    Classe que representa um buraco (pocket) na mesa de sinuca.
    
    Args:
        posicao (tuple): Coordenadas (x, y) do centro do buraco.
        raio (float): Raio do buraco.
    '''
    
    def __init__(self, posicao: tuple, raio: float):
        '''
        Inicializa um buraco da mesa de sinuca com sua posição e raio.
        '''
        self.posicao = posicao
        self.raio = raio

    def verificar_bola_no_buraco(self, bola: Ball) -> bool:
        '''
        Verifica se uma bola foi encaçapada no buraco.
        
        Args:
            bola (Ball): Instância da bola que está sendo verificada.
        
        Returns:
            bool: True se a bola foi encaçapada, False caso contrário.
        '''
        distancia = ((bola.posicao[0] - self.posicao[0]) ** 2 + (bola.posicao[1] - self.posicao[1]) ** 2) ** 0.5
        
        return distancia <= self.raio
