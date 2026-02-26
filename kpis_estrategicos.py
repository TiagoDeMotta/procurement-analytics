import pandas as pd
import matplotlib.pyplot as plt
import sys

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'BASE_MESTRA_2025_AUDITADA.xlsx'

print("--- CALCULANDO ÍNDICES ESTRATÉGICOS ---")

try:
    # 1. CARGA DE DADOS
    # Tenta carregar o arquivo. Se estiver aberto, avisa.
    try:
        df = pd.read_excel(arquivo_entrada)
    except PermissionError:
        print("\n❌ ERRO: O arquivo Excel está aberto!")
        print(f"Feche o arquivo '{arquivo_entrada}' e tente novamente.")
        sys.exit()

    # Tratamentos
    df['Data_Formatada'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
    df['Dia'] = df['Data_Formatada'].dt.day
    df['Mes_Ano'] = df['Data_Formatada'].dt.to_period('M')

    plt.style.use('ggplot')

    # ==============================================================================
    # KPI 1: PULVERIZAÇÃO
    # ==============================================================================
    total_gasto = df['Valor'].sum()
    qtd_fornecedores = df['Fornecedor'].nunique()

    if qtd_fornecedores > 0:
        media_por_fornecedor = total_gasto / qtd_fornecedores
    else:
        media_por_fornecedor = 0

    print(f"\n1️⃣ ANÁLISE DE PULVERIZAÇÃO")
    print(f"   > Total Gasto: R$ {total_gasto:,.2f}")
    print(f"   > Base Ativa: {qtd_fornecedores} fornecedores")
    print(f"   > Ticket Médio por Parceiro: R$ {media_por_fornecedor:,.2f}")

    # ==============================================================================
    # KPI 2: A SÍNDROME DO FIM DE MÊS
    # ==============================================================================
    bins = [0, 10, 25, 31]
    labels = ['Início (1-10)', 'Meio (11-25)', 'Fechamento (26+)']
    df['Periodo_Mes'] = pd.cut(df['Dia'], bins=bins, labels=labels)

    analise_periodo = df.groupby('Periodo_Mes', observed=False)['Valor'].sum()

    # Gráfico Pizza
    if analise_periodo.sum() > 0:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        analise_periodo.plot(kind='pie', autopct='%1.1f%%', colors=['#2ECC71', '#F1C40F', '#E74C3C'], ax=ax1,
                             startangle=90)
        ax1.set_ylabel('')
        ax1.set_title('Concentração de Compras por Período', fontsize=14)
        print("   > Mostrando gráfico de planejamento (feche para continuar)...")
        plt.show()

    # ==============================================================================
    # KPI 3: PESO DO FRETE (COM PROTEÇÃO DE ERRO)
    # ==============================================================================
    termos_frete = ['TRANSPORTE', 'LOGISTICA', 'EXPRESSO', 'RODONAVES', 'GARIBALDI', 'FRETE']
    mask_frete = df['Fornecedor'].str.contains('|'.join(termos_frete), case=False, na=False)

    df['Tipo'] = 'Material'
    df.loc[mask_frete, 'Tipo'] = 'Frete'

    # Cria a tabela dinâmica
    evolucao = df.groupby(['Mes_Ano', 'Tipo'])['Valor'].sum().unstack(fill_value=0)

    # PROTEÇÃO: Verifica se a coluna 'Frete' existe. Se não existir, cria com zero.
    if 'Frete' not in evolucao.columns:
        evolucao['Frete'] = 0.0
    if 'Material' not in evolucao.columns:
        evolucao['Material'] = 0.0

    # Calcula o % com segurança (evita divisão por zero)
    total_mensal = evolucao['Frete'] + evolucao['Material']
    evolucao['% Frete'] = 0.0
    mask_total_ok = total_mensal > 0
    evolucao.loc[mask_total_ok, '% Frete'] = (evolucao.loc[mask_total_ok, 'Frete'] / total_mensal.loc[
        mask_total_ok]) * 100

    print(f"\n3️⃣ EVOLUÇÃO DO CUSTO LOGÍSTICO")
    print(evolucao[['Frete', '% Frete']])

    # Gráfico Linha
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    evolucao['% Frete'].plot(kind='line', marker='o', color='#8E44AD', linewidth=3, ax=ax2)
    ax2.set_title('Peso do Frete no Custo Total (%)', fontsize=14)
    ax2.set_ylabel('% Custo', color='#8E44AD')
    ax2.grid(True)

    print("   > Mostrando gráfico de frete...")
    plt.tight_layout()
    plt.show()

except Exception as e:
    print("\n" + "X" * 40)
    print(f"ERRO ENCONTRADO: {e}")
    print("Verifique se o arquivo Excel existe e não está aberto.")
    print("X" * 40)