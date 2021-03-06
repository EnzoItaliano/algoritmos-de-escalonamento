"""*******************************************************************
* NOME DO ARQUIVO :    RoundRobin.py                                 *
*                                                                    *
* DESCRIÇÂO :                                                        *
*                                                                    *
*        Este programa consiste em simular um processador            *
*        em execução, utilizando o algoritimo de escalonamento       *
*        de processos Round Robin com quantum fixo.                  *
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
import StatisticalAnalysis as sa

processes_list = []     # lista que receberá todos o BCP dos processos 
number_of_process = 0   # numero de processos total (passados no arquivo txt)

QUANTUM = config.quantum_rr     # tamanho do quantum definido no arquivo config
tick = -1                       # cada vez que um processo é executado uma unidade do quantum no processador o tick é incrementado

processes_ready_queue = []      # lista de processos prontos para executar (em espera)
processes_blocked_queue = []    # lista de processos bloqueados
processes_finished_queue = []   # lista de processos finalizados
len_ready_queue = []            # guarda os tamanhos da lista de prontos a cada ciclo 
len_blocked_queue = []          # guarda os tamanhos da lista de bloqueados a cada ciclo

# p.sort(key=lambda x: x.incoming, reverse=False)


def runOneTick(running):        # função que executa uma unidade do quantum
    if running.quantum == 0:            # o quantum é zero quando o processo entra no processador então marca o momento na lista de inicios
        running.starts.append(tick)

    for x in processes_ready_queue:     # soma mais um no tempo de espera de todos os processos na fila de prontos e que tem o estado "waiting"
        if x.pid != running.pid:        
            x.wait_time += 1
        else:                           # o unico processo que não tem o estado "waiting" é o primeiro da fila pois está no processador então incrmenta seu tempo na cpu
            x.cpu_use += 1

    
    running.duration -= 1               # decrementa a duração restante do processo
    running.quantum += 1                #incrementa o tempo que ele já está no processador
    

    if len(running.io_events) != 0:                     # caso o processo em execução tenha eventos E/S ele precisa verificar se está no tempo de fazê-lo
        if running.io_events[0] == running.cpu_use:     # utiliza o seu tempo de cpu para saber se é hora de sair para fazer E/S
            running.io_events.pop(0)                    # remove o evento já executado
            processes_blocked_queue.append(running)     # adiciona-o na lista de bloqueados
            processes_ready_queue.pop(0)                # remove ele da fila de prontos

            running.quantum = 0                         # reseta seu quantum para zero
            running.ends.append(tick+1)                 # marca o tempo de saída do processador
            running.state = "blocked"                   # muda seu status para bloqueado
            running.block_starts.append(tick+1)         # marca o tempo de entrada na fila de bloqueados


            return
        
    if running.duration == 0:                           # a duração é zero quando ele termina de executar completamente
        processes_finished_queue.append(running)        # adiciona-o na fila de terminados
        processes_ready_queue.pop(0)                    # remove-o da fila de prontos

        running.ends.append(tick+1)                     # marca o tempo de saída do processador
        running.state = "finished"                      # muda o estado para finalizado

        global number_of_process
        number_of_process -= 1                          # diminui o numero de processos restantes

        return
        
    elif running.quantum == QUANTUM:                # se o processo já tiver utilizado dois quantuns do processador ele será removido
        processes_ready_queue.append(running)       # coloca-o no final da fila de prontos
        processes_ready_queue.pop(0)                # remove-o do começo                     

        running.ends.append(tick+1)                 # marca o tempo de término
        running.quantum = 0                         # reseta o quantum
        running.state = "waiting"                   # volta o status para "waiting"
            

def check(tick):
    if number_of_process != 0:                                      # checa se há processos para serem executados
        for i in range(len(processes_list)):
            if tick == processes_list[i].incoming:                  # se houver algum processo com o tempo de chegada do tick atual
                processes_ready_queue.append(processes_list[i])
                
        if len(processes_blocked_queue) > 0:                        # se houver algum processo na lista de bloqueados, verifica se já está no tempo de ele voltar para a fila de prontos
            if tick - processes_blocked_queue[0].ends[len(processes_blocked_queue[0].ends) - 1] == QUANTUM:
                processes_blocked_queue[0].block_ends.append(tick)  # marca o tempo de saída da fila de bloqueados
                processes_ready_queue.append(processes_blocked_queue[0])
                processes_blocked_queue.pop(0)
                  
        return True
    else:
        global end_condition    # muda a variavel de condição quando não há mais nenhum processo a ser executado
        end_condition = 1
        return False

end_condition = 0
def Run(processes):                             # função principal
    global processes_list
    global number_of_process
    processes_list = processes.copy()           # faz uma cópia da lista de processos passada por argumento
    number_of_process = len(processes_list)     # coloca o numero de processos total na variavel
    while not end_condition:
        global tick
        tick += 1                                               # incrementa o tick que corresponde a quantidade de vezes que o processador rodou
        len_ready_queue.append(len(processes_ready_queue))      # guarda o tamanho atual da fila de prontos
        len_blocked_queue.append(len(processes_blocked_queue))  # guarda o tamanho atual da fila de bloqueados
        if check(tick):                                         # função que verifica se existem processos a serem executados
            if len(processes_ready_queue) > 0:                  # verifica se há algum processo na fila de prontos
                running_process = processes_ready_queue[0]      # guarda o processo que será executado
                running_process.state = "running"               # altera seu estado
                runOneTick(running_process)                     # roda ele uma vez

    sa.printAnalysis(processes_list,tick,len_blocked_queue,len_ready_queue)
    sa.plot(processes_list,tick)

    # for i in processes_list:
    #     for j in range(len(i.starts)):
    #         print("Processo " + str(i.pid) + " Começa " + str(i.starts[j]) + " Termina " + str(i.ends[j]))