import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO ---
# Vamos ler o arquivo final que acabamos de gerar
arquivo_entrada = 'Relatorio_Fretes_Nomes_Final.xlsx'

print("--- GERANDO DASHBOARD DE FRETES ---")

try:
    # 1. CARREGA OS DADOS
    # O arquivo tem os detalhes, vamos agrupar novamente para garantir
    df = pd.read_excel(arquivo_entrada)

    # Agrupa por Transportadora
    resumo = df.groupby('Transportadora')['Valor'].sum().sort_values(
        ascending=True)  # Crescente para o gráfico ficar bonito

    total_geral = resumo.sum()

    # 2. CONFIGURA O VISUAL
    plt.style.use('ggplot')
    # Cria uma figura com 2 gráficos (lado a lado)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- GRÁFICO 1: RANKING (BARRAS HORIZONTAIS) ---
    # Cores: Um gradiente de azul
    resumo.plot(kind='barh', color='#2980B9', ax=ax1, edgecolor='black')

    ax1.set_title(f'Ranking de Gastos com Frete\nTotal: R$ {total_geral:,.2f}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Valor Gasto (R$)')
    ax1.set_ylabel('')  # Tira o label 'Transportadora' para limpar

    # Escreve os valores na frente das barras
    for index, value in enumerate(resumo):
        label = f"R$ {value:,.2f}"
        ax1.text(value, index, f' {label}', va='center', fontweight='bold', fontsize=10)

    # --- GRÁFICO 2: SHARE (ROSCA) ---
    # Pega o Top 5 e agrupa o resto como "Outros" para não poluir
    resumo_desc = resumo.sort_values(ascending=False)
    if len(resumo_desc) > 5:
        top_5 = resumo_desc.head(5)
        outros = pd.Series([resumo_desc.iloc[5:].sum()], index=['OUTROS'])
        dados_pizza = pd.concat([top_5, outros])
    else:
        dados_pizza = resumo_desc

    # Cores personalizadas para diferenciar
    cores = ['#E74C3C', '#8E44AD', '#3498DB', '#F1C40F', '#2ECC71', '#95A5A6']

    # Cria o gráfico de rosca (Pie chart com buraco no meio)
    wedges, texts, autotexts = ax2.pie(dados_pizza, labels=None, autopct='%1.1f%%',
                                       startangle=90, colors=cores, pctdistance=0.85, explode=[0.05] * len(dados_pizza))

    # Cria o círculo branco no meio
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax2.add_artist(centre_circle)

    ax2.set_title('Representatividade por Transportadora', fontsize=14, fontweight='bold')

    # Legenda lateral para ficar organizado
    ax2.legend(wedges, dados_pizza.index,
               title="Transportadoras",
               loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))

    plt.tight_layout()

    print(f"✅ Sucesso! Total Analisado: R$ {total_geral:,.2f}")
    print("Mostrando gráficos...")
    plt.show()

except FileNotFoundError:
    print(f"❌ ERRO: Não encontrei o arquivo '{arquivo_entrada}'.")
    print("Rode o script anterior (rastreio_frete_nomes.py) primeiro para gerar esse arquivo.")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")