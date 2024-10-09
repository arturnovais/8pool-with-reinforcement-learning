import math

class PhysicsEnvironment:
    def __init__(self, friccao_dinamica: float = 0.99, friccao_estatica: float = 0.95, resistencia_ar: float = 0.999):
        """
        Inicializa o ambiente físico com atrito dinâmico, atrito estático e resistência do ar.

        Args:
            friccao_dinamica (float): O fator de atrito dinâmico da superfície da mesa (0 < friccao_dinamica <= 1).
            friccao_estatica (float): O fator de atrito estático que age quando a bola se move devagar (0 < friccao_estatica <= 1).
            resistencia_ar (float): O fator de resistência do ar (0 < resistencia_ar <= 1).
        """
        self.friccao_dinamica = friccao_dinamica  # Atrito quando a bola está se movendo rapidamente
        self.friccao_estatica = friccao_estatica  # Atrito quando a bola está se movendo lentamente
        self.resistencia_ar = resistencia_ar

    def aplicar_atrito(self, velocidade: tuple) -> tuple:
        """
        Aplica o atrito à velocidade da bola. Quando a bola está se movendo rapidamente, o atrito dinâmico é usado. Quando está se movendo devagar, o atrito estático é usado.

        Args:
            velocidade (tuple): A velocidade da bola (vx, vy).

        Returns:
            tuple: A nova velocidade após aplicar o atrito.
        """
        magnitude_velocidade = math.sqrt(velocidade[0]**2 + velocidade[1]**2)

        # Define o limiar entre o atrito dinâmico e estático
        limiar_atrito = 0.5  # Quando a magnitude da velocidade está abaixo desse limiar, usamos o atrito estático

        if magnitude_velocidade > limiar_atrito:
            # Atrito dinâmico quando a bola está rápida
            friccao_real = self.friccao_dinamica * (1 - (magnitude_velocidade * 0.0005))  # A fricção diminui com a velocidade
        else:
            # Atrito estático quando a bola está lenta
            friccao_real = self.friccao_estatica

        # Garante que a fricção não seja negativa
        friccao_real = max(friccao_real, 0)

        # Aplica o fator de atrito à velocidade
        return (
            velocidade[0] * friccao_real,
            velocidade[1] * friccao_real
        )

    def aplicar_resistencia_ar(self, velocidade: tuple) -> tuple:
        """
        Aplica a resistência do ar à velocidade da bola.

        Args:
            velocidade (tuple): A velocidade da bola (vx, vy).

        Returns:
            tuple: A nova velocidade após aplicar a resistência do ar.
        """
        return (
            velocidade[0] * self.resistencia_ar,
            velocidade[1] * self.resistencia_ar
        )

    def aplicar_forcas(self, velocidade: tuple) -> tuple:
        """
        Aplica todas as forças físicas (atrito e resistência do ar) à bola.

        Args:
            velocidade (tuple): A velocidade atual da bola (vx, vy).

        Returns:
            tuple: A nova velocidade da bola após aplicar todas as forças.
        """
        # Aplica o atrito, que varia conforme a velocidade
        velocidade = self.aplicar_atrito(velocidade)

        # Aplica a resistência do ar
        velocidade = self.aplicar_resistencia_ar(velocidade)

        return velocidade
