import sys

class BCP(object):
    def __init__(self):
        self.pid = 0
        self.prioridade = 0
        self.estado = 0
        self.tempos = []
        self.eventosIO = []

end_condition = 0

while not end_condition: