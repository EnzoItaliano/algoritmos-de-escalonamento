import queue
import config
import sys
import processes

p = processes.BCPs(open(sys.argv[1]))
processes.printProcess(p[0])

number_of_process = len(p)

QUANTUM = config.quantum_rr
tick = -1

processes_queue = []

p.sort(key=lambda x: x.incoming, reverse=True)


def runOneTick(running):
    if running.quantum == 0:
        running.start = tick
    running.duration -= 1
    running.quantum += 1

    for x in processes_queue:
        if x.pid != running.pid:
            x.wait_time += 1
        else:
            x.cpu_use += 1

def check(tick):

    if number_of_process != 0:
        for i in range(len(p)):
            if tick == p[i].incoming
                processes_queue.append(p[i])
        if len(processes_queue) == 0:
            return False
        else:
            return True
    else:
        end_condition = 1
        return False


end_condition = 0
while not end_condition:
    tick += 1
    if check(tick):
        running_process = process_queue[0]
        running_process.state = "running"
        runOneTick(running_process)

                

