# Como compilar

python3 main.py inputProcesses.txt tipo

O tipo pode ser RR (Round Robin), SJF (Shortest Job First) e PDR (Prioridade dinâmica com retroalimentação)

Ex.:
```
python3 main.py inputProcesses.txt RR
```

# Como executar

Para alterar os processos basta abrir o inputProcesses.txt e mudar os números na ordem seguinte:

    1 - PID, 2 - Duração, 3 - Prioridade, 4 - tempo de chegada, 5 - Eventos de E/S, caso não queira eventos E/S simplesmente deixe em branco

# Bibliotecas usadas (descrever as não padrões)

* sys - da acesso à variaveis usadas pelo terminal e para funções que interagem diretamente com ele. Neste projeto foi utilizada apenas para pegar variáveis por linha de comando

* Processes - essa biblioteca corresponde ao código processes.py que contém todas as funções relacionadas aos BCPs

* RoundRobin - essa biblioteca corresponde ao código RoundRobin.py que contém o código de funcionamento do escalonador do tipo round robin (RR)

* ShortestJobFirst - essa biblioteca corresponde ao código ShortestJobFirst.py que contém o código de funcionamento do escalonador do tipo shortest job first (SJF)

* DinamicPriority - essa biblioteca corresponde ao código DinamicPriority.py que contém o código de funcionamento do escalonador do tipo prioridade dinâmica com retroalimentação (PDR)

* StatisticalAnalysis - essa biblioteca corresponde ao código StatisticalAnalysis.py que contém o código necessário para a plotagem do diagrama de Grantt e a exibição das estatísticas de escalonamento no terminal

* matplotlib - Biblioteca de plotagem de gráficos para Python
    Instalação:
    ```
    python3 -m pip install -U pip
    python3 -m pip install -U matplotlib
    ```

# Exemplo de uso

    Arquivo txt de entrada:
    0 10 4 0 3 5 7
    1 5 2 1
    2 2 1 5 1

Entrada do terminal:
```
python3 main.py inputProcesses.txt RR
```