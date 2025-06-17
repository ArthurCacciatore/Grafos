import sys
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
    print("F", k)
    print("D", end=" ")
    for i in range(len(dist)):
        print(dist[i], end=" ")
    print()
    print("A", end=" ")
    for i in range(len(ant)):
        print(ant[i], end=" ")
    print()

def PCCM(grafo, n, s, ant , dist): #perguntar para o wagner se aqui pode ter o n, pois no exemplo nao tem (?o programa funcionava sem passar o n?)
    dist = [INFINITO] * n
    ant = [-1] * n
    dist[s] = 0
    ordem_impar = ordem_atual(n,s,0)
    ordem_par = ordem_atual (n,s,1)
    print("O I", ordem_impar)
    print("O P", ordem_par)

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

    imprime_estado_final(dist, ant, k)

    if k == n:
        print("CN")
        # como encontrar = print(vertice da ultima iteração voltando até seu interior = ao da ultima iteração)
    else:
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
            # ao final do while, temos o caminho de t (atual) até s, mas só consideramos o de s até s, ou aqueles que existem (comprimento > 1)
            if (len(caminho) == 1 and v == s) or (len(caminho) > 1):
                # imprime no formato solicitado
                print("P", s, v, dist[v], *caminho)

caminho_Arquivo = sys.argv[1]
s = int(sys.argv[2])
grafo, n = ler_grafo("Arquivos/" + caminho_Arquivo)
distancia = []
anterior = []
PCCM(grafo,n, s, anterior, distancia)
