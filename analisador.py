import pdfplumber
import os
import pandas as pd
import re
import requests
import time

# --- CONFIGURAÇÃO ---
pasta_pdfs = 'nfs_pdf'
arquivo_saida = 'Relatorio_Compras_Validado.xlsx'


def limpar_cnpj(cnpj):
    """Remove pontos, barras e traços do CNPJ para consulta"""
    return re.sub(r'\D', '', str(cnpj))


def consultar_nome_cnpj(cnpj):
    """
    Vai na internet (BrasilAPI) e descobre o nome da empresa pelo CNPJ.
    Retorna o nome ou 'Não Encontrado'.
    """
    cnpj_limpo = limpar_cnpj(cnpj)

    # Se o CNPJ estiver incompleto ou errado, nem tenta
    if len(cnpj_limpo) != 14:
        return f"CNPJ Inválido ({cnpj})"

    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"

    try:
        # Faz a consulta
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            # Pega a Razão Social ou o Nome Fantasia
            return dados.get('razao_social', dados.get('nome_fantasia', 'Nome Desconhecido'))
        else:
            return "Não encontrado na base"

    except Exception as e:
        print(f"Erro de conexão ao buscar CNPJ {cnpj}: {e}")
        return "Erro Conexão"


def extrair_dados_basicos(texto_pdf):
    dados = {
        "CNPJ": None,
        "Data": "N/D",
        "Valor": 0.0
    }

    # 1. Busca CNPJ
    busca_cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto_pdf)
    if busca_cnpj: dados["CNPJ"] = busca_cnpj.group(0)

    # 2. Busca Data
    busca_data = re.search(r'\d{2}/\d{2}/\d{4}', texto_pdf)
    if busca_data: dados["Data"] = busca_data.group(0)

    # 3. Busca Valor
    busca_valor = re.search(r'Valor Total.*?R\$\s?([\d.,]+)', texto_pdf, re.IGNORECASE | re.DOTALL)
    if not busca_valor:
        busca_valor = re.search(r'R\$\s?([\d.,]+)', texto_pdf)

    if busca_valor:
        valor_txt = busca_valor.group(1).replace('.', '').replace(',', '.')
        try:
            dados["Valor"] = float(valor_txt)
        except:
            dados["Valor"] = 0.0

    return dados


# --- EXECUÇÃO PRINCIPAL ---
print("--- INICIANDO LEITURA E CONSULTA DE CNPJ ---")
print("Aviso: Para funcionar, você precisa estar conectado à internet.")

lista_bruta = []

# 1. LER OS PDFs
if not os.path.exists(pasta_pdfs):
    print(f"ERRO: Pasta '{pasta_pdfs}' não encontrada.")
else:
    arquivos = [f for f in os.listdir(pasta_pdfs) if f.endswith('.pdf')]
    print(f"Lendo {len(arquivos)} arquivos PDF...")

    for i, arquivo in enumerate(arquivos):
        if (i + 1) % 10 == 0: print(f"Lendo PDF {i + 1}...")  # Mostra progresso a cada 10
        try:
            with pdfplumber.open(os.path.join(pasta_pdfs, arquivo)) as pdf:
                texto = pdf.pages[0].extract_text() or ""
                info = extrair_dados_basicos(texto)

                if info["CNPJ"]:  # Só adiciona se achou CNPJ
                    info["Arquivo"] = arquivo
                    lista_bruta.append(info)
        except Exception as e:
            pass

    # 2. CONSULTAR NOMES (A MÁGICA)
    if lista_bruta:
        df = pd.DataFrame(lista_bruta)

        # Pega a lista de CNPJs únicos para não consultar o mesmo 50 vezes
        cnpjs_unicos = df['CNPJ'].unique()
        print(f"\nEncontrei {len(cnpjs_unicos)} fornecedores diferentes.")
        print("Consultando nomes na Receita Federal (BrasilAPI)... Aguarde...")

        mapa_nomes = {}
        for i, cnpj in enumerate(cnpjs_unicos):
            print(f"[{i + 1}/{len(cnpjs_unicos)}] Consultando: {cnpj}...")
            nome = consultar_nome_cnpj(cnpj)
            mapa_nomes[cnpj] = nome
            # Pausa pequena para não bloquear o IP
            time.sleep(0.5)

            # Aplica os nomes descobertos na tabela principal
        df['Fornecedor'] = df['CNPJ'].map(mapa_nomes)

        # 3. SALVAR EXCEL
        try:
            # Organiza colunas
            df = df[['Fornecedor', 'CNPJ', 'Valor', 'Data', 'Arquivo']]

            # Cria Resumo
            resumo = df.groupby(['Fornecedor', 'CNPJ']).agg(
                Total_Gasto=('Valor', 'sum'),
                Qtd_Notas=('Arquivo', 'count')
            ).reset_index().sort_values('Total_Gasto', ascending=False)

            with pd.ExcelWriter(arquivo_saida) as writer:
                df.to_excel(writer, sheet_name='Detalhado', index=False)
                resumo.to_excel(writer, sheet_name='Resumo_Por_Fornecedor', index=False)

            print("\n" + "=" * 50)
            print("✅ SUCESSO ABSOLUTO!")
            print(f"Os nomes foram consultados e o arquivo '{arquivo_saida}' foi criado.")
            print("=" * 50)

        except PermissionError:
            print("🚨 ERRO: Feche o arquivo Excel antes de rodar!")
    else:
        print("Nenhum CNPJ encontrado nos arquivos.")