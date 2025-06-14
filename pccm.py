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



def ordem(n, s, valor ): #se valor = 0 par se = 1 impar
    if valor == 0:
        ordem = list(range(n))
        ordem.remove(s)
        ordem.insert(0, s);
    elif valor == 1: 
        ordem = list(reversed(range(n)))
        ordem.remove(s)
        ordem.insert(0, s);
    return ordem




caminho_Arquivo = sys.argv[1];
s = int(sys.argv[2]);
grafo, n = ler_grafo("Arquivos/" + caminho_Arquivo)
ordem_impar = ordem(n,s,0)
ordem_par = ordem (n,s,1)
print("O I", ordem_impar)
print("O P", ordem_par)
distancia = [INFINITO] * n
distancia[s] = 0
anterior = [-1] * n

