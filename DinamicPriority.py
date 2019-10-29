import config
import time
from random import randint
import StatisticalAnalysis as sa

processes_list = []     # lista que receberá todos o BCP dos processos 
number_of_process = 0   # numero de processos total (passados no arquivo txt)

QUANTUM_A = config.quantum_fila_a       # tempo mínimo de bloqueio para I/O (passados no arquivo txt)
QUANTUM_B = config.quantum_fila_b       # tempo mínimo de bloqueio para I/O (passados no arquivo txt)

tick = -1                               # cada vez que um processo é executado uma unidade do quantum no processador o tick é incrementado

processes_ready_queueA = []             # lista de processos prontos para executar da fila A (em espera)
processes_ready_queueB = []             # lista de processos prontos para executar da fila B(em espera)
processes_blocked_queue = []            # lista de processos bloqueados
processes_finished_queue = []           # lista de processos finalizados
len_ready_queueA = []            # guarda os tamanhos da lista de prontos "A", a cada ciclo 
len_ready_queueB = []            # guarda os tamanhos da lista de prontos "B", a cada ciclo 
len_blocked_queue = []          # guarda os tamanhos da lista de bloqueados a cada ciclo


def runOneTick(running, queue):                 # função que executa uma unidade de tempo
    
    running.starts.append(tick)             # marca o momento que o processo começou uma execução

    for x in processes_ready_queueA:    
        if x.pid != running.pid:                # soma mais um no tempo de espera e aumenta a prioridade dinâmica de todos os processos na fila de prontos e que tem o estado "waiting" da fila A
            x.wait_time += 1
            x.dynamic_priority += 1
        else:                                   # incrmenta seu tempo na cpu do processo em execução e reseta sua prioridade dinâmica
            x.cpu_use += 1
            x.dynamic_priority = x.priority

    for x in processes_ready_queueB:            # soma mais um no tempo de espera e aumenta a prioridade dinâmica de todos os processos na fila de prontos e que tem o estado "waiting" da fila B
        if x.pid != running.pid:
            x.wait_time += 1
        else:                                   # incrmenta seu tempo na cpu do processo em execução e reseta sua prioridade dinâmica
            x.cpu_use += 1

    
    running.duration -= 1                       # decrementa a duração restante do processo
    running.quantum += 1                        # incrementa o tempo que ele já está no processador

    if len(running.io_events) != 0:                     # caso o processo em execução tenha eventos I/O ele precisa verificar se está no tempo de fazê-lo
        if running.io_events[0] == running.cpu_use:     # utiliza o seu tempo de cpu para saber se é hora de sair para fazer I/O
            processes_blocked_queue.append(running)     # adiciona-o na lista de bloqueados

            if queue == 'A':
                processes_ready_queueA.pop(0)           # remove ele da fila A de prontos
            elif queue == 'B':
                processes_ready_queueB.pop(0)           # remove ele da fila B de prontos

            running.time_block = randint(2,5)           # é sorteado um tempo de bloqueio para este I/O

            running.quantum = 0                         # reseta seu quantum
            running.ends.append(tick+1)                 # marca o tempo de saída do processador
            running.io_events.pop(0)                    # remove o I/O já executado
            running.state = "blocked"                   # muda seu status para bloqueado
            running.block_starts.append(tick+1)         # marca o tempo de entrada na fila de bloqueados

            return
        
    if running.duration == 0:                           # a duração é zero quando ele termina de executar completamente
        processes_finished_queue.append(running)        # adiciona-o na fila de terminados

        if queue == 'A':
            processes_ready_queueA.pop(0)               # remove ele da fila A de prontos
        elif queue == 'B':
            processes_ready_queueB.pop(0)               # remove ele da fila B de prontos
        
        running.ends.append(tick+1)                     # marca o tempo de saída do processador

        global number_of_process                        
        number_of_process -= 1                          # diminui o numero de processos restantes

        running.state = "finished"                      # muda o estado para finalizado

        return

    if queue == 'A' and running.quantum == QUANTUM_A:       # se o processo for da fila A e exercutou a quantidade do seu quantum deve entrar nesta condição

        processes_ready_queueB.append(running)              # o processo é adicionado à última posição na fila B por ser CPU-Bound
        processes_ready_queueA.pop(0)                       # é removido da fila de prontos de A

        running.quantum = 0                                 # reseta seu quantum

    elif queue == 'B' and running.quantum == QUANTUM_B:
        processes_ready_queueB.append(running)              # o processo é adicionado à última posição na fila B por ser CPU-Bound
        processes_ready_queueB.pop(0)                       # é removido da primeira posição de B

        running.quantum = 0                                 # reseta seu quantum

    running.ends.append(tick+1)                         # marca o tempo de saída do processador
    running.state = "waiting"                           # volta o estado para esperando 
            

def check(tick):
    
    if number_of_process != 0:                                                      # se ainda houver processos para trabalhar continua
        for i in range(len(processes_list)):

            if tick == processes_list[i].incoming:                                  # entra quando houver um processo para chegar a fila de prontos 
                processes_list[i].dynamic_priority = processes_list[i].priority     # começa a prioridade dinâmica identica a prioridade estatica
                processes_ready_queueA.append(processes_list[i])                    # adiciona o processo que chegou a fila de prontos


        
        if len(processes_blocked_queue) > 0:        # entra quando houver um processo bloqueado devido a um I/O
        
            h = 0                                
            control = len(processes_blocked_queue)  # quantidade da fila de bloqueados
            while h < control:
                
                if tick - processes_blocked_queue[h].ends[len(processes_blocked_queue[h].ends) - 1] == processes_blocked_queue[h].time_block:       # entra quando estiver no momento de algum processo bloquado sair de I/O
                    processes_ready_queueA.append(processes_blocked_queue[h])                                                                       # adiciona-o novamente a fila de prontos
                    processes_blocked_queue[h].block_ends.append(tick)                                                                              # marca o tempo de saída da fila de bloqueados
                    processes_blocked_queue.pop(h)                                                                                                  # remove-o da fila de bloquados

                    h -= 1                  # utilizado para manter na mesma posiçãp
                    control -= 1            # diminui a quantidade de elementos da fila pois foi removido

                h += 1

        return True

    else:               # finaliza a simulação

        global end_condition
        end_condition = 1
        return False


end_condition = 0
def Run(processes):
    global processes_list
    global number_of_process
    processes_list = processes.copy()           # faz uma cópia da lista de processos passada por argumento
    number_of_process = len(processes_list)     # coloca o numero de processos total na variavel
    while not end_condition:
        global tick
        tick += 1
        len_ready_queueA.append(len(processes_ready_queueA))      # guarda o tamanho atual da fila de prontos "A"
        len_ready_queueB.append(len(processes_ready_queueB))      # guarda o tamanho atual da fila de prontos "B"
        len_blocked_queue.append(len(processes_blocked_queue))  # guarda o tamanho atual da fila de bloqueados
        if check(tick):
            if len(processes_ready_queueA) > 0:                                                         # se houver processos na lista A entra aqui (lista A tem prioridade sobre a lista B)
                if len(processes_ready_queueB) > 0 and processes_ready_queueB[0].quantum != 0:          # se um processo da lista B estava sendo executado, este é resetado
                    processes_ready_queueB[0].quantum = 0                                               # reseta o quantum

                    processes_ready_queueA.append(processes_ready_queueB[0])                            # por terminar antes do tempo, é adicionado a lista A (processos que terminam antes do quantum)
                    processes_ready_queueB.pop(0)                                                       # remove o processo da lista B

                processes_ready_queueA.sort(key=lambda x: x.dynamic_priority, reverse=True)             # organiza novamente a fila de prontos de acordo com a prioridade dinâmica
                running_process = processes_ready_queueA[0]                                             # pega o primeiro processo da fila de prontos
                running_process.state = "running"                                                       # muda o seu estado para executando
                runOneTick(running_process, 'A')                                                        # roda a rotina de execução do processo

            elif len(processes_ready_queueB) > 0:                   # se não houver processos prontos na fila A, houver em B começa a executar B
                running_process = processes_ready_queueB[0]         # pega o primeiro processo da fila de prontos
                running_process.state = "running"                   # muda o seu estado para executando
                runOneTick(running_process, 'B')                    # roda a rotina de execução do processo

    sa.printAnalysis(processes_list,tick,len_blocked_queue,len_ready_queueA,len_ready_queueB)
    sa.plot(processes_list,tick)
