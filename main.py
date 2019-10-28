import sys
import processes
import RoundRobin
import ShortestJobFirst
import DinamicPriority

processes_list = processes.BCPs(open(sys.argv[1]))
Type = sys.argv[2]
switcher = {
    "RR": 1,
    "SJF": 2,
    "PDR": 3
}
if switcher.get(Type) == 1:
    RoundRobin.Run(processes_list)
elif switcher.get(Type) == 2:
    ShortestJobFirst.Run(processes_list)
elif switcher.get(Type) == 3:
    DinamicPriority.Run(processes_list)
else:
    print("Invalid Type")
