def gerar_padroes_guloso(tamanhos, L, k=None):
    padroes = []
    n = len(tamanhos)

    tamanhos_ordenados = sorted(enumerate(tamanhos), key=lambda x: x[1], reverse=True)

    for start in range(n):
        restante = L
        padrao = [0] * n

        for i, tam in tamanhos_ordenados[start:]:
            qtd = restante // tam
            padrao[i] = qtd
            restante -= qtd * tam

        uso = sum(padrao[i] * tamanhos[i] for i in range(n))

        # 🔴 REGRA DE OURO: nunca aceitar padrão inválido
        if 0 < uso <= L:
            padroes.append(padrao)

    # remover duplicados
    vistos = set()
    unicos = []

    for p in padroes:
        t = tuple(p)
        if t not in vistos:
            vistos.add(t)
            unicos.append(p)

    def eficiencia(p):
        return sum(p[i] * tamanhos[i] for i in range(len(p))) / L

    unicos.sort(key=eficiencia, reverse=True)

    if k:
        unicos = unicos[:k]

    return unicos

from ortools.linear_solver import pywraplp

def corte_uni(comprimento_padrao, itens):
    import time
    start_time = time.time()

    if comprimento_padrao < 0:
        raise ValueError("A capacidade da barra padrão não pode ser negativa")

    if any(item.quantidade < 0 for item in itens):
        raise ValueError("A quantidade de cada item não pode ser negativa")

    if any(item.comprimento > comprimento_padrao for item in itens):
        raise ValueError("Um item não pode ter comprimento maior que a barra padrão")
    
    tamanhos = [item.comprimento for item in itens]
    demanda = [item.quantidade for item in itens]

    padroes = gerar_padroes_guloso(tamanhos, comprimento_padrao, k=6)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise Exception("Solver não pôde ser criado")

    n_padroes = len(padroes)
    n_itens = len(tamanhos)

    # variáveis
    x = [
        solver.IntVar(0, solver.infinity(), f'x[{j}]')
        for j in range(n_padroes)
    ]

    # restrição de demanda
    for i in range(n_itens):
        solver.Add(
            sum(padroes[j][i] * x[j] for j in range(n_padroes)) >= demanda[i]
        )

    # objetivo
    solver.Minimize(sum(x[j] for j in range(n_padroes)))

    solver.SetTimeLimit(60000)

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        raise Exception("Sem solução ótima")

    plano = []
    total_barras = 0
    uso_total = 0

    for j in range(n_padroes):
        qtd = int(x[j].solution_value())

        if qtd > 0:
            uso_padrao = sum(padroes[j][i] * tamanhos[i] for i in range(n_itens))

            total_barras += qtd
            uso_total += qtd * uso_padrao

            plano.append({
                "padrao_id": j,
                "quantidade_barras": qtd,
                "itens_cortados": [
                    {
                        "item_id": itens[i].id,
                        "quantidade": padroes[j][i] * qtd
                    }
                    for i in range(n_itens) if padroes[j][i] > 0
                ],
                "comprimento_utilizado_por_barra": uso_padrao,
                "sobra_por_barra": comprimento_padrao - uso_padrao
            })

    desperdicio = total_barras * comprimento_padrao - uso_total
    execution_time = time.time() - start_time

    return {
        "status_solver": status,
        "tempo_execucao_segundos": execution_time,
        "barras_utilizadas": total_barras,
        "desperdicio_total_mm": desperdicio,
        "plano_de_corte": plano
    }