import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

arquivo_entrada = 'Base_Consolidada_Final.xlsx'  # Ou Relatorio_Impostos_Detalhado.xlsx
print("--- GERANDO MATRIZ ESTRATÉGICA (TEXTOS CORRIGIDOS) ---")

try:
    df = pd.read_excel(arquivo_entrada)
    if 'Fornecedor_Tratado' not in df.columns:
        df['Fornecedor_Tratado'] = df['Arquivo'].apply(
            lambda x: x.split('NF')[0].split('R$')[0].split('RS')[0].replace('_', ' ').strip()[:15])

    dados = df.groupby('Fornecedor_Tratado').agg(
        Total_Comprado=('Valor_Nota_Total', 'sum'),
        Total_Imposto=('Total_Impostos', 'sum')
    ).reset_index()

    dados['Eficiencia_Fiscal'] = (dados['Total_Imposto'] / dados['Total_Comprado']) * 100
    dados['Eficiencia_Fiscal'] = dados['Eficiencia_Fiscal'].fillna(0)
    dados = dados[dados['Total_Comprado'] > 1500]  # Aumentei o filtro para limpar a base

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 8))
    tamanhos = (dados['Total_Comprado'] / dados['Total_Comprado'].max()) * 2000 + 100

    scatter = ax.scatter(dados['Total_Comprado'], dados['Eficiencia_Fiscal'], s=tamanhos,
                         c=dados['Eficiencia_Fiscal'], cmap='RdYlGn', alpha=0.8, edgecolors='gray')

    media_compra = dados['Total_Comprado'].median()
    ax.axvline(x=media_compra, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=10, color='blue', linestyle='--', alpha=0.5)

    ax.text(dados['Total_Comprado'].max() * 0.9, 15, "ESTRELAS\n(Alto Crédito)", color='green', fontweight='bold',
            ha='center')
    ax.text(dados['Total_Comprado'].max() * 0.9, 2, "ALERTA\n(Baixo Crédito)", color='red', fontweight='bold',
            ha='center')

    # --- O SEGREDO PARA NÃO ENCAVALAR OS NOMES ---
    top_10 = dados.sort_values(by='Total_Comprado', ascending=False).head(10)

    # Adiciona um deslocamento (offset) alternado para cima e para baixo
    offset_y = 1.5
    for i in range(len(top_10)):
        x = top_10['Total_Comprado'].iloc[i]
        y = top_10['Eficiencia_Fiscal'].iloc[i]
        label = top_10['Fornecedor_Tratado'].iloc[i]

        # Alterna a posição do texto (um para cima, um para baixo)
        direcao = offset_y if i % 2 == 0 else -offset_y

        ax.annotate(label, (x, y), xytext=(0, direcao * 15), textcoords='offset points',
                    ha='center', va='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                    arrowprops=dict(arrowstyle="-", color="gray"))

    ax.set_title('Matriz de Compras 2026: Volume vs. Eficiência Fiscal', fontsize=16, pad=20)
    ax.set_xlabel('Volume Total de Compras (R$)', fontsize=12)
    ax.set_ylabel('Retorno em Crédito Tributário (%)', fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'R$ {x:,.0f}'))

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Erro: {e}")
    