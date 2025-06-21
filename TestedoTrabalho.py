import subprocess
import os
import re

def normaliza(texto):
    # Remove espaços no final de cada linha e ignora linhas vazias no final
    return '\n'.join(l.strip() for l in texto.strip().splitlines())

d = 0
c = 0
nome_da_pasta_entrada = "Arquivos"  #Nome da pasta com os txt de entrada
nome_da_pasta_saidas = "SaidasEsperadas" #nome da pasta que tem os arquivos .out

codigoentrada = "pccm.py" #Nome do codigo que vai rodar
nome_do_txt = "g-1000-10000.txt" #nome do arquivo de entrada para testar
saida_prefixo = "g-1000-10000-" #Coloque apenas o nome do arquivo antes do ultimo elemento exemplo para o arquivo g-1000-10000.txt aqui deve ser g-1000-10000- 

# ele pega automaticamente o numero das saidas de teste e passa como entrada para o codigo 
base_dir = os.path.dirname(os.path.abspath(__file__))
pccm_path = os.path.join(base_dir, codigoentrada)
entrada = os.path.join(base_dir, nome_da_pasta_entrada, nome_do_txt)
saida_dir = os.path.join(base_dir, nome_da_pasta_saidas)
saida_sufixo = ".out"

# Expressão regular para extrair X de arquivos tipo g-1000-10000-X.out
padrao_saida = re.compile(rf"{re.escape(saida_prefixo)}(\d+)\.out")
#padrao_saida = re.compile(r"g-neg-e-10-30-(\d+)\.out")

# Lista todos os arquivos e filtra os que batem com o padrão
arquivos_saida = []    
for nome in os.listdir(saida_dir):
    if padrao_saida.match(nome):
        c += 1
        arquivos_saida.append(nome)

# Ordena os arquivos por X (convertido para inteiro)
arquivos_saida.sort(key=lambda nome: int(padrao_saida.match(nome).group(1)))

# Processa cada arquivo de saída esperado
for nome_saida in arquivos_saida:
    match = padrao_saida.match(nome_saida)
    if not match:
        continue
    
    x = match.group(1)  # Parâmetro X extraído do nome
    caminho_saida = os.path.join(saida_dir, nome_saida)

    print(f"\nTestando com X={x} (arquivo {nome_saida})")

    # Executa o programa com o X correspondente
    resultado = subprocess.run(
        ["python", pccm_path, entrada, x],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    with open(caminho_saida, "r") as f:
        esperado = f.read().strip()

    obtido = resultado.stdout.strip()

    if normaliza(esperado) == normaliza(obtido):
        print(f"Saída correta para X={x}")
        d +=1
    else:
        print(f"Saída incorreta para X={x}")
        print("---- Esperado ----")
        print(esperado)
        print("---- Obtido ------")
        print(obtido)
        print("\nComparação detalhada:")
        for i, (e_char, o_char) in enumerate(zip(esperado, obtido)):
            if e_char != o_char:
                print(f"Posição {i}: esperado='{repr(e_char)}' obtido='{repr(o_char)}'")

        if resultado.stderr.strip():
            print("Erro na execução:")
            print(resultado.stderr.strip())
print(f"Numero de arquivos = {c} --  Corretos: {d}")