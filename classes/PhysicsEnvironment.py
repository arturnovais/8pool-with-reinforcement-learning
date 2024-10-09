class PhysicsEnvironment:
    def __init__(self, friccao: float = 0.995, resistencia_ar: float = 0.999):
        """
        Inicializa o ambiente físico com atrito e resistência do ar.

        Args:
            friccao (float): O fator de atrito da superfície da mesa (0 < friccao <= 1).
            resistencia_ar (float): O fator de resistência do ar (0 < resistencia_ar <= 1).
        """
        self.friccao = friccao
        self.resistencia_ar = resistencia_ar

    def aplicar_atrito(self, velocidade: tuple) -> tuple:
        """
        Aplica o atrito à velocidade da bola, reduzindo-a gradualmente.

        Args:
            velocidade (tuple): A velocidade da bola (vx, vy).

        Returns:
            tuple: A nova velocidade após aplicar o atrito.
        """
        return (
            velocidade[0] * self.friccao,
            velocidade[1] * self.friccao
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
