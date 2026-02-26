import os
import pandas as pd
import re

# --- CONFIGURAÇÃO ---
# O 'r' antes das aspas é obrigatório para caminhos do Windows com barras invertidas
pasta_arquivos = r"C:\Users\LENOX PC\OneDrive\Documentos\NF PARA ANALISE  COM NOME DE FORNECEDORES"
arquivo_saida = 'Relatorio_Baseado_Nomes.xlsx'

print(f"--- INICIANDO LEITURA NA PASTA: {pasta_arquivos} ---")


def extrair_info_nome(nome_arquivo):
    """
    Extrai Fornecedor, NF e Valor do nome do arquivo.
    """
    dados = {
        'Arquivo': nome_arquivo,
        'Fornecedor': 'Não Identificado',
        'Numero_Nota': 'N/D',
        'Valor': 0.0
    }

    # Remove a extensão .pdf
    nome_limpo = os.path.splitext(nome_arquivo)[0]

    # 1. TENTA ACHAR O VALOR (Padrão: 200,50 ou 1.200,00)
    # Procura dígitos seguidos de vírgula ou ponto e mais 2 dígitos
    busca_valor = re.search(r'(?:R\$ ?)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+\.\d{2})', nome_limpo)

    nome_sem_valor = nome_limpo  # Cópia para continuar limpando

    if busca_valor:
        valor_texto = busca_valor.group(1)
        # Remove o valor do nome para não confundir com o número da nota
        nome_sem_valor = nome_limpo.replace(busca_valor.group(0), '')

        # Converte para número (Python)
        # Tira o ponto de milhar e troca vírgula decimal por ponto
        valor_formatado = valor_texto.replace('.', '').replace(',', '.')
        try:
            dados['Valor'] = float(valor_formatado)
        except:
            dados['Valor'] = 0.0

    # 2. TENTA ACHAR O NÚMERO DA NOTA
    # Procura números inteiros que sobraram no texto
    numeros_encontrados = re.findall(r'\d+', nome_sem_valor)

    if numeros_encontrados:
        # Geralmente o número da nota é o maior número inteiro que sobra (ex: 45032)
        # Filtra números pequenos que podem ser dia/ano (menor que 3 digitos) se houver opção melhor
        candidatos = [n for n in numeros_encontrados if len(n) >= 3]

        if candidatos:
            dados['Numero_Nota'] = max(candidatos, key=len)
        elif numeros_encontrados:
            dados['Numero_Nota'] = numeros_encontrados[0]

        # Remove o número da nota do texto
        nome_sem_nf = nome_sem_valor.replace(str(dados['Numero_Nota']), '')
    else:
        nome_sem_nf = nome_sem_valor

    # 3. O QUE SOBROU É O FORNECEDOR
    # Limpa traços, underlines e espaços extras
    fornecedor_sujo = nome_sem_nf.replace('-', ' ').replace('_', ' ').replace('NF', '').strip()
    # Remove espaços duplos
    dados['Fornecedor'] = " ".join(fornecedor_sujo.split())

    # Se o nome ficou vazio (só tinha numero e valor), usa o original
    if len(dados['Fornecedor']) < 2:
        dados['Fornecedor'] = "Nome Indefinido"

    return dados


# --- EXECUÇÃO ---
lista_dados = []

if not os.path.exists(pasta_arquivos):
    print(f"❌ ERRO CRÍTICO: Não encontrei a pasta no caminho:")
    print(f"{pasta_arquivos}")
    print("Verifique se o caminho está correto e se o OneDrive está sincronizado.")
else:
    try:
        arquivos = [f for f in os.listdir(pasta_arquivos) if f.lower().endswith('.pdf')]
        print(f"Encontrei {len(arquivos)} arquivos PDF. Processando nomes...")

        for i, arquivo in enumerate(arquivos):
            info = extrair_info_nome(arquivo)
            lista_dados.append(info)
            if (i + 1) % 50 == 0: print(f"Processados {i + 1}...")

        if lista_dados:
            df = pd.DataFrame(lista_dados)

            # Organiza colunas
            df = df[['Fornecedor', 'Numero_Nota', 'Valor', 'Arquivo']]

            # Salva
            df.to_excel(arquivo_saida, index=False)

            print("\n" + "=" * 50)
            print("✅ SUCESSO! DADOS EXTRAÍDOS DOS NOMES.")
            print(f"📂 Arquivo gerado: {arquivo_saida}")
            print("=" * 50)
            print(f"Total Lido: R$ {df['Valor'].sum():,.2f}")

        else:
            print("Nenhum arquivo PDF encontrado na pasta.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
