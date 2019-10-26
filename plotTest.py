import queue
import config
import sys
import processes
import time
import numpy as np
import matplotlib.pyplot as plt

p = processes.BCPs(open(sys.argv[1]))

number_of_process = len(p)

QUANTUM = config.quantum_rr
tick = -1

processes_ready_queue = []
processes_blocked_queue = []
processes_finished_queue = []

# p.sort(key=lambda x: x.incoming, reverse=False)


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


fig, ax = plt.subplots()
ax.broken_barh([(110, 30), (150, 10)], (10, 9), facecolors='tab:blue')
ax.broken_barh([(110, 10), (150, 5)], (10, 9), facecolors='tab:red')
ax.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
               facecolors=('tab:orange', 'tab:green', 'tab:red'))
ax.set_ylim(5, 35)
ax.set_xlim(0, 200)
ax.set_xlabel('seconds since start')
ax.set_yticks([15, 25])
ax.set_yticklabels(['Bill', 'Jim'])
ax.grid(True)

plt.show()