import pandas as pd

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'Relatorio_Impostos_Detalhado.xlsx'
arquivo_saida = 'Base_Consolidada_Final.xlsx'

print("--- UNIFICANDO FORNECEDORES DUPLICADOS ---")

try:
    df = pd.read_excel(arquivo_entrada)

    # 1. Cria uma coluna de "Fornecedor Tratado" se não existir
    # (Baseado na lógica que usamos antes para limpar o nome do arquivo)
    if 'Fornecedor_Tratado' not in df.columns:
        df['Fornecedor_Tratado'] = df['Arquivo'].apply(
            lambda x: x.split('NF')[0].split('R$')[0].split('RS')[0].replace('_', ' ').strip())

    # 2. Mostra como estava ANTES (para conferência)
    filtro_antes = df['Fornecedor_Tratado'].str.contains('Izabela|Explosão|Explosao', case=False, na=False)
    print("\n📊 SITUAÇÃO ATUAL (SEPARADOS):")
    print(df.loc[filtro_antes].groupby('Fornecedor_Tratado')['Valor_Nota_Total'].sum())

    # 3. A MÁGICA: UNIFICAÇÃO
    # O comando abaixo diz: "Onde tiver 'Izabela' OU 'Explosão', mude o nome para..."
    novo_nome = "EXPLOSÃO DE SABORES (UNIFICADO)"
    df.loc[filtro_antes, 'Fornecedor_Tratado'] = novo_nome

    # 4. Mostra como ficou DEPOIS
    filtro_depois = df['Fornecedor_Tratado'] == novo_nome
    total_unificado = df.loc[filtro_depois, 'Valor_Nota_Total'].sum()

    print("\n✅ SITUAÇÃO NOVA (UNIFICADOS):")
    print(f"Fornecedor: {novo_nome}")
    print(f"Novo Volume Total de Compras: R$ {total_unificado:,.2f}")
    print(f"Quantidade de Notas: {df.loc[filtro_depois].shape[0]}")

    # 5. Salva o novo arquivo consolidado
    df.to_excel(arquivo_saida, index=False)
    print(f"\n📂 Arquivo atualizado salvo como: {arquivo_saida}")
    print("Use este arquivo novo para gerar os gráficos daqui pra frente!")

except FileNotFoundError:
    print(f"Erro: Não encontrei o arquivo '{arquivo_entrada}'.")
except Exception as e:
    print(f"Erro: {e}")