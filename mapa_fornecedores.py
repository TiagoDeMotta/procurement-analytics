import pandas as pd
import requests
import time
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'BASE_MESTRA_2025_AUDITADA.xlsx'

print("--- INICIANDO RASTREAMENTO GEOGRÁFICO ---")


def consultar_uf(cnpj):
    """Consulta o Estado (UF) do CNPJ na BrasilAPI"""
    # Remove pontuação e garante que é string
    cnpj_limpo = str(cnpj).replace('.', '').replace('/', '').replace('-', '').replace('.0', '')

    # Se o CNPJ estiver incompleto (menos de 14 dígitos), ignora
    if len(cnpj_limpo) < 14:
        return 'N/D'

    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get('uf', 'N/D')
        else:
            return 'N/D'
    except:
        return 'ERRO'


try:
    # 1. CARREGAR DADOS
    print(f"Lendo arquivo: {arquivo_entrada}...")
    df = pd.read_excel(arquivo_entrada)

    # --- A CORREÇÃO DO ERRO ESTÁ AQUI ---
    # Remove linhas onde Fornecedor ou CNPJ estão vazios
    linhas_antes = len(df)
    df = df.dropna(subset=['Fornecedor', 'CNPJ'])
    linhas_depois = len(df)

    if linhas_antes > linhas_depois:
        print(f"⚠️ Limpeza: Removidas {linhas_antes - linhas_depois} linhas vazias/inválidas.")

    # Garante que Fornecedor é texto (string) para não dar erro de float
    df['Fornecedor'] = df['Fornecedor'].astype(str)
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

    # 2. LISTA DE FORNECEDORES ÚNICOS
    fornecedores_unicos = df[['CNPJ', 'Fornecedor']].drop_duplicates(subset='CNPJ')

    print(f"Encontrei {len(fornecedores_unicos)} fornecedores únicos. Consultando localização...")

    # 3. CONSULTA API
    mapa_uf = {}
    total = len(fornecedores_unicos)

    for i, (idx, row) in enumerate(fornecedores_unicos.iterrows()):
        cnpj = row['CNPJ']
        nome_fornecedor = row['Fornecedor']

        # Mostra progresso sem quebrar
        print(f"[{i + 1}/{total}] Consultando: {nome_fornecedor[:20]}...", end='\r')

        uf = consultar_uf(cnpj)
        mapa_uf[cnpj] = uf
        time.sleep(0.2)  # Pausa para não bloquear

    print("\nConsulta concluída!")

    # 4. APLICA A UF NA TABELA PRINCIPAL
    df['UF'] = df['CNPJ'].map(mapa_uf)

    # 5. FILTRA QUEM É DE FORA DO RJ
    # Lista de estados que não são RJ (excluindo N/D e ERRO)
    fora_do_rj = df[(df['UF'] != 'RJ') & (df['UF'].isin(['SP', 'MG', 'ES', 'PR', 'SC', 'RS', 'BA', 'GO', 'DF', 'AM']))]

    if fora_do_rj.empty:
        print("✅ Todos os seus fornecedores parecem ser do RJ!")
    else:
        # Agrupa por Fornecedor
        resumo_fora = fora_do_rj.groupby(['Fornecedor', 'UF'])['Valor'].sum().reset_index()
        resumo_fora = resumo_fora.sort_values(by='Valor', ascending=False)

        print("\n" + "=" * 60)
        print(f"🚨 ALERTA: {len(resumo_fora)} FORNECEDORES SÃO DE FORA DO RJ")
        print("Esses pedidos provavelmente têm frete mais caro (CIF ou FOB).")
        print("=" * 60)

        print(f"{'FORNECEDOR':<40} | {'UF':<3} | {'TOTAL (R$)':<15}")
        print("-" * 65)
        for _, row in resumo_fora.iterrows():
            print(f"{row['Fornecedor'][:40]:<40} | {row['UF']:<3} | R$ {row['Valor']:,.2f}")

        # 6. GRÁFICO
        plt.style.use('ggplot')
        # Pega os Top 10 para o gráfico não ficar polulaído
        top_10 = resumo_fora.head(10).sort_values(by='Valor', ascending=True)

        if not top_10.empty:
            fig, ax = plt.subplots(figsize=(12, 8))

            labels = [f"{row['Fornecedor'][:20]}... ({row['UF']})" for _, row in top_10.iterrows()]

            ax.barh(labels, top_10['Valor'], color='#E67E22')
            ax.set_title('Top Fornecedores de Fora do RJ (Impacto no Frete)', fontsize=14)
            ax.set_xlabel('Total Comprado (R$)')

            for i, v in enumerate(top_10['Valor']):
                ax.text(v, i, f' R$ {v:,.0f}', va='center', fontweight='bold', color='black')

            plt.tight_layout()
            plt.show()

except Exception as e:
    print(f"\nErro inesperado: {e}")
