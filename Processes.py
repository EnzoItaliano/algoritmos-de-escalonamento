"""*******************************************************************
* NOME DO ARQUIVO :    Processes.py                                  *
*                                                                    *
* DESCRIÇÂO :                                                        *
*                                                                    *
*        Este programa consiste em receber os dados de cada          *
*        processo, e armazena-los em suas estruturas definidas       *   
*        para serem utilizados pela simulação de escolamento         *
*        de processos.                                               *
*                                                                    *
*                                                                    *
*                                                                    *
* AUTORES :    Enzo Italiano, Henrique Marcuzzo e Matheus Batistela  *
*                                                                    *
* DATA DE CRIAÇÃO :    18/10/2019                                    *   
*                                                                    *
* MODIFICAÇÕES :       28/10/2019                                    *
*                                                                    * 
**********************************************************************"""

class BCP:                              # classe BCP, utilizado como se fosse uma struct
    def __init__(self):
        self.pid = 0                    # PID do processo
        self.priority = 0               # prioridade do processo
        self.dynamic_priority = 0       # prioridade dinâmica do processo
        self.state = "waiting"          # estado atual do processo: em espera, bloqueado, pronto, finalizado
        self.incoming = 0               # tempo de chegada do processo
        self.starts = []                # momentos em que o processo entra no processador
        self.ends = []                  # momentos em que o processo sai do processador
        self.cpu_use = 0                # tempos de uso da cpu do processo
        self.wait_time = 0              # tempos de espera do processo
        self.duration = 0               # duração total do processo
        self.duration_prevision = []    # previsão de duração do processo
        self.io_events = []             # chegada de momentos de E/S
        self.quantum = 0                # unidade de tempo dentro do processador
        self.block_starts = []          # momentos em que o processo entra na fila de bloqueados
        self.block_ends = []            # momentos em que o processo é liberado da fila de bloqueados
        self.time_block = 0;            # tempo bloqueado


def BCPs(fp):                           # coloca os dados do txt de entrada em objetos 
    process = []
    i=0
    for linha in fp:
        values = linha.split()
        process.append(BCP())
        process[i].pid = int(values[0])
        process[i].duration = int(values[1])
        process[i].priority = int(values[2])
        process[i].incoming = int(values[3])
        if len(values) > 4:
            values[4:]
            for j in range(4,len(values)):
                process[i].io_events.append(int(values[j]))
        i+=1
    return process

# process.sort(key=lambda x: x.incoming, reverse=True)

def printProcess(process):
    print("PID: " + str(process.pid))
    print("Prioridade: " + str(process.priority))
    print("Chegada: " + str(process.incoming))
