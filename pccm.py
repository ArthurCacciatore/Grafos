import sys
import os
INFINITO = 2_000_000_000

def ler_grafo(caminho_arquivo):
    with open(caminho_arquivo) as f:
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

def ordem_atual(n, s, valor ): #se valor = 0 par se = 1 impar   (perguntar para o vagner se usar essa funcao afetaria o desempenho para grafos GIGANTES)
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
    ant_formatado = [a if a != -1 else "-" for a in ant]
    dist_formatado = [b if b!= INFINITO else "-" for b in dist]
    print("F", k)
    print("D", *dist_formatado)
    print("A", *ant_formatado)

def PCCM(grafo, n, s, ant , dist): 
    dist = [INFINITO] * n
    ant = [-1] * n
    dist[s] = 0
    ordem_impar = ordem_atual(n,s,0)
    ordem_par = ordem_atual (n,s,1)
    print("O I", *ordem_impar)
    print("O P", *ordem_par)

    k = 1
    atualiza = True
    while(k <= n - 1 and atualiza):
        atualiza = False
        ordem = ordem_impar if  k % 2 ==1 else ordem_par
        for u in ordem:
            for d,c in grafo[u]:
                if dist[u] + c < dist[d]:
                    dist[d] = dist[u] + c
                    ant[d] = u
                    atualiza = True
        if not atualiza:
            break
        k += 1

   

    if k == n:
        # Primeiro, encontre o vértice atualizado na última iteração (k = n)
        ordem = ordem_impar if k % 2 == 1 else ordem_par
        d_ciclo = None
        for u in ordem:
            for d, c in grafo[u]:
                if dist[u] + c < dist[d]:
                    d_ciclo = d
                    break
            if d_ciclo is not None:
                break

        # Agora decrementa k para imprimir estado final
        k -= 1
        imprime_estado_final(dist, ant, k)
        print("CN")

        # Caminha n passos para garantir que está dentro do ciclo
        for _ in range(n):
            d_ciclo = ant[d_ciclo]

        # Coletar os vértices do ciclo seguindo ant, que estão na ordem invertida
        ciclo = []
        visitado = {}
        v = d_ciclo
        while v not in visitado:
            visitado[v] = len(ciclo)
            ciclo.append(v)
            v = ant[v]

        # Cortar para pegar só o ciclo real
        inicio = visitado[v]
        ciclo = ciclo[inicio:]  # ciclo invertido!

        ciclo.reverse()  # Corrige a ordem para o sentido correto

        ciclo.append(ciclo[0])  # fechar ciclo

        # Organizar para começar pelo menor vértice
        menor = min(ciclo[:-1])
        idx_menor = ciclo.index(menor)
        ciclo = ciclo[idx_menor:-1] + ciclo[:idx_menor] + [menor]

        # Calcular o custo do ciclo
        custo = 0
        for i in range(len(ciclo) - 1):
            u = ciclo[i]
            v = ciclo[i + 1]
            for viz, c in grafo[u]:
                if viz == v:
                    custo += c
                    break

        print("C", len(ciclo) - 1, custo, *ciclo)


        
        # como encontrar = print(vertice da ultima iteração voltando até seu interior = ao da ultima iteração)
    else:
        imprime_estado_final(dist, ant, k)
        # imprimir o caminho de s para cada vértice, se houver
        for v in range(n):
            # o caminho será construído a partir do antecessor até s, e deve ser invertido ao final
            caminho = []
            # analisaremos os antecessores do vértice destino
            atual = v
            # enquanto houver antecessor, adicionamos o vértice atual ao caminho
            # quando começamos de um vértice sem antecessor, o passo é pulado
            while (atual != -1):
                caminho.append(atual)
                atual = ant[atual]
            caminho.reverse()
            # ao final do while, temos o caminho de t (atual) até s, por isso é necessário inverter. podemos concluir que os únicos existentes são os que saem de s e chegam em v
            if (caminho[0] == s and caminho[-1] == v):
                # imprime no formato solicitado
                print("P", v, dist[v], len(caminho), *caminho)
            else:
                # se o caminho não começa em s ou não termina em v, não há caminho de s a v
                print("U", v)

caminho_Arquivo = sys.argv[1]
s = int(sys.argv[2]) 

base_dir = os.path.dirname(os.path.abspath(__file__))  ## ler_grafo("Arquivos/" + caminho_Arquivo)
caminho_Arquivo = os.path.join(base_dir, "Arquivos", caminho_Arquivo)
grafo, n = ler_grafo(caminho_Arquivo)
distancia = []
anterior = []
PCCM(grafo,n, s, anterior, distancia)
