import sys
import processes
import RoundRobin
import ShortestJobFirst

processes_list = processes.BCPs(open(sys.argv[1]))
Type = sys.argv[2]
switcher = {
    1: "RR"
    2: "SJF"
    3: "PDR"
}
if switcher.get(Type) == 1:
    RoundRobin.Run(processes_list)
elif switcher.get(Type) == 2:
    ShortestJobFirst.Run(processs_list)
