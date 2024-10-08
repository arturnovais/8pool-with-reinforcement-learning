from classes.Ball import Ball
class Pocket:
    def __init__(self, posicao: tuple, raio: float):
        """
        Inicializa um buraco da mesa de sinuca com sua posição e raio.

        Args:
            posicao (tuple): As coordenadas (x, y) do centro do buraco.
            raio (float): O raio do buraco.
        """
        self.posicao = posicao  # Coordenadas do centro do buraco
        self.raio = raio  # Raio do buraco

    def verificar_bola_no_buraco(self, bola: Ball) -> bool:
        """
        Verifica se a bola foi encaçapada no buraco.

        Args:
            bola (Ball): Instância da bola que está sendo verificada.

        Returns:
            bool: True se a bola foi encaçapada no buraco, False caso contrário.
        """
        # Calcula a distância entre o centro da bola e o centro do buraco
        distancia = ((bola.posicao[0] - self.posicao[0]) ** 2 + (bola.posicao[1] - self.posicao[1]) ** 2) ** 0.5
        
        # Verifica se a distância entre o centro da bola e o centro do buraco é menor que a soma dos raios
        if distancia <= self.raio:
            return True
        return False
