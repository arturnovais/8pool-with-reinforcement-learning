import math
from utils.Ball import Ball

class Cue:
    def __init__(self, força_maxima: float = 10.0):
        """
        Inicializa o taco de sinuca com a força máxima que pode ser aplicada.

        Args:
            força_maxima (float): A força máxima que o taco pode aplicar na bola (em Newtons).
        """
        self.força_maxima = força_maxima  # A força máxima que o taco pode aplicar

    def calcular_forca(self, intensidade: float, angulo: float) -> tuple:
        """
        Calcula a força a ser aplicada na bola com base na intensidade e no ângulo da tacada.

        Args:
            intensidade (float): A intensidade da tacada, de 0 a 1 (representando uma fração da força máxima).
            angulo (float): O ângulo da tacada em radianos, relativo ao eixo horizontal da mesa.

        Returns:
            tuple: A força aplicada na bola nas direções x e y (fx, fy).
        """
        # Garante que a intensidade esteja entre 0 e 1
        intensidade = min(max(intensidade, 0), 1)

        # Calcula a força total a ser aplicada
        forca_total = intensidade * self.força_maxima

        # Decomposição da força em componentes x e y, usando seno e cosseno do ângulo
        fx = forca_total * math.cos(angulo)
        fy = forca_total * math.sin(angulo)

        return fx, fy

    def aplicar_tacada(self, bola: Ball, intensidade: float, angulo: float):
        """
        Aplica a tacada na bola, calculando a força a ser aplicada e ajustando a velocidade da bola.

        Args:
            bola (Ball): A bola que será golpeada pelo taco.
            intensidade (float): A intensidade da tacada, de 0 a 1.
            angulo (float): O ângulo da tacada em radianos, relativo ao eixo horizontal da mesa.
        """
        # Calcula a força a ser aplicada na bola
        forca = self.calcular_forca(intensidade, angulo)

        # Aplica a força à bola (método da classe Ball)
        bola.aplicar_forca(forca, dt=0.1)  # Aqui usamos um pequeno intervalo de tempo dt para a tacada inicial
