import queue
import config
import sys
import processes
import time
import numpy as np
import matplotlib.pyplot as plt
import random

p = processes.BCPs(open(sys.argv[1]))

number_of_process = len(p)

QUANTUM = config.quantum_rr
tick = -1

processes_ready_queue = []
processes_blocked_queue = []
processes_finished_queue = []


def runOneTick(running):
    if running.quantum == 0:
        running.starts.append(tick)

    for x in processes_ready_queue:
        if x.pid != running.pid:
            x.wait_time += 1
        else:
            x.cpu_use += 1

    
    running.duration -= 1
    running.quantum += 1
    

    if len(running.io_events) != 0:
        if running.io_events[0] == running.cpu_use:
            processes_blocked_queue.append(running)
            processes_ready_queue.pop(0)
            running.quantum = 0
            running.ends.append(tick+1)
            running.io_events.pop(0)
            running.state = "blocked"

            return
        
    if running.duration == 0:
        processes_finished_queue.append(running)
        processes_ready_queue.pop(0)
        running.ends.append(tick+1)
        global number_of_process
        number_of_process -= 1
        running.state = "finished"

        return

    elif running.quantum == 2:
        processes_ready_queue.append(running)
        processes_ready_queue.pop(0)

        running.ends.append(tick+1)
        running.quantum = 0
        running.state = "waiting"
            

def check(tick):
    
    if number_of_process != 0:
        for i in range(len(p)):
            if tick == p[i].incoming:
                processes_ready_queue.append(p[i])
            if len(processes_blocked_queue) > 0:
                if tick - processes_blocked_queue[0].ends[len(processes_blocked_queue[0].ends) - 1] == QUANTUM:
                    processes_ready_queue.append(processes_blocked_queue[0])
                    processes_blocked_queue.pop(0)
                else:
                    processes_blocked_queue[0].time_block +=1
        else:
            return True
    else:
        global end_condition
        end_condition = 1
        return False

end_condition = 0
while not end_condition:
    tick += 1
    if check(tick):
        if len(processes_ready_queue) > 0:
            running_process = processes_ready_queue[0]
            running_process.state = "running"
            runOneTick(running_process)
    # time.sleep(0.5)

for i in p:
    print("-------Processo " + str(i.pid))
    processes.printProcess(i)
    for j in range(len(i.starts)):
        print("Começa " + str(i.starts[j]) + " Termina " + str(i.ends[j]))
    print(i.cpu_use)
    print(i.wait_time)
    print(i.time_block)


pairs = []
wait_time_plot = []
labels = [""]


# p.sort(key=lambda x: x.incoming, reverse=False)

for i in p:
    
    temp = []
    labels.append("Processo "+str(i.pid))

    for j in range(len(i.starts)):
        temp.append(i.ends[j] - i.starts[j])

    pairs.append(list((zip(i.starts,temp))))
    del temp[:]



fig, ax = plt.subplots()
for i in range(len(pairs)):
    ax.broken_barh(pairs[i], ((i+1), 1), color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))



ax.set_ylim(True)
ax.set_xlim(True)
ax.set_xlabel('Ciclos de CPU')
# ax.set_ylabel('Processos')
ax.set_yticklabels(labels) 
ax.set_xticks(np.arange(0, tick+2, 1))
ax.set_yticks(np.arange(0, len(p)+2, 1))

ax.grid()

plt.show()