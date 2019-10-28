import sys
import processes
import RoundRobin
import ShortestJobFirst
import DinamicPriority

processes_list = processes.BCPs(open(sys.argv[1]))
# RoundRobin.Run(processes_list)
# ShortestJobFirst.Run(processes_list)
DinamicPriority.Run(processes_list)