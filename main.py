"""*******************************************************************
* NOME DO ARQUIVO :    main.py                                       *
*                                                                    *
* DESCRIÇÂO :                                                        *
*                                                                    *
*        Este programa consiste em receber os dados de entrada       *
*        pelo terminal e  fazer o intermédio carregando os           *
*        processos, deixando-os prontos para ser executados          *
*        por um método de escalonamento que será de acordo com       *
*        o fornecido pelo usário na entrada.                         *       
*                                                                    *
*                                                                    *
*                                                                    *
* AUTORES :    Enzo Italiano, Henrique Marcuzzo e Matheus Batistela  *
*                                                                    *
* DATA DE CRIAÇÃO :    18/10/2019                                    *   
*                                                                    *
* MODIFICAÇÕES :       28/10/2019                                    *
*                                                                    * 
**********************************************************************"""

import sys
import Processes
import RoundRobin
import ShortestJobFirst
import DinamicPriority

processes_list = Processes.BCPs(open(sys.argv[1]))
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
