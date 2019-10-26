class BCP:
    def __init__(self):
        self.pid = 0
        self.priority = 0
        self.state = "waiting"
        self.incoming = 0
        self.starts = []
        self.ends = []
        self.cpu_use = 0
        self.wait_time = 0
        self.duration = 0
        self.io_events = []
        self.quantum = 0
        self.time_block = 0;

def BCPs(fp):
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
    print("Duração: " + str(process.duration))
    print("Prioridade: " + str(process.priority))
    print("Chegada: " + str(process.incoming))
    for j in range(len(process.io_events)):
        print("Eventos: "+str(process.io_events[j]))
