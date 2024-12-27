import time
import subprocess
import random
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

# Caminho para o executável a ser testado
executavel = "./stor"

def run_makefile():
    try:
        # Executa o make com o alvo padrão
        result = subprocess.run(["make"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o Makefile:")
        print(e.stderr.decode())
        return False
    return True

def delete_files(pattern):
    # Encontra todos os arquivos que correspondem ao padrão e os remove
    for file in glob.glob(pattern):
        try:
            os.remove(executavel)
            print(f"Arquivo {executavel} deletado.")
        except OSError as e:
            print(f"Erro ao deletar o arquivo {executavel}: {e}")

# Função para gerar o ficheiro de input
def gerar_input(n, m, nome_ficheiro="test.in"):
    with open(nome_ficheiro, "w") as ficheiro:
        ficheiro.write(f"{n} {m}\n")
        
        # Geração da matriz n x n
        for _ in range(n):
            linha = " ".join(str(random.randint(1, n)) for _ in range(n))
            ficheiro.write(linha + "\n")
        
        # Geração de m inteiros (expressao)
        ficheiro.write(" ".join(str(random.randint(1, n)) for _ in range(m)) + "\n")
        
        # Geração do resultado desejado
        ficheiro.write(str(random.randint(1, n)) + "\n")

# Função para medir o tempo de execução do programa com um dado input
def testar_velocidade(n, m):
    gerar_input(n, m)
    
    # Mede o tempo antes da execução
    inicio = time.time()
    
    # Executa o programa com o input do ficheiro
    with open("test.in", "r") as entrada:
        subprocess.run([executavel], stdin=entrada, stdout=subprocess.DEVNULL)
    
    # Mede o tempo após a execução
    fim = time.time()
    
    # Calcula o tempo total
    tempo_execucao = fim - inicio
    
    # Retorna o tempo
    return tempo_execucao

# Dicionários para guardar tempos de execução
tempos_n = {}
tempos_m = {}

# Executa o makefile
if not run_makefile():
    exit()

# Testes variando n de 5 a 100 e m de 10 a 1000
for n in range(11, 127, 5):      # Incrementa n de 5 em 5 até 100
    tempos_n[n] = []
    for m in range(1, 1542, 70):  # Incrementa m de 50 em 50 até 1000
        tempo = testar_velocidade(n, m)
        tempos_n[n].append(tempo)
        
        # Guarda o tempo para m específico em todos os n
        if m not in tempos_m:
            tempos_m[m] = []
        tempos_m[m].append(tempo)
        
        print(f"n={n:02}, m={m:03} -> Tempo de execução: {tempo:.4f} segundos")

# Deleta o executavel

all_f_n_m_values = []
all_times = []

for n, tempos in tempos_n.items():
    m_values = list(range(1, 1402, 70))
    for i, m in enumerate(m_values):
        f_n_m = n*m*m
        all_f_n_m_values.append(f_n_m)
        all_times.append(tempos[i])

# Plota os pontos de dados originais
plt.scatter(all_f_n_m_values, all_times, alpha=0.5, color="blue")

# Ajusta uma curva polinomial de tendência para todos os dados combinados
degree = 2  # Ajusta o grau conforme necessário
coef = np.polyfit(all_f_n_m_values, all_times, degree)
poly_fn = np.poly1d(coef)

# Plota a curva de ajuste
sorted_nm_values = sorted(all_f_n_m_values)  # Ordena para uma curva suave
plt.plot(sorted_nm_values, poly_fn(sorted_nm_values), '--', color="red")

plt.xlabel("f(n,m)")
plt.ylabel("Time (s)")
plt.title("")
plt.legend()
plt.show()
