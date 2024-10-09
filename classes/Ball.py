from  classes.PhysicsEnvironment import PhysicsEnvironment

class Ball:
    def __init__(self, numero: int, raio: float, massa: float, posicao: tuple, velocidade: tuple = (0, 0), rotação: float = 0):
        """
        Inicializa uma bola de sinuca com número, raio, massa, posição e velocidade inicial.

        Args:
            numero (int): O número da bola (1-15, por exemplo).
            raio (float): O raio da bola (geralmente em metros).
            massa (float): A massa da bola (em kg).
            posicao (tuple): A posição inicial da bola na mesa (x, y).
            velocidade (tuple): A velocidade inicial da bola (vx, vy). Padrão é (0, 0).
            rotação (float): A rotação inicial da bola em radianos.
        """
        self.numero = numero
        self.raio = raio
        self.massa = massa
        self.posicao = posicao  # Posição inicial da bola (x, y)
        self.velocidade = velocidade  # Velocidade (vx, vy)
        self.cor = (255, 255, 255)  # Cor da bola (padrão branca)
        if self.numero != 0:
            if self.numero % 2 == 0:
                self.cor = (255,0,0)
            else:
                self.cor = (0,0,255)
            
        
        #self.aceleracao = (0, 0)  # Aceleração (ax, ay)
        #self.rotação = rotação  # Rotação da bola (efeito)
        #self.spin = 0  # Spin da bola (efeito aplicado no movimento)
    
    def aplicar_forca(self, forca: tuple, dt: float):
        """
        Aplica uma força à bola e ajusta sua aceleração e velocidade de acordo.

        Args:
            forca (tuple): A força aplicada na bola (fx, fy) em Newtons.
            dt (float): O intervalo de tempo para o qual a força é aplicada (em segundos).
        """
        # Aceleração resultante da força aplicada (F = m * a => a = F / m)
        ax = forca[0] / self.massa
        ay = forca[1] / self.massa
        self.aceleracao = (ax, ay)
        
        # Atualiza a velocidade da bola com a aceleração
        self.velocidade = (
            self.velocidade[0] + self.aceleracao[0] * dt,
            self.velocidade[1] + self.aceleracao[1] * dt
        )
    
    def atualizar_posicao(self, dt: float, ambiente_fisico: PhysicsEnvironment):
        """
        Atualiza a posição da bola considerando a velocidade e o tempo decorrido,
        além de aplicar atrito, resistência do ar e verificar se a bola deve parar.

        Args:
            dt (float): Intervalo de tempo para atualização (em segundos).
            ambiente_fisico (PhysicsEnvironment): O ambiente físico que afeta o movimento da bola.
        """
        # Aplica as forças do ambiente físico (atrito, resistência do ar) e ajusta a velocidade
        self.velocidade = ambiente_fisico.aplicar_forcas(self.velocidade)

        # Atualiza a posição levando em conta a nova vel1ocidade e o tempo
        self.posicao = (
            self.posicao[0] + self.velocidade[0] * dt,
            self.posicao[1] + self.velocidade[1] * dt
        )
        
        # Aplica o spin ao movimento
        #self.aplicar_spin(dt)

    def aplicar_spin(self, dt: float):
        """
        Aplica o efeito de rotação da bola (spin) ao movimento, afetando a trajetória.

        Args:
            dt (float): Intervalo de tempo para atualização (em segundos).
        """
        # O spin afeta a trajetória da bola, aplicando uma leve alteração
        spin_efeito = self.spin * 0.05  # Escala o efeito do spin
        self.velocidade = (
            self.velocidade[0] + spin_efeito * dt,
            self.velocidade[1] - spin_efeito * dt
        )
