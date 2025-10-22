import os
import sys

NOME_ARQUIVO = 'linhas_onibus.txt'
DELIMITADOR = ';'
HEADER = f"nome{DELIMITADOR}valor{DELIMITADOR}peso"


def verificar_e_criar_arquivo():
    """
    Verifica se o arquivo de dados existe.
    Se não existir, cria o arquivo e escreve o cabeçalho.
    """
    # os.path.isfile verifica se o arquivo já existe no diretório
    file_exists = os.path.isfile(NOME_ARQUIVO)

    if not file_exists:
        print(f"Arquivo '{NOME_ARQUIVO}' não encontrado.")
        print("Criando arquivo com o cabeçalho necessário...")
        try:
            # cria um novo arquivo caso não exista com o nome
            with open(NOME_ARQUIVO, mode='w', encoding='utf-8') as file:
                file.write(HEADER)
            print("Arquivo criado com sucesso.\n")
            return True  # Sucesso
        except Exception as e:
            print(f"Erro fatal ao criar o arquivo: {e}")
            return False  # Falha

    # se o arquivo já existe, não faz nada e retorna sucesso
    return True


def main():
    """
    Função para pedir os dados ao usuário e
    adicioná-los ao arquivo de texto.
    """
    print("--- Ferramenta de Inserção de Dados (Linhas de Ônibus) ---")
    print(f"Este script adicionará novas linhas ao arquivo '{NOME_ARQUIVO}'.")
    print("Digite 'sair' a qualquer momento para fechar.\n")

    # Primeiro, garante que o arquivo existe ou o cria
    if not verificar_e_criar_arquivo():
        sys.exit("Encerrando o programa devido a erro de arquivo.")

    while True:
        # --- 1. Obter Nome ---
        nome = input("Nome da nova linha: ").strip()
        if nome.lower() == 'sair':
            break
        if not nome:
            print("O nome não pode ser vazio. Tente novamente.\n")
            continue  # Volta ao início do loop

        # --- 2. Obter Valor (Demanda) ---
        try:
            valor_str = input(f"  Valor (Demanda) para '{nome}': ")
            if valor_str.lower() == 'sair':
                break
            valor = int(valor_str)  # Tenta converter para inteiro
            if valor < 0:
                print("  Erro: O valor não pode ser negativo.\n")
                continue
        except ValueError:
            print("  Erro: Valor deve ser um número inteiro. Tente novamente.\n")
            continue  # Volta ao início do loop

        # --- 3. Obter Peso (Ocupação) ---
        try:
            peso_str = input(f"  Peso (Ocupação) para '{nome}': ")
            if peso_str.lower() == 'sair':
                break
            peso = int(peso_str)  # Tenta converter para inteiro
            if peso < 0:
                print("  Erro: O peso não pode ser negativo.\n")
                continue
        except ValueError:
            print("  Erro: Peso deve ser um número inteiro. Tente novamente.\n")
            continue  # Volta ao início do loop

        # --- 4. Formatar e Salvar ---
        nova_linha = f"\n{nome}{DELIMITADOR}{valor}{DELIMITADOR}{peso}"

        try:
            # adicionando ao final do arquivo a nova linha
            with open(NOME_ARQUIVO, mode='a', encoding='utf-8') as file:
                file.write(nova_linha)

            print(f"\n✅ SUCESSO! Linha '{nome}' adicionada ao arquivo.\n")

        except Exception as e:
            print(f"\nERRO FATAL: Ocorreu um erro inesperado ao salvar: {e}")
            print("O programa será encerrado.")
            break

    print("\nPrograma finalizado.")


# Executa a função principal quando o script é rodado
if __name__ == "__main__":
    main()