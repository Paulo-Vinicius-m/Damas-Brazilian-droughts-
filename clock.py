import time

class Clock:
    # classe para o relógio
    # o relógio só conta durante a vez do adversário e contem o tempo restante para todo os lances da partida
    # a cada lance que o cara faz, ele ganha um acréscimo

    def __init__(self, side, max_time, increment = 0) -> None:
        self.side = side
        self.remaining = max_time
        self.inc = increment
        self.last_time = time.time()

    def get_time(self, turno):
        # calcula quanto tempo se passou desde a ultima vez que o método foi chamado e atualiza o relógio com base nisso

        if turno == self.side and self.remaining > 0:
            t = time.time()
            self.remaining = self.remaining + self.last_time - t
            self.last_time = t

        elif self.remaining < 0:
            # se o tempo acabou, retorna 0 pra impedir que apareça tempo negativo na tela
            return 0
            
        return self.remaining

    def incremento(self):
        # o incremento tem que ser feito separadamente para garantir que só pe feito um incremento por lance, pois o get_time() é chamado a cada frame do jogo
        self.remaining += self.inc