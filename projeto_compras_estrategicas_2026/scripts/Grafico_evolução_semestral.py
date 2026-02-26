import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO ---
# Use a Base Mestra, pois ela tem a coluna 'Data'
arquivo_entrada = 'BASE_MESTRA_2025_AUDITADA.xlsx'

print("--- GERANDO GRÁFICO DE EVOLUÇÃO DO SEMESTRE ---")

try:
    # 1. Carrega os dados
    df = pd.read_excel(arquivo_entrada)

    # 2. Tratamento das Datas e Valores
    # Converte a coluna Data para o formato de data do Python
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

    # Remove linhas que não tenham data válida
    df = df.dropna(subset=['Data'])

    # Extrai o Mês/Ano para agrupar (Ex: 2025-07)
    df['Mes'] = df['Data'].dt.to_period('M')

    # 3. Agrupamento (A Mágica)
    # Soma o valor e conta quantas notas existem por mês
    resumo = df.groupby('Mes').agg(
        Valor_Total=('Valor', 'sum'),
        Qtd_NFs=('Valor', 'count')
    ).reset_index()

    # Formata o mês para o gráfico ficar com o nome bonitinho (Ex: Jul/25)
    resumo['Mes_Str'] = resumo['Mes'].dt.strftime('%b/%y').str.title()

    # 4. Configuração do Gráfico Duplo (Combo Chart)
    plt.style.use('ggplot')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # --- EIXO Y ESQUERDO (BARRAS - DINHEIRO) ---
    cor_dinheiro = '#3498DB'  # Azul corporativo
    barras = ax1.bar(resumo['Mes_Str'], resumo['Valor_Total'], color=cor_dinheiro, alpha=0.8, edgecolor='black')

    ax1.set_ylabel('Valor Total Gasto (R$)', color=cor_dinheiro, fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=cor_dinheiro)
    ax1.set_xlabel('Meses do Semestre', fontsize=12)

    # Escreve o valor em R$ em cima de cada barra
    for barra in barras:
        altura = barra.get_height()
        ax1.text(barra.get_x() + barra.get_width() / 2., altura + 1000,
                 f'R$ {altura:,.0f}', ha='center', va='bottom', color='#2C3E50', fontweight='bold', fontsize=10)

    # --- EIXO Y DIREITO (LINHA - OPERAÇÃO/NFs) ---
    ax2 = ax1.twinx()  # Cria um segundo eixo Y que compartilha o mesmo eixo X
    cor_operacao = '#E74C3C'  # Vermelho alerta

    linha = ax2.plot(resumo['Mes_Str'], resumo['Qtd_NFs'], color=cor_operacao, marker='o',
                     linewidth=3, markersize=10, label='Qtd de NFs')

    ax2.set_ylabel('Quantidade de Notas Fiscais (Trabalho Operacional)', color=cor_operacao, fontsize=12,
                   fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=cor_operacao)

    # Escreve a quantidade de notas na bolinha da linha
    for i, valor in enumerate(resumo['Qtd_NFs']):
        ax2.text(i, valor + 1.5, f'{valor} NFs', ha='center', va='bottom', color=cor_operacao, fontweight='bold',
                 fontsize=11)

    # Ajusta os limites do eixo da linha para o texto não cortar no topo
    ax2.set_ylim(bottom=0, top=resumo['Qtd_NFs'].max() * 1.2)

    # 5. Títulos e Ajustes Finais
    plt.title('Evolução de Compras: Gasto Estratégico vs. Volume Operacional', fontsize=16, fontweight='bold')

    # Grid apenas no eixo esquerdo para não poluir
    ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
    ax2.grid(False)

    plt.tight_layout()
    print("✅ Gráfico gerado com sucesso! Mostrando na tela...")
    plt.show()

except FileNotFoundError:
    print(f"❌ ERRO: Arquivo '{arquivo_entrada}' não encontrado. Verifique se ele está na pasta.")
except Exception as e:
    print(f"❌ ERRO INESPERADO: {e}")