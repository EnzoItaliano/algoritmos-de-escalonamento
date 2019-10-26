import config
import time

processes_list = []     # lista que receberá todos o BCP dos processos 
number_of_process = 0   # numero de processos total (passados no arquivo txt)

QUANTUM = config.quantum_rr     # tamanho do quantum definido no arquivo config
tick = -1                       # cada vez que um processo é executado uma unidade do quantum no processador o tick é incrementado

processes_ready_queue = []      # lista de processos prontos para executar (em espera)
processes_blocked_queue = []    # lista de processos bloqueados
processes_finished_queue = []   # lista de processos finalizados

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
            processes_blocked_queue.append(running)     # adiciona-o na lista de bloqueados
            processes_ready_queue.pop(0)                # remove ele da fila de prontos
            running.quantum = 0                         # reseta seu quantum para zero
            running.ends.append(tick+1)                 # marca o tempo de saída do processador
            running.io_events.pop(0)                    # remove o evento já executado
            running.state = "blocked"                   # muda seu status para bloqueado

            return
        
    if running.duration == 0:                           # a duração é zero quando ele termina de executar completamente
        processes_finished_queue.append(running)        # adiciona-o na fila de terminados
        processes_ready_queue.pop(0)                    # remove-o da fila de prontos
        running.ends.append(tick+1)                     # marca o tempo de saída do processador
        global number_of_process
        number_of_process -= 1                          # diminui o numero de processos restantes
        running.state = "finished"                      # muda o estado para finalizado

        return

    elif running.quantum == 2:
        processes_ready_queue.append(running)
        processes_ready_queue.pop(0)

        running.ends.append(tick+1)
        running.quantum = 0
        running.state = "waiting"
            

def check(tick):
    if number_of_process != 0:
        for i in range(len(processes_list)):
            if tick == processes_list[i].incoming:
                processes_ready_queue.append(processes_list[i])
            if len(processes_blocked_queue) > 0:
                if tick - processes_blocked_queue[0].ends[len(processes_blocked_queue[0].ends) - 1] == QUANTUM:
                    processes_ready_queue.append(processes_blocked_queue[0])
                    processes_blocked_queue.pop(0)
        return True
    else:
        global end_condition
        end_condition = 1
        return False

end_condition = 0
def Run(processes):
    global processes_list
    global number_of_process
    processes_list = processes.copy()
    number_of_process = len(processes_list)
    while not end_condition:
        global tick
        tick += 1
        if check(tick):
            if len(processes_ready_queue) > 0:
                running_process = processes_ready_queue[0]
                running_process.state = "running"
                runOneTick(running_process)
        # time.sleep(0.5)

    # for i in processes_list:
    #     for j in range(len(i.starts)):
    #         print("Processo " + str(i.pid) + " Começa " + str(i.starts[j]) + " Termina " + str(i.ends[j]))