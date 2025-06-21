import sys
import os
INFINITO = 2_000_000_000

def ler_grafo(arquivo):
    """
    Função que abre e lê um arquivo de entrada para retornar o grafo como uma lista de adjacências e o número de vértices para posterior manipulação.
    """
    with open(arquivo) as f:
        linhas = f.readlines()
    n = 0 
    grafo = []
    for linha in linhas:
        if linha.startswith("I"):
            partes = linha.split()
            n = int(partes[1])
            grafo = [[] for _ in range(n)]
        elif linha.startswith("E"):
            _, u, v, c = linha.split()
            u, v, c = int(u), int(v), int(c)
            grafo[u].append((v, c))
        elif linha.startswith("T"):
            break
    return grafo, n

def ordem_atual(n, s, valor): 
    """
    Função que retorna a ordem de visita dos vértices do grafo, dependendo do valor passado. 
    Se valor for 0, a ordem é crescente a partir de s; se for 1, a ordem é decrescente a partir de s.
    """
    if valor == 0:
        ordem = list(range(n))
        ordem.remove(s)
        ordem.insert(0, s)
    elif valor == 1: 
        ordem = list(reversed(range(n)))
        ordem.remove(s)
        ordem.insert(0, s)
    return ordem

def imprime_estado_final(dist, ant, k):
    """
    Função que imprime o estado final dos vetores seguindo o formato solicitado no trabalho.
    """
    ant_formatado = [a if a != -1 else "-" for a in ant]
    dist_formatado = [b if b!= INFINITO else "-" for b in dist]
    print("F", k)
    print("D", *dist_formatado)
    print("A", *ant_formatado)

def encontra_ciclo(ant, CN):
    """
    Função que encontra o ciclo voltando os vértices a partir daquele que foi o último atualizado no passo n-1, e retorna-o no formato de saída.
    """
    ciclo = []
    visitado = {}
    v = ant[CN] # parte do anterior do último vértice atualizado, pois ele é o primeiro do ciclo
    
    # enquanto não acharmos um vértice já visitado, seguimos o antecessor e adicionamos ao ciclo.
    # como já sabemos que há um ciclo, o primeiro que já tiver sido visitado será o início dele.
    while v not in visitado:
        visitado[v] = len(ciclo) # vértices já visitados são guardados com o tamanho do ciclo
        ciclo.append(v)
        v = ant[v]
    ciclo.reverse() # corrige a ordem para o sentido correto
    ciclo.append(ciclo[0])  # fecha o ciclo

    # organiza o ciclo para começar pelo menor vértice
    menor = min(ciclo[:-1])
    menorPos = ciclo.index(menor)
    ciclo = ciclo[menorPos:-1] + ciclo[:menorPos] + [menor]

    return ciclo

def PCCM(grafo, n, s, ant, dist): 
    """
    Função que roda o algoritmo de Bellman-Ford modificado com a ordem de visita dos vértices alternando entre ímpar e par em relação ao número da iteração, conforme a proposta do trabalho. Para grafos com ciclos negativos, constrói-o e calcula seu custo, além de imprimir o estado final dos vetores. Em caso contrário, imprime os caminhos de s para cada vértice.
    """
    # inicializa vetores de Distancia e Anterior
    dist = [INFINITO] * n
    ant = [-1] * n
    dist[s] = 0
    # computa e imprime ordens
    ordem_impar = ordem_atual(n,s,0)
    ordem_par = ordem_atual (n,s,1)
    print("O I", *ordem_impar)
    print("O P", *ordem_par)

    k = 1
    atualiza = True 
    CN = None # vai armazenar o último vértice atualizado no passo n-1, caso haja ciclo negativo
    while(k <= n - 1 and atualiza):
        atualiza = False # só continua a ser falso se (dist[u] + c >= dist[d]) para todos os vértices
        ordem = ordem_impar if  k % 2 ==1 else ordem_par # define a ordem de visita dos vértices da iteração atual
        for u in ordem:
            for d,c in grafo[u]:
                if dist[u] + c < dist[d]:
                    dist[d] = dist[u] + c
                    ant[d] = u
                    atualiza = True
                    # se for a última iteração, guardamos o vértice do ciclo
                    if k == n - 1:
                        CN = d
        if not atualiza:
            break
        k += 1

    if k == n:
        # decrementa k para imprimir estado final
        k -= 1
        imprime_estado_final(dist, ant, k)
        print("CN")
        ciclo = encontra_ciclo(ant, CN)

        # calcula o custo do ciclo
        custo = 0
        for i in range(len(ciclo) - 1):
            u = ciclo[i]
            v = ciclo[i + 1]
            for viz, c in grafo[u]:
                if viz == v:
                    custo += c
                    break
        print("C", custo, len(ciclo)-1, *ciclo)
    else:
        imprime_estado_final(dist, ant, k)
        for v in range(n):
            # imprimir o caminho de s para cada vértice, se houver
            caminho = [] # analisaremos os antecessores do vértice destino
            atual = v
            # enquanto houver antecessor, adicionamos o vértice atual ao caminho
            # quando começamos de um vértice sem antecessor, o passo é pulado
            while (atual != -1):
                caminho.append(atual)
                atual = ant[atual]
            caminho.reverse()
            # ao final do laço, temos o caminho de t (atual) até s, por isso é necessário inverter. podemos concluir que os únicos existentes são os que saem de s e chegam em v
            if (caminho[0] == s and caminho[-1] == v):
                # imprime no formato solicitado
                print("P", v, dist[v], len(caminho), *caminho)
            else:
                # se o caminho não começa em s ou não termina em v, não há caminho de s a v
                print("U", v)

arquivo = sys.argv[1]
s = int(sys.argv[2]) 

# cria o caminho adequado para o arquivo a ser aberto
# base_dir = os.path.dirname(os.path.abspath(__file__))  
# arquivo = os.path.join(base_dir, "Arquivos", arquivo)

grafo, n = ler_grafo("Arquivos/" + arquivo)
distancia = []
anterior = []
PCCM(grafo,n, s, anterior, distancia)
