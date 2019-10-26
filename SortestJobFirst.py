import config
import sys
import processes
import time
from random import randint

p = processes.BCPs(open(sys.argv[1]))

number_of_process = len(p)

QUANTUM_MIN = config.tempo_min_io
QUANTUM_MAX = config.tempo_max_io
tick = -1

processes_ready_queue = []
processes_blocked_queue = []
processes_finished_queue = []

p.sort(key=lambda x: x.incoming, reverse=False)


def runOneTick(running):
    running.starts.append(tick)

    for x in processes_ready_queue:
        if x.pid != running.pid:
            x.wait_time += 1
        else:
            x.cpu_use += 1

    
    running.duration -= 1
    

    if len(running.io_events) != 0:
        if running.io_events[0] == running.cpu_use:
            processes_blocked_queue.append(running)
            processes_ready_queue.pop(0)

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

    else:

        running.ends.append(tick+1)
        running.state = "waiting"
            

def check(tick):
    
    if number_of_process != 0:
        for i in range(len(p)):
            if tick == p[i].incoming:
                p[i].time_block = randint(QUANTUM_MIN,QUANTUM_MAX)
                processes_ready_queue.append(p[i])

                processes_ready_queue.sort(key=lambda x: x.priority, reverse=False)
                for i in range(len(processes_ready_queue)):
                    j = i + 1
                    for j in range(len(processes_ready_queue)):
                        if processes_ready_queue[i].duration < processes_ready_queue[j].duration:
                            processes_ready_queue[i], processes_ready_queue[j] = processes_ready_queue[j], processes_ready_queue[i]

            if len(processes_blocked_queue) > 0:

                for j in range(len(processes_blocked_queue)):
                    if tick - processes_blocked_queue[j].ends[len(processes_blocked_queue[j].ends) - 1] == processes_blocked_queue[j].time_block:
                        processes_ready_queue.append(processes_blocked_queue[j])
                        processes_blocked_queue.pop(j)

                        processes_ready_queue.sort(key=lambda x: x.priority, reverse=False)
                        for h in range(len(processes_ready_queue)):
                            k = h + 1
                            for k in range(len(processes_ready_queue)):
                                if processes_ready_queue[h].duration < processes_ready_queue[k].duration:
                                    processes_ready_queue[h], processes_ready_queue[k] = processes_ready_queue[k], processes_ready_queue[h]

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
    for j in range(len(i.starts)):
        print("Processo " + str(i.pid) + " Começa " + str(i.starts[j]) + " Termina " + str(i.ends[j]))