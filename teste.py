def ler_grafo(caminho_arquivo):
    try:
        with open(caminho_arquivo) as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("Nao encontrei")  
        exit()

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

a = ler_grafo("Arquivos/g1.txt")
print(a)