import random

class Produto:
    def __init__(self, valor, tam_x, tam_y):
        self.valor = valor
        self.tam_x = tam_x
        self.tam_y = tam_y

produtos = [
    Produto(3, 15, 15),
    Produto(5, 10, 10),
    Produto(6, 7, 4),
    Produto(8, 7, 2),
    Produto(10, 6, 4),
    Produto(12, 5, 5),
    Produto(20, 3, 3),
    Produto(30, 1, 1)
]

tamanho_maximo_x = 30
tamanho_maximo_y = 30
orcamento_maximo = 100

def calcular_custo(sol):
    return sum(produto.valor for i, produto in enumerate(produtos) if sol[i] == 1)

def verificar_restricoes(sol):
    tamanho_x = sum(produto.tam_x for i, produto in enumerate(produtos) if sol[i] == 1)
    tamanho_y = sum(produto.tam_y for i, produto in enumerate(produtos) if sol[i] == 1)
    return tamanho_x <= tamanho_maximo_x and tamanho_y <= tamanho_maximo_y and tamanho_x > 0 and tamanho_y > 0

def gerar_solucao_inicial():
    solucao = random.sample(range(1, 9), 8)
    while True:
        if verificar_restricoes(solucao) and 1 in solucao:
            return solucao
        solucao = random.sample(range(1, 9), 8)

def tabu_search(max_iter):
    solucao_inicial = gerar_solucao_inicial()
    melhor_solucao = solucao_inicial.copy()
    melhor_custo = calcular_custo(melhor_solucao)

    tabu_list = []  

    for _ in range(max_iter):
        vizinhos = []
        for i in range(len(produtos)):
            vizinho = melhor_solucao.copy()
            available_numbers = [n for n in range(1, 9) if n not in set(vizinho)]
            if available_numbers:
                novo_numero = random.choice(available_numbers)
                vizinho[i] = novo_numero  
                if vizinho not in tabu_list and verificar_restricoes(vizinho):
                    vizinhos.append((vizinho, calcular_custo(vizinho)))

        if not vizinhos:
            continue

        vizinhos.sort(key=lambda x: x[1], reverse=True)
        melhor_vizinho, custo_vizinho = vizinhos[0]

        if custo_vizinho > melhor_custo:
            melhor_solucao = melhor_vizinho
            melhor_custo = custo_vizinho

        tabu_list.append(melhor_solucao.copy())

        if len(tabu_list) > 5:
            tabu_list.pop(0)
            
        inicial = gerar_solucao_inicial()

    return melhor_solucao, melhor_custo

melhor_solucao, melhor_custo = tabu_search(max_iter=1000)

inicial = gerar_solucao_inicial()

print("Solução Inicial:", inicial)
print("Melhor solução:", melhor_solucao)
print("Melhor custo:", melhor_custo)

if verificar_restricoes(melhor_solucao):
    print("A solução atende aos requisitos.")
else:
    print("A solução não atende aos requisitos.")
