# É necessário instalar a biblioteca:
# pip install ortools

from ortools.linear_solver import pywraplp
import csv

def resolver_mochila_urbs(dados_linhas, capacidade_total):
    """
    Resolve o Problema da Mochila 0/1 para alocação de linhas no terminal.

    Argumentos:
    dados_linhas (dict): Dicionário contendo 'nomes', 'valores' (Demanda) e 'pesos' (Ocupação).
    capacidade_total (int): A capacidade total do terminal.
    """

    # Extrai os dados
    valores = dados_linhas['valores']
    pesos = dados_linhas['pesos']
    nomes = dados_linhas['nomes']
    num_itens = len(valores)

    # 1. Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver SCIP não disponível, tentando CBC...")
        solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Nenhum solver de MIP (SCIP ou CBC) encontrado.")
        return

    # 2. Criar as variáveis de decisão (x_i)
    x = {}
    for i in range(num_itens):
        x[i] = solver.BoolVar(f'x[{i}]')

    # 3. Definir a Restrição (Constraint)
    restricao = solver.Constraint(0, capacidade_total, 'Restricao_Capacidade') #para dizer a capacidade limite ao solver
    for i in range(num_itens):
        restricao.SetCoefficient(x[i], pesos[i])#conecta a variavel aos pesos

    # 4. Definir a Função Objetivo (Objective Function)
    objetivo = solver.Objective()
    for i in range(num_itens):
        objetivo.SetCoefficient(x[i], valores[i])#controi a formula para pegar a maximização
    objetivo.SetMaximization()

    # 5. Resolver o problema
    status = solver.Solve()#devolve o resultado

    # 6. Exibir os resultados (Versão formatada para leigos)
    if status == pywraplp.Solver.OPTIMAL:
        print("\n" + "=" * 50)
        print("   RELATÓRIO DE OTIMIZAÇÃO DO TERMINAL (URBS)")
        print("=" * 50)

        print(f"\nAnalisamos {num_itens} linhas de ônibus para encontrar a melhor combinação.")

        print("\n[ O OBJETIVO ]")
        print("Maximizar o número total de passageiros transportados por hora.")

        print("\n[ A RESTRIÇÃO ]")
        print(f"Não ultrapassar a capacidade máxima do terminal, que é de {capacidade_total} unidades de ocupação.")

        print("\n" + "---" * 17)
        print("         RESULTADO DA OTIMIZAÇÃO ENCONTRADO")
        print("---" * 17)

        print(f"\n✅ Demanda Máxima Atingida: {objetivo.Value():.0f} passageiros por hora.")
        print("\nPara atingir esse resultado, as seguintes linhas devem ser alocadas:")

        peso_total = 0
        linhas_selecionadas = []

        for i in range(num_itens):
            if x[i].solution_value() > 0.5:  # Se x[i] == 1
                linhas_selecionadas.append(
                    f"  - {nomes[i]:<30} (Atende: {valores[i]} pass/hora, Ocupação: {pesos[i]})"
                )
                peso_total += pesos[i]

        for linha_str in linhas_selecionadas:
            print(linha_str)

        print("\n[ RESUMO DA OCUPAÇÃO DO TERMINAL ]")
        print(f"Ocupação Total utilizada: {peso_total:.0f} unidades")
        print(f"Capacidade Total do Terminal: {capacidade_total} unidades")

        percentual_uso = (peso_total / capacidade_total) * 100
        print(f"\nConclusão: O terminal operará com {percentual_uso:.0f}% de sua capacidade máxima.")

    elif status == pywraplp.Solver.INFEASIBLE:
        print("\n" + "!" * 50)
        print("  RELATÓRIO DE OTIMIZAÇÃO DO TERMINAL (URBS)")
        print("!" * 50)
        print("\n[ PROBLEMA ENCONTRADO ]")
        print("O sistema não encontrou uma solução.")
        print(f"Isso pode significar que a capacidade ({capacidade_total}) é muito baixa.")
    else:
        print("O problema não pôde ser resolvido para uma solução ótima.")


def carregar_dados_do_arquivo_texto(nome_arquivo):

    dados_para_resolver = {
        'nomes': [],
        'valores': [],
        'pesos': []
    }

    try:
        # Abrimos o arquivo com encoding 'utf-8' (para acentos)
        with open(nome_arquivo, mode='r', encoding='utf-8') as file:

            # Usamos DictReader, especificando que o separador é ';'
            leitor_csv = csv.DictReader(file, delimiter=';')

            for linha in leitor_csv:
                try:
                    dados_para_resolver['nomes'].append(linha['nome'])
                    # Converte valor e peso para números inteiros
                    dados_para_resolver['valores'].append(int(linha['valor']))
                    dados_para_resolver['pesos'].append(int(linha['peso']))
                except ValueError:
                    print(f"Erro: A linha '{linha['nome']}' tem um valor ou peso que não é um número.")
                except KeyError:
                    print("Erro: O arquivo está faltando uma das colunas: 'nome', 'valor' ou 'peso'.")

    except FileNotFoundError:
        print(f"Erro Crítico: Arquivo '{nome_arquivo}' não encontrado.")
        print("Por favor, crie este arquivo no mesmo diretório do script.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return None

    return dados_para_resolver

if __name__ == "__main__":

    NOME_ARQUIVO = 'linhas_onibus.txt'
    capacidade_terminal = 100


    # 1. Carrega os dados do arquivo
    print(f"Carregando dados do arquivo '{NOME_ARQUIVO}'...")
    dados_linhas_urbs = carregar_dados_do_arquivo_texto(NOME_ARQUIVO)

    # 2. Se os dados foram carregados com sucesso, resolve o problema
    if dados_linhas_urbs:
        if not dados_linhas_urbs['nomes']:
            print("O arquivo de dados está vazio. Nada para otimizar.")
        else:
            resolver_mochila_urbs(dados_linhas_urbs, capacidade_terminal)
    else:
        print("A otimização não pôde ser executada devido a erros na leitura dos dados.")