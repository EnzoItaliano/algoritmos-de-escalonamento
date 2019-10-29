"""*******************************************************************
* NOME DO ARQUIVO :    StatisticalAnalysis.py                        *
*                                                                    *
* DESCRIÇÂO :                                                        *
*                                                                    *
*       Este programa consiste em receber os dados de cada           *
*       processo, processá-los, e retornar suas análises             *
*       estatísticas. Como também a plotagem de um diagrama          *
*       de Grantt do escalonameto.                                   *
*                                                                    *
*                                                                    *
*                                                                    *
* AUTORES :    Matheus Batistela, Henrique Marcuzzo e Enzo Italiano  *
*                                                                    *
* DATA DE CRIAÇÃO :    18/10/2019                                    *   
*                                                                    *
* MODIFICAÇÕES :       28/10/2019                                    *
*                                                                    * 
**********************************************************************"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import Processes as pc
import random


CYCLE_TIME = 10                                                                                  # Assumindo o tempo de 10ms para cada ciclo (CPU de 100Hz)

def printAnalysis(processes_list,tick,len_blocked_queue,len_ready_queueA,len_ready_queueB=None): # printa no terminal as análises estatísticas do escalonamento dos processos
    
    total_wait_time = 0
    response_time = []

    print("-----------Dados-----------\n")

    for i in processes_list:
        
        print(f"-------Processo {i.pid}")                                                       # printa as dados de cada processo
        pc.printProcess(i)
        print(f"Uso de CPU: {i.cpu_use}")
        print(f"Tempo de espera: {i.wait_time}")
        for j in range(len(i.starts)):
            print("Começa " + str(i.starts[j]) + " Termina " + str(i.ends[j]))
        for j in range(len(i.block_starts)):
            print("Bloqueado " + str(i.block_starts[j]) + " Liberado " + str(i.block_ends[j]))
        print("\n")

        total_wait_time += i.wait_time                                                          # guarda o tempo total de espera

        blocked_time = 0
        for j in range(len(i.block_starts)):                                                    # guarda o tempo total de bloqueios
            block_interval = i.block_ends[j] - i.block_starts[j]
            blocked_time += block_interval
        
        response_time.append((i.wait_time + blocked_time + i.cpu_use)*CYCLE_TIME)               # guarda o temp total de execução, desde a solicitação até a resposta

    print("----------Estatísticas--------\n")
    
    tme =  float( '%.2f' % ( total_wait_time/len(processes_list) ))                             # tempo médio de espera   
    print(f"Tempo total de espera: {total_wait_time}\n")
    print(f"Tempo médio de espera: {tme}\n")

    if len_ready_queueB is not None:                                                            # caso houver duas filas de processos aptos
        tmfpa =  float( '%.2f' % ( (sum(len_ready_queueA))/(tick+1)))                           # tamanho médio da fila de aptos
        tmfpb =  float( '%.2f' % ( (sum(len_ready_queueB))/(tick+1)))                           # soma-se todos os tamanhos atingidos da fila de epera, e o divide pelo número total de ciclos
        print(f"Tamanho médio da fila de prontos A: {tmfpa}\n")
        print(f"Tamanho máximo da fila de prontos A: {max(len_ready_queueA)}\n")                # retorna o tamanho máximo atingido na fila de processos aptos
        print(f"Tamanho médio da fila de prontos B: {tmfpb}\n")
        print(f"Tamanho máximo da fila de prontos B: {max(len_ready_queueB)}\n")
    else:
        tmfp =  float( '%.2f' % ( (sum(len_ready_queueA))/(tick+1)))                            # caso houver apenas uma fila de processos aptos                               
        print(f"Tamanho médio da fila de prontos: {tmfp}\n")
        print(f"Tamanho máximo da fila de prontos: {max(len_ready_queueA)}\n")

    tmfb = float( '%.2f' % ( (sum(len_blocked_queue))/(tick+1)))                                # tamanho médio da fila de bloqueados
    print(f"Tamanho médio da fila de bloqueados: {tmfb}\n")                                     # soma-se todos os tamanhos atingidos da fila de bloqueados, e o divide pelo número total de ciclos
    print(f"Tamanho máximo da fila de bloqueados: {max(len_blocked_queue)}\n")                  # retorna o tamanho máximo atingido na fila de bloqueados

    processing_time = (tick+1)*CYCLE_TIME                                                       # tempo total de processamento do escalonamento
    troughput =  float( '%.2f' % ( (len(processes_list)/processing_time)*1000 ) )               # Troughput - número de processos executados por segundo
    print(f"Throughput do sistema: {troughput} processos/seg\n")

    j=0
    for i in processes_list:
        print(f"Tempo de resposta do processo {i.pid}: {response_time[j]}ms")           
        j+=1


def plot(processes_list,tick):                                              # função responsável pela plotagem do diagrama de Grantt

    tuples = []                                                             # pares ordenados (a,b), que representam momentos de execução de cada processo
    block_time_plot = []                                                    # pares ordenados (a,b), que representam momentos de bloqueio de cada processo
    wait_time_plot = []                                                     # pares ordenados (a,b), que representam momentos de espera de cada processo
    y_labels = [""]                                                         # lista de nomes de cada processo

    for i in processes_list:
        
        temp_tuples = []
        temp_block = []
        temp_wait = []

        y_labels.append("Processo "+str(i.pid))                             # define o label de cada processo no diagrama, baseado no seu pid

        temp_starts = i.starts.copy()
        temp_ends = i.ends.copy()

        temp_starts.pop(0)                                                   # shift para a esquerda na lista temporária de inícios de execução
        temp_ends.pop(len(temp_ends)-1)                                      # shift para a direita na lista temporária de términos de execução
                                                                             # os shifts auxiliam na definição do início da espera (final da execução) até fim da espera (início da próxima execução)

        if i.incoming != i.starts[0]:                                        # caso o processo não executou na sua chegada, insere os valores necessários para calcular o tempo de espera até a primeira execução
            temp_starts.insert(0,i.incoming)
            temp_ends.insert(0,i.starts[0])


        for j in range(len(i.starts)):
            temp_tuples.append(i.ends[j] - i.starts[j])                     # cria uma lista temporária com a duração de cada execução em cada momento de início de uma execução

        for j in range(len(i.block_starts)):
            block_interval = i.block_ends[j] - i.block_starts[j]
            temp_block.append(block_interval)                               # cria uma lista temporária com a duração de cada bloqueio em cada momento de início de um bloqueio

        for j in range(len(temp_starts)):
            temp_wait.append(temp_starts[j] - temp_ends[j])                 # cria uma lista temporária com a duração de cada momento de espera, após cada perca de processador

        tuples.append(list((zip(i.starts,temp_tuples))))                    # une as listas com todos os inícios de execuções e suas durações
        block_time_plot.append(list((zip(i.block_starts,temp_block))))      # une as listas com todos inícios de bloqueios e suas durações
        wait_time_plot.append(list((zip(temp_ends,temp_wait))))             # une as listas com todos os inícios de espera e suas durações           

        # limpa da memória as listas auxiliares
        del temp_tuples[:]
        del temp_block[:]
        del temp_starts[:]
        del temp_ends[:]
        del temp_wait[:]

    fig, ax = plt.subplots()
    for i in range(len(tuples)):                                             # realiza o "plot" das execuções, com cores aleatórias para cada processo
        ax.broken_barh(tuples[i], ((i+1), 1), color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

    for i in range(len(wait_time_plot)):                                     # realiza o "plot" dos momentos de espera
        ax.broken_barh(wait_time_plot[i], ((i+1), 1), color=(0,0,0),alpha=0.1)

    for i in range(len(block_time_plot)):                                    # realiza o "plot" dos bloqueios
        ax.broken_barh(block_time_plot[i], ((i+1), 1), color=(1,0,0),alpha=0.3,hatch='//')

    ax.set_ylim(True)                                                        # define os limites no modo auto
    ax.set_xlim(True)

    ax.set_xlabel('Ciclos de CPU')                                           # configurações visuais do matplotlib
    ax.set_yticklabels(y_labels) 
    ax.set_xticks(range(0, tick+2, 2))
    ax.set_yticks(range(0, len(processes_list)+2, 1))
    leg_wait = mpatches.Patch(color=(0,0,0),alpha=0.1, label='Espera')
    leg_block = mpatches.Patch(color=(1,0,0),alpha=0.3,hatch='//',label='Bloqueado')
    ax.legend(handles=[leg_wait,leg_block],
                loc='upper center', bbox_to_anchor=(0.5, 1.05),
                ncol=2, fancybox=True, shadow=True)

    ax.set_title('Diagrama de Grantt', pad=30)

    ax.grid()

    plt.show()                                                                # "plota" o gráfico numa nova janela