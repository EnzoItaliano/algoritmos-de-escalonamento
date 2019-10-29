"""*******************************************************************
* NOME DO ARQUIVO :    ShortestJobFirst.py                           *
*                                                                    *
* DESCRIÇÂO :                                                        *
*                                                                    *
*        Este programa consiste em simular um processador            *
*        em execução, utilizando o algoritimo de escalonamento       *
*        de processos Shortest Job First com Previsão e Preempção.   *
*        E também armazenar os dados para produção de estatíticas    *
*        futuras.                                                    *
*                                                                    *
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

import config
import time
from random import randint
import StatisticalAnalysis as sa

processes_list = []     # lista que receberá todos o BCP dos processos 
number_of_process = 0   # numero de processos total (passados no arquivo txt)

QUANTUM_MIN = config.tempo_min_io       # tempo mínimo de bloqueio para I/O (passados no arquivo txt)
QUANTUM_MAX = config.tempo_max_io       # tempo mínimo de bloqueio para I/O (passados no arquivo txt)
ALPHA = config.alpha

tick = -1                               # cada vez que um processo é executado uma unidade do quantum no processador o tick é incrementado

processes_ready_queue = []              # lista de processos prontos para executar (em espera)
processes_blocked_queue = []            # lista de processos bloqueados
processes_finished_queue = []           # lista de processos finalizados
len_ready_queue = []                    # guarda os tamanhos da lista de prontos a cada ciclo 
len_blocked_queue = []                  # guarda os tamanhos da lista de bloqueados a cada ciclo



def runOneTick(running):                # função que executa uma unidade de tempo
    running.starts.append(tick)         # marca o momento que o processo começou uma execução

    for x in processes_ready_queue:     # soma mais um no tempo de espera de todos os processos na fila de prontos e que tem o estado "waiting"
        if x.pid != running.pid:
            x.wait_time += 1
        else:                           # o unico processo que não tem o estado "waiting" é o primeiro da fila pois está no processador então incrmenta seu tempo na cpu
            x.cpu_use += 1

    
    running.duration -= 1               # decrementa a duração restante do processo
    running.duration_prevision.append( int( (ALPHA * running.duration) + (ALPHA * running.duration_prevision[len(running.duration_prevision) - 1]) ) )      # faz uma nova previsão de tempo que ira durar o processo
    

    if len(running.io_events) != 0:     # caso o processo em execução tenha eventos I/O ele precisa verificar se está no tempo de fazê-lo
        if running.io_events[0] == running.cpu_use:     # utiliza o seu tempo de cpu para saber se é hora de sair para fazer I/O
            processes_blocked_queue.append(running)     # adiciona-o na lista de bloqueados
            processes_ready_queue.pop(0)                # remove ele da fila de prontos
            
            running.time_block = randint(QUANTUM_MIN,QUANTUM_MAX)       # é sorteado um tempo de bloqueio para este I/O

            running.ends.append(tick+1)                 # marca o tempo de saída do processador
            running.io_events.pop(0)                    # remove o I/O já executado
            running.state = "blocked"                   # muda seu status para bloqueado
            running.block_starts.append(tick+1)         # marca o tempo de entrada na fila de bloqueados

            return
        
    if running.duration == 0:                           # a duração é zero quando ele termina de executar completamente
        processes_finished_queue.append(running)        # adiciona-o na fila de terminados
        processes_ready_queue.pop(0)                    # remove-o da fila de prontos
        running.ends.append(tick+1)                     # marca o tempo de saída do processador

        global number_of_process                        
        number_of_process -= 1                          # diminui o numero de processos restantes

        running.state = "finished"                      # muda o estado para finalizado

        return

    else:

        running.ends.append(tick+1)                     # marca o tempo de saída do processador (para o caso dele não voltar)
        running.state = "waiting"                       # volta o estado para esperado (para o caso dele não voltar)
            

def check(tick):
    
    if number_of_process != 0:                          # se ainda houver processos para trabalhar continua
        for i in range(len(processes_list)):

            if tick == processes_list[i].incoming:                   # entra quando houver um processo para chegar a fila de prontos 
                processes_list[i].duration_prevision.append(processes_list[i].duration)
                processes_ready_queue.append(processes_list[i])      # adiciona o processo que chegou a fila de prontos

                processes_ready_queue.sort(key=lambda x: x.duration_prevision[len(x.duration_prevision) - 1], reverse=False)     # organiza a fila de acordo com o menor tempo da previsão


        if len(processes_blocked_queue) > 0:        # entra quando houver um processo bloqueado devido a um I/O

            h = 0  
            control = len(processes_blocked_queue)  # quantidade da fila de bloqueados
            while h < control:

                if tick - processes_blocked_queue[h].ends[len(processes_blocked_queue[h].ends) - 1] == processes_blocked_queue[h].time_block:      # entra quando estiver no momento de algum processo bloquado sair de I/O
                    processes_ready_queue.append(processes_blocked_queue[h])                     # adiciona-o novamente a fila de prontos
                    processes_blocked_queue[h].block_ends.append(tick)                           # marca o tempo de saída da fila de bloqueados
                    processes_blocked_queue.pop(h)                                               # remove-o da fila de bloquados
                    
                    h -= 1                  # utilizado para manter na mesma posiçãp
                    control -= 1            # diminui a quantidade de elementos da fila pois foi removido

                    processes_ready_queue.sort(key=lambda x: x.duration_prevision[len(x.duration_prevision) - 1], reverse=False)     # organiza novamente a fila de prontos de acordo com o menor tempo da previsão

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
        len_ready_queue.append(len(processes_ready_queue))      # guarda o tamanho atual da fila de prontos
        len_blocked_queue.append(len(processes_blocked_queue))  # guarda o tamanho atual da fila de bloqueados
        if check(tick):
            if len(processes_ready_queue) > 0:
                running_process = processes_ready_queue[0]      # pega o primeiro processo da fila de prontos
                running_process.state = "running"               # muda o seu estado para executando
                runOneTick(running_process)                     # roda a rotina de execução do processo

    sa.printAnalysis(processes_list,tick,len_blocked_queue,len_ready_queue)
    sa.plot(processes_list,tick)