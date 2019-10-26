import sys
import processes
import RoundRobin

processes_list = processes.BCPs(open(sys.argv[1]))
RoundRobin.Run(processes_list)
# processes.printProcess(process_list,0)